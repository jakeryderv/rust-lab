#!/usr/bin/env python3
"""Combine converted reading copies by chapter without modifying the input.

Usage: python3 scripts/aggregate_references.py SOURCE_DIRECTORY OUTPUT_DIRECTORY
The source contains converted book/ and rust-by-example/ directories. Output must
not exist. The upstream SUMMARY.md order defines chapter and subsection order.
"""

from collections import Counter
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import sys
from urllib.parse import unquote, urlsplit, urlunsplit

from convert_references import outside_fences


HEADING = re.compile(r'^(?P<prefix>(?:>\s*)*)(?P<marks>#{1,6}) (?P<title>.+)$', re.M)
DEFINITION = re.compile(r'^ {0,3}\[(?!\^)([^\]\n]+)\]:[ \t]*(\S+)([^\n]*)$', re.M)
ANCHOR = re.compile(r'<a\s+(?:id|name)="([^"]+)"[^>]*></a>')

# These two links already target missing anchors in the supplied snapshot.
# Keep them usable by linking to the beginning of the referenced section.
LEGACY_ANCHORS = {
    ('book/ch17-03-more-futures.md', 'working-with-any-number-of-futures'),
    ('book/ch17-04-streams.md', 'composing-streams'),
}


def prose_only(text, transform):
    return outside_fences(text, transform, lambda opening, body, closing: opening[0] + body + closing)


def slug(text):
    # Generic parameters inside code spans are text, not HTML tags.
    text = ''.join(part if part.startswith('`') else re.sub(r'<[^>]+>', '', part)
                   for part in re.split(r'(`+[^`]*`+)', text))
    text = html.unescape(text).lower().replace('`', '')
    return re.sub(r'[^\w\-\s]', '', text).replace(' ', '-')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def headings(text):
    result = []
    counts = Counter()
    def collect(prose):
        for match in HEADING.finditer(prose):
            base = slug(match['title'])
            anchor = base + (f'-{counts[base]}' if counts[base] else '')
            counts[base] += 1
            result.append((match['title'], len(match['marks']), anchor, bool(match['prefix'])))
        return prose
    prose_only(text, collect)
    return result


def summary_entries(root):
    entries = []
    for match in re.finditer(r'^( *)- \[(.+)\]\(([^)]+\.md)\)$', (root / 'SUMMARY.md').read_text(), re.M):
        entries.append((len(match[1]), match[2], match[3]))
    return entries


def plan(source):
    pages, groups, summaries = {}, {}, {}
    for resource in ('book', 'rust-by-example'):
        root = source / resource
        entries = summary_entries(root)
        summary, chapter = [], 0
        group = None
        for indent, title, filename in entries:
            old = f'{resource}/{filename}'
            if resource == 'book':
                match = re.match(r'ch(\d+)-\d+-(.+)\.md', filename)
                if match and int(match[1]):
                    if indent == 0:
                        group = f'{resource}/{match[1]}-{match[2]}.md'
                        summary.append((0, title, group))
                    depth = 0 if indent == 0 else 1
                elif filename.startswith('appendix-'):
                    target = 'README.md' if filename == 'appendix-00.md' else filename.removeprefix('appendix-')
                    group, depth = f'{resource}/appendices/{target}', 0
                    summary.append((indent, title, group))
                else:
                    group, depth = old, 0
                    summary.append((0, title, group))
            else:
                if indent == 0:
                    if filename == 'index.md':
                        group = old
                    else:
                        chapter += 1
                        group = f'{resource}/{chapter:02d}-{slug(title)}.md'
                    summary.append((0, title, group))
                depth = indent // 4
            assert group is not None
            text = (source / old).read_text()
            page_id = 'section-' + filename.removesuffix('.md').replace('/', '-')
            hs = headings(text)
            explicit = []
            prose_only(text, lambda s: explicit.extend(ANCHOR.findall(s)) or s)
            anchors = {a: page_id + '--' + a for a in [h[2] for h in hs] + explicit}
            anchors.update({anchor: page_id for path, anchor in LEGACY_ANCHORS if path == old})
            pages[old] = dict(target=group, anchor=page_id, anchors=anchors,
                              depth=depth, title=title, text=text, headings=hs,
                              explicit=explicit, source_sha256=digest(text.encode()))
            groups.setdefault(group, []).append(old)
        known = {p.relative_to(source).as_posix() for p in root.rglob('*.md')}
        expected = {p for p in pages if p.startswith(resource + '/')} | {f'{resource}/README.md', f'{resource}/SUMMARY.md'}
        if known != expected:
            raise ValueError(f'Unmapped Markdown files: {known ^ expected}')
        summaries[resource] = summary
    return pages, groups, summaries


