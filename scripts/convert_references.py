#!/usr/bin/env python3
"""Convert pristine upstream snapshots into Markdown reading copies.

Usage: python3 scripts/convert_references.py SOURCE_DIRECTORY OUTPUT_DIRECTORY
SOURCE_DIRECTORY must contain book/ and rust-by-example/. OUTPUT_DIRECTORY must
not exist. Uses only the Python standard library; does not alter the source.
Includes are expanded as visible excerpts, not as executable rustdoc test units.
"""

import hashlib
from datetime import date
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import urljoin, urlsplit


class Attributes(HTMLParser):
    def handle_starttag(self, tag, attrs):
        self.attrs = dict(attrs)


def attrs(tag):
    parser = Attributes()
    parser.feed(tag)
    return parser.attrs


def excerpt(path, selector):
    lines = path.read_text().splitlines()
    # This imported upstream file mistakenly repeats its opening 'all' marker
    # on the final line. Its intended excerpt is the entire source file.
    if path.as_posix().endswith('/ch02-guessing-game-tutorial/listing-02-01/src/main.rs') and selector == 'all':
        if lines[0] == '// ANCHOR: all' and lines[-1] == '// ANCHOR: all':
            lines[-1] = '// ANCHOR_END: all'
    if path.as_posix().endswith('/ch15-smart-pointers/listing-15-22/src/lib.rs') and selector == 'here':
        # Upstream duplicates a start marker separated only by a blank line.
        joined = '\n'.join(lines).replace('        // ANCHOR: here\n\n        // ANCHOR: here', '        // ANCHOR: here')
        lines = joined.splitlines()
    if selector:
        if re.fullmatch(r"\d+(?::\d*)?", selector):
            parts = selector.split(":")
            start = int(parts[0]) - 1
            end = int(parts[1]) if len(parts) == 2 and parts[1] else (
                len(lines) if len(parts) == 2 else start + 1
            )
            end = min(end, len(lines))  # mdBook ranges may extend past EOF.
            if not 0 <= start < end <= len(lines):
                raise ValueError(f"Invalid line range {path}:{selector}")
            lines = lines[start:end]
        else:
            selected, active, found = [], False, False
            for line in lines:
                if re.search(r"\bANCHOR:\s*" + re.escape(selector) + r"\s*$", line):
                    assert not active, (path, selector)
                    active = found = True
                elif re.search(r"\bANCHOR_END:\s*" + re.escape(selector) + r"\s*$", line):
                    assert active, (path, selector)
                    active = False
                elif active:
                    selected.append(line)
            if not found or active:
                raise ValueError(f"Missing/unclosed anchor {path}:{selector}")
            lines = selected
    return "\n".join(line for line in lines if not re.search(r"\bANCHOR(?:_END)?:", line))


def outside_fences(text, transform, transform_code):
    """Keep nested shorter fences and source-code HTML out of prose rewrites."""
    result, prose, code = [], [], []
    opening = None
    for line in text.splitlines(keepends=True):
        fence = re.match(r"^( {0,3}(?:>[ \t]?)* {0,3})(`{3,}|~{3,})([^\n]*)\n?$", line)
        if opening is None:
            if fence:
                result.append(transform("".join(prose)))
                prose = []
                opening = fence
            else:
                prose.append(line)
        elif fence and fence[2][0] == opening[2][0] and len(fence[2]) >= len(opening[2]) and not fence[3].strip():
            result.append(transform_code(opening, "".join(code), line))
            opening, code = None, []
        else:
            code.append(line)
    if opening:
        raise ValueError("Unclosed code fence")
    result.append(transform("".join(prose)))
    return "".join(result)


