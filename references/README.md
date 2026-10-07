# Rust learning references

- [The Rust Programming Language](book/SUMMARY.md)
- [Rust by Example](rust-by-example/SUMMARY.md)

These are adapted Markdown reading copies of [rust-lang/book](https://github.com/rust-lang/book)
and [rust-lang/rust-by-example](https://github.com/rust-lang/rust-by-example).
Converted on 2026-10-07 from locally supplied snapshots. Their Git
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