def rewrite_url(url, old, new, pages):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or url.startswith('/'):
        return url
    resolved = os.path.normpath(str(Path(old).parent / unquote(parsed.path))) if parsed.path else old
    fragment = unquote(parsed.fragment)
    if resolved in pages:
        page = pages[resolved]
        target = page['target']
        if fragment:
            if fragment not in page['anchors']:
                raise ValueError(f'Unknown source anchor: {old} -> {url}')
            fragment = page['anchors'][fragment]
        elif not page['depth']:
            fragment = ''
        else:
            fragment = page['anchor']
    else:
        target = resolved
    path = '' if target == new and fragment else os.path.relpath(target, Path(new).parent)
    return urlunsplit(('', '', path, parsed.query, fragment))


def rewrite_links(text, old, new, pages):
    def prose(s):
        s = re.sub(r'(\]\()([^\s)]+)(\))', lambda m: m[1] + rewrite_url(m[2], old, new, pages) + m[3], s)
        return DEFINITION.sub(lambda m: m[0][:m.start(2) - m.start()] + rewrite_url(m[2], old, new, pages) + m[3], s)
    return prose_only(text, prose)


def scope_references(text, namespace):
    """Keep independently authored reference labels and footnotes independent."""
    labels = {}
    def collect(s):
        for match in DEFINITION.finditer(s):
            key = ' '.join(match[1].split()).casefold()
            labels[key] = namespace + '-ref-' + str(len(labels) + 1)
        return s
    prose_only(text, collect)
    def prose(s):
        spans = []
        def protect(m):
            spans.append(m[0])
            return f'\x00CODE{len(spans) - 1}\x00'
        def restore(value):
            return re.sub(r'\x00CODE(\d+)\x00', lambda m: spans[int(m[1])], value)
        # Brackets inside inline Rust code are not Markdown references. Masking
        # also lets labels such as [`#[allow(...)]`][allow] match as a unit.
        s = re.sub(r'(`+)(?!`)(.+?)(?<!`)\1(?!`)', protect, s, flags=re.S)
        # Expand shortcuts/collapsed references and namespace explicit labels.
        # A single pass prevents touching the labels we have just generated.
        pattern = r'(?<![\\\[])\[([^\[\]]+)\](?:\[([^\[\]]*)\])?'
        def reference(m):
            label = m[2] if m[2] else m[1]
            key = ' '.join(restore(label).split()).casefold()
            if m[1].startswith('^') and m[2] is None:
                return '[^' + namespace + '-' + m[1][1:] + ']'
            if key not in labels:
                return m[0]
            if m[2] is None and s[m.end():].startswith(':') and not s[s.rfind('\n', 0, m.start()) + 1:m.start()].strip():
                return '[' + labels[key] + ']'
            if m[2] is None and s[m.end():].startswith('('):
                return m[0]
            return '[' + m[1] + '][' + labels[key] + ']'
        return restore(re.sub(pattern, reference, s))
    return prose_only(text, prose)