def convert(source, output):
    output.mkdir(parents=True, exist_ok=False)
    report = {}
    for name in ("book", "rust-by-example"):
        root = source / name
        dest = output / name
        shutil.copytree(root / "src", dest)
        stats = {"markdown_files": 0, "includes": [], "externalized_links": []}
        report[name] = stats
        tree_hash = hashlib.sha256()
        for file in sorted(root.rglob("*")):
            if file.is_file() and ".git" not in file.relative_to(root).parts:
                tree_hash.update(str(file.relative_to(root)).encode() + b'\0')
                tree_hash.update(hashlib.sha256(file.read_bytes()).digest())
        stats['source_tree_sha256'] = tree_hash.hexdigest()
        for notice in ("LICENSE-APACHE", "LICENSE-MIT", "COPYRIGHT"):
            if (root / notice).exists():
                shutil.copy2(root / notice, dest / notice)
        for original in sorted((root / "src").rglob("*.md")):
            relative = original.relative_to(root / "src")
            target = dest / relative
            text = original.read_text()
            stats["markdown_files"] += 1

            def include(match):
                spec = match[2].strip()
                filename, _, selector = spec.partition(":")
                path = (original.parent / filename).resolve()
                if not path.is_relative_to(root.resolve()):
                    raise ValueError(f"Include outside source tree: {path}")
                content = excerpt(path, selector)
                stats["includes"].append({"chapter": str(relative), "source": spec, "sha256": hashlib.sha256(content.encode()).hexdigest()})
                return content

            text = re.sub(r"\{\{#(rustdoc_include|include)\s+([^}]+)\}\}", include, text)
            if "{{#" in text:
                raise ValueError(f"Unresolved directive: {original}")
            pending_caption = []

            def link(url):
                parsed = urlsplit(url)
                if parsed.scheme or parsed.netloc or not parsed.path or url.startswith("/"):
                    return url
                path = parsed.path
                rewritten = path[:-5] + ".md" if path.endswith(".html") else path
                local = target.parent / rewritten
                if local.is_file():
                    return rewritten + ("?" + parsed.query if parsed.query else "") + ("#" + parsed.fragment if parsed.fragment else "")
                # Links to other Rust manuals stay useful on the official site.
                base = "https://doc.rust-lang.org/" + name + "/" + relative.as_posix()
                remote = urljoin(base, url)
                stats["externalized_links"].append({"chapter": str(relative), "original": url, "url": remote})
                return remote

            def prose(s):
                s = re.sub(r'^(#{1,6} .+?)\s+\{#([^}]+)\}[ \t]*$', lambda m: '<a id="' + m[2] + '"></a>\n\n' + m[1], s, flags=re.M)
                def listing(m):
                    if m[0].startswith("</"):
                        if not pending_caption:
                            raise ValueError(f"Unmatched listing in {original}")
                        caption = pending_caption.pop()
                        return "\n\n" + caption + "\n\n"
                    a = attrs(m[0])
                    caption = a.get("caption", "")
                    if a.get("number"):
                        caption = "Listing " + a["number"] + ": " + caption
                    pending_caption.append(caption)
                    return "\n\n" + ("Filename: `" + a["file-name"] + "`\n\n" if a.get("file-name") else "")

                s = re.sub(r"</?Listing\b(?:[^\"<>]|\"[^\"]*\")*>", listing, s)
                def image(m):
                    a = attrs(m[0])
                    alt = " ".join(a.get("alt", "").split()).replace("[", r"\[").replace("]", r"\]")
                    return "![" + alt + "](" + a["src"] + ")"
                s = re.sub(r'<img\b[^>]*>', image, s, flags=re.S)
                s = re.sub(r'</?(?:figure|figcaption)\b[^>]*>', '\n\n', s)
                s = re.sub(r'<span\b[^>]*>(.*?)</span>', lambda m: m[1], s, flags=re.S)
                # Keep explicit HTML anchors: existing links depend on them.
                s = re.sub(r"(\]\()([^\s)]+)(\))", lambda m: m[1] + link(m[2]) + m[3], s)
                s = re.sub(r"(^ {0,3}\[(?!\^)[^\]\n]+\]:[ \t]*)(\S+)", lambda m: m[1] + link(m[2]), s, flags=re.M)
                return re.sub(r"\n{3,}", "\n\n", s)

            def code(opening, content, closing):
                info = [x.strip() for x in opening[3].split(",")]
                lang = info[0]
                notes = []
                if lang.lower() == "rust" or lang == "ignore":
                    lang = "rust"
                    labels = set(info[1:])
                    if {"does_not_compile", "compile_fail"} & labels:
                        notes.append("This example intentionally does not compile.")
                    if {"should_panic", "panics"} & labels:
                        notes.append("This example is expected to panic.")
                    if "not_desired_behavior" in labels:
                        notes.append("This example demonstrates undesired behavior.")
                    if "ignore" in info:
                        notes.append("Upstream excludes this example from automated compilation tests; it may be incomplete or require additional context.")
                    if "no_run" in labels:
                        notes.append("Upstream compiles this example without running it.")
                    if "test_harness" in labels:
                        notes.append("Run this example with Rust's test harness.")
                    for label in sorted(labels):
                        if label.startswith("edition"):
                            notes.append("This example uses Rust edition " + label[7:] + ".")
                    # Expose scaffold already present in source fences. Includes
                    # select only visible excerpts, just as the rendered book does.
                    content = re.sub(r"^((?:>[ \t]?)*[ \t]*)# (.*)$", r"\1\2", content, flags=re.M)
                    content = re.sub(r"^((?:>[ \t]?)*[ \t]*)#$", r"\1", content, flags=re.M)
                    content = re.sub(r"^((?:>[ \t]?)*[ \t]*)##", r"\1#", content, flags=re.M)
                prefix = "".join(opening[1] + "> **Example note:** " + note + "\n" + opening[1].rstrip() + "\n" for note in notes)
                return prefix + opening[1] + opening[2] + lang + "\n" + content + closing

            text = outside_fences(text, prose, code)
            if relative.name == 'SUMMARY.md':
                text = re.sub(r'^(\[[^\n]+\]\([^\n]+\))$', r'- \1', text, flags=re.M)
            if pending_caption:
                raise ValueError(f"Unclosed listing in {original}")
            if name == "rust-by-example" and str(relative) == "hello.md":
                text = text.replace('// You can test this code by clicking the "Run" button over there ->\n// or if you prefer to use your keyboard, you can use the "Ctrl + Enter"\n// shortcut.', '// Save this code as hello.rs and run it with rustc, as shown below.')
                text = text.replace('// You can always return to the original code by clicking the "Reset" button ->', '// Keep a copy of the original if you want to reset your experiment.')
                text = text.replace("Click 'Run' above to see the expected output.", "Compile and run the program locally to see the expected output.")
            target.write_text(text)
        (dest / "README.md").write_text(
            f"# {'The Rust Programming Language' if name == 'book' else 'Rust by Example'}\n\n"
            "Start with the [table of contents](SUMMARY.md).\n\n"
            f"Adapted from [rust-lang/{name}](https://github.com/rust-lang/{name}) "
            "for reading in a Markdown viewer. See [conversion notes](../README.md).\n\n"
            "Code blocks are learning examples, not necessarily standalone programs. "
            "Intentionally failing examples and relevant execution constraints are labeled.\n\n"
            "Original licensing: [MIT](LICENSE-MIT) or [Apache 2.0](LICENSE-APACHE).\n"
        )
    (output / "conversion-manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    (output / "README.md").write_text(f"""# Rust learning references

- [The Rust Programming Language](book/SUMMARY.md)
- [Rust by Example](rust-by-example/SUMMARY.md)

These are adapted Markdown reading copies of [rust-lang/book](https://github.com/rust-lang/book)
and [rust-lang/rust-by-example](https://github.com/rust-lang/rust-by-example).
Converted on {date.today().isoformat()} from locally supplied snapshots. Their Git
metadata had already been removed, so the exact upstream commits are unknown.
The [conversion manifest](conversion-manifest.json) records source-tree fingerprints,
the included excerpts, and links redirected to other official Rust manuals.

## Reading

Open either table of contents in a Markdown viewer supporting tables, footnotes,
and local SVG/PNG images. No mdBook, Cargo, or preprocessing is needed to read.
Explicit HTML anchors are retained for existing section links; viewers that strip
HTML anchors may not support every deep link. External documentation needs internet.

The Book retains all 112 source Markdown files and 28 images. Its 707 includes
are embedded directly, with listing captions, filenames, and example warnings.
Rust by Example retains all 198 source Markdown files and their directory structure.
Both use ordinary code fences. Source lines hidden by mdBook are exposed without
their special `#` prefix; anchored includes retain the displayed excerpt only.
Examples may be fragments or intentionally fail. Running them still requires Rust
and, where applicable, their own dependencies, files, toolchains, or platform.

Website themes, build tools, translations, historical editions, and print-production
copies were removed. Diagrams and original license/copyright notices are retained.
These are adapted upstream texts, not original notes; keep personal notes in `notes/`.

## Repeating the conversion

The standard-library-only [conversion script](../scripts/convert_references.py)
accepts a directory containing pristine `book/` and `rust-by-example/` snapshots
and a new, nonexistent output directory:

```sh
python3 scripts/convert_references.py /path/to/pristine-snapshots /path/to/new-output
```

Review and validate new output before replacing these copies. Conversion does not
fetch upstream content or modify its input. The current script explicitly handles
two malformed upstream anchor markers (guessing-game listing 2-1 and smart-pointer
listing 15-22); line selections extending past EOF stop at the end of the file.
The source-tree fingerprint hashes sorted relative paths followed by NUL and each
file's SHA-256 digest, excluding `.git` metadata.
""")
    print(json.dumps({name: {"chapters": s["markdown_files"], "includes": len(s["includes"]), "externalized_links": len(s["externalized_links"])} for name, s in report.items()}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    convert(Path(sys.argv[1]), Path(sys.argv[2]))
