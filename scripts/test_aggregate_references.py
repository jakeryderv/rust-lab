"""Regression checks for chapter aggregation and the upstream conversion pipeline."""

from pathlib import Path
import tempfile
import unittest

from aggregate_references import code_blocks, rewrite_links, scope_references, slug, validate
from convert_references import convert


class AggregationTests(unittest.TestCase):
    def test_reference_labels_and_inline_rust_are_independent(self):
        text = ('Use `[dependencies]` and [`#[allow(...)]`][allow].\n'
                '[dependencies], [dependencies][], [other][dependencies].\n\n'
                '[dependencies]: https://example.com/deps\n'
                '[allow]: https://example.com/allow\n')
        actual = scope_references(text, 'one')
        self.assertIn('`[dependencies]`', actual)
        self.assertIn('[`#[allow(...)]`][one-ref-2]', actual)
        self.assertIn('[dependencies][one-ref-1], [dependencies][one-ref-1], [other][one-ref-1]', actual)
        self.assertIn('[one-ref-1]: https://example.com/deps', actual)
        self.assertNotEqual(actual, scope_references(text, 'two'))

    def test_code_fences_and_footnotes(self):
        text = ('Note[^1].\n\n[^1]: Footnote.\n\n'
                '````rust\n// [label] and ``` are code\nlet x = "[^1]";\n````\n'
                '\n[label]: https://example.com\n')
        actual = scope_references(text, 'page')
        self.assertEqual(code_blocks(actual), code_blocks(text))
        self.assertIn('Note[^page-1]', actual)
        self.assertIn('[^page-1]: Footnote.', actual)

    def test_shortcut_labels_can_contain_code(self):
        actual = scope_references('[Borrowing (`&`)]\n\n[Borrowing (`&`)]: target.md\n', 'page')
        self.assertIn('[Borrowing (`&`)][page-ref-1]', actual)
        self.assertIn('[page-ref-1]: target.md', actual)

    def test_heading_generics_are_not_html(self):
        self.assertEqual(slug('Shared Access to `Mutex<T>`'), 'shared-access-to-mutext')

    def test_link_rebase_does_not_replace_definition_label(self):
        actual = rewrite_links('[x.md]: x.md\n![image](image.svg)\n', 'book/x.md', 'book/appendices/x.md', {})
        self.assertEqual(actual, '[x.md]: ../x.md\n![image](../image.svg)\n')

    def test_pristine_conversion_includes_aggregation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source, output = root / 'source', root / 'output'
            files = {
                'book/LICENSE-MIT': 'Test license\n',
                'book/LICENSE-APACHE': 'Test license\n',
                'rust-by-example/LICENSE-MIT': 'Test license\n',
                'rust-by-example/LICENSE-APACHE': 'Test license\n',
                'book/src/SUMMARY.md': '# Book\n\n- [Start](ch01-00-start.md)\n  - [Install](ch01-01-install.md)\n',
                'book/src/ch01-00-start.md': '# Start\n\n[Install](ch01-01-install.html#install)\n',
                'book/src/ch01-01-install.md': '## Install\n\n![diagram](img.svg)\n\n```rust\n{{#include ../sample.rs}}\n```\n',
                'book/src/img.svg': '<svg></svg>\n',
                'book/sample.rs': 'fn main() {}\n',
                'rust-by-example/src/SUMMARY.md': '# Summary\n\n- [Hello](hello.md)\n    - [Print](hello/print.md)\n',
                'rust-by-example/src/hello.md': '# Hello\n\n[link]\n\n[link]: https://example.com/hello\n',
                'rust-by-example/src/hello/print.md': '# Print\n\n[link]\n\n[link]: https://example.com/print\n',
            }
            for name, text in files.items():
                file = source / name
                file.parent.mkdir(parents=True, exist_ok=True)
                file.write_text(text)
            convert(source, output)
            self.assertTrue((output / 'book/01-start.md').is_file())
            self.assertFalse((output / 'book/ch01-01-install.md').exists())
            self.assertIn('fn main() {}', (output / 'book/01-start.md').read_text())
            example = (output / 'rust-by-example/01-hello.md').read_text()
            self.assertIn('[section-hello-ref-1]: https://example.com/hello', example)
            self.assertIn('[section-hello-print-ref-1]: https://example.com/print', example)
            self.assertGreater(validate(output), 0)
            for name, text in files.items():
                self.assertEqual((source / name).read_text(), text)
            with self.assertRaises(FileExistsError):
                convert(source, output)


if __name__ == '__main__':
    unittest.main()