def transform_page(old, page, pages):
    text = rewrite_links(page['text'], old, page['target'], pages)
    text = scope_references(text, page['anchor'])
    hs = iter(page['headings'])
    base_level = next(h[1] for h in page['headings'] if not h[3])
    missing_title = old.startswith('book/') and page['depth'] == 1 and base_level > 2
    if missing_title:
        base_level = 2
    def prose(s):
        s = ANCHOR.sub(lambda m: m[0].replace(m[1], page['anchors'][m[1]], 1), s)
        def heading(m):
            _, level, anchor, quoted = next(hs)
            level = min(6, level - base_level + page['depth'] + 1)
            explicit = '' if anchor in page['explicit'] else m['prefix'] + '<a id="' + page['anchors'][anchor] + '"></a>\n' + m['prefix'] + '\n'
            return explicit + m['prefix'] + '#' * level + ' ' + m['title']
        return HEADING.sub(heading, s)
    title = '## ' + page['title'] + '\n\n' if missing_title else ''
    return '<a id="' + page['anchor'] + '"></a>\n\n' + title + prose_only(text, prose)


def code_blocks(text):
    blocks = []
    outside_fences(text, lambda s: s, lambda o, body, c: blocks.append((o[0], body, c.rstrip('\n'))) or '')
    return blocks


def validate(root):
    """Check every local destination and explicit fragment outside code fences."""
    root = Path(root)
    ids = {}
    files = list(root.rglob('*.md'))
    for file in files:
        anchors = []
        prose_only(file.read_text(), lambda s: anchors.extend(ANCHOR.findall(s)) or s)
        if len(anchors) != len(set(anchors)):
            raise ValueError(f'Duplicate anchors in {file}')
        ids[file.resolve()] = set(anchors) | {h[2] for h in headings(file.read_text())}
    checked = 0
    for file in files:
        urls = []
        def collect(s):
            urls.extend(re.findall(r'\]\(([^\s)]+)\)', s))
            urls.extend(m[2] for m in DEFINITION.finditer(s))
            return s
        prose_only(file.read_text(), collect)
        for url in urls:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or url.startswith('/'):
                continue
            dest = (file.parent / unquote(parsed.path)).resolve() if parsed.path else file.resolve()
            # The library links back to the repo's conversion scripts.
            if not dest.exists() and not parsed.path.startswith('../scripts/'):
                raise ValueError(f'Missing destination: {file}: {url}')
            if parsed.fragment and dest in ids and unquote(parsed.fragment) not in ids[dest]:
                raise ValueError(f'Missing fragment: {file}: {url}')
            checked += 1
    return checked


def aggregate(source, output):
    source, output = Path(source), Path(output)
    if (source / 'aggregation-manifest.json').exists():
        raise ValueError('Input has already been aggregated; use the original converted snapshot.')
    pages, groups, summaries = plan(source)
    shutil.copytree(source, output)
    for resource in summaries:
        for file in (output / resource).rglob('*.md'):
            file.unlink()
    for target, members in groups.items():
        sections = [transform_page(old, pages[old], pages) for old in members]
        # Each transformed source appears exactly once, in SUMMARY order.
        text = '\n\n'.join(section.rstrip() for section in sections) + '\n'
        first = pages[members[0]]
        toc = []
        if len(members) > 1:
            for old in members[1:]:
                p = pages[old]
                toc.append('  ' * max(0, p['depth'] - 1) + f'- [{p["title"]}](#{p["anchor"]})')
        else:
            toc = [f'- [{title}](#{first["anchors"][anchor]})' for title, level, anchor, quoted in first['headings'][1:] if not quoted and level <= 3]
        index = os.path.relpath(Path(target).parts[0] + '/SUMMARY.md', Path(target).parent)
        nav = f'\n[Chapter index]({index})\n'
        if toc:
            nav += '\n**In this chapter**\n\n' + '\n'.join(toc) + '\n'
        # The first heading is the chapter title; place navigation beneath it.
        match = HEADING.search(text)
        text = text[:match.end()] + '\n' + nav + text[match.end():]
        dest = output / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text)
        before = [block for old in members for block in code_blocks(pages[old]['text'])]
        if before != code_blocks(text):
            raise ValueError(f'Code examples changed: {target}')
    for resource, summary in summaries.items():
        title = 'The Rust Programming Language' if resource == 'book' else 'Rust by Example'
        lines = [f'# {title}', '', 'Each chapter contains its own linked contents list.', '']
        for indent, label, target in summary:
            lines.append('  ' * bool(indent) + f'- [{label}]({os.path.relpath(target, resource)})')
        (output / resource / 'SUMMARY.md').write_text('\n'.join(lines) + '\n')
        readme = (source / resource / 'README.md').read_text()
        readme = rewrite_links(readme, resource + '/README.md', resource + '/README.md', pages)
        readme = readme.replace('Start with the [table of contents](SUMMARY.md).', 'Start with the [chapter index](SUMMARY.md). Each chapter is a single Markdown file with a linked contents list where it has subsections.')
        (output / resource / 'README.md').write_text(readme)
    for directory in sorted(output.rglob('*'), key=lambda p: len(p.parts), reverse=True):
        if directory.is_dir() and not any(directory.iterdir()):
            directory.rmdir()
    # All non-Markdown source assets, including licenses, remain byte-for-byte intact.
    for original in source.rglob('*'):
        if original.is_file() and original.suffix != '.md':
            assert original.read_bytes() == (output / original.relative_to(source)).read_bytes()
    manifest = {
        'format_version': 1,
        'description': 'Paths are relative to references/. Source hashes describe the pre-aggregation reading copies. conversion-manifest.json retains upstream provenance.',
        'sources': {old: {key: value for key, value in p.items() if key in ('target', 'anchor', 'anchors', 'depth', 'source_sha256')} for old, p in pages.items()},
        'chapters': groups,
        'legacy_anchor_fallbacks': [dict(source=path, fragment=anchor, target=pages[path]['target'] + '#' + pages[path]['anchor']) for path, anchor in sorted(LEGACY_ANCHORS) if path in pages],
    }
    (output / 'aggregation-manifest.json').write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + '\n')
    notes = (output / 'README.md').read_text()
    start = notes.index('The Book retains')
    end = notes.index('\nWebsite themes', start)
    notes = notes[:start] + """The Book has one file per numbered chapter, with front matter and individual
appendices kept separately. Rust by Example has one file per top-level chapter.
Each chapter has a linked contents list where it has subsections, and both
`SUMMARY.md` files are compact chapter indexes. Section links in the repository
roadmap jump directly into the combined chapters.

All source reading content, code examples, images, captions, and example warnings
are retained. Includes are embedded directly and code fences are ordinary Markdown.
Source lines hidden by mdBook are exposed without their special `#` prefix;
anchored includes retain the displayed excerpt only. Examples may be fragments or
intentionally fail. Running them still requires Rust and, where applicable, their
own dependencies, files, toolchains, or platform.

The [aggregation manifest](aggregation-manifest.json) maps every original reading
page to its chapter and section anchors, and records the original page hashes.
Link labels, footnotes, and anchors are scoped to their original sections to avoid
collisions. Two missing anchors in the supplied Book async snapshot now lead to
the beginning of their referenced sections; these fallbacks are recorded in the
manifest. Filenames in `conversion-manifest.json` refer to the original source
layout and remain unchanged as provenance.
""" + notes[end:]
    notes = notes.replace('Review and validate new output before replacing these copies.',
        'The conversion script automatically runs the [chapter aggregation step](../scripts/aggregate_references.py).\n'
        'To aggregate an existing, uncombined reading copy into a new directory:\n\n'
        '```sh\npython3 scripts/aggregate_references.py /path/to/reading-copies /path/to/new-output\n```\n\n'
        'Review and validate new output before replacing these copies.')
    (output / 'README.md').write_text(notes)
    count = validate(output)
    print(f'Combined {len(pages)} source pages into {len(groups)} reading files; validated {count} local links.')
    return pages


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    aggregate(Path(sys.argv[1]), Path(sys.argv[2]))
