import html
import io
import unittest

from bibtex_to_table import latex_to_display_text, write_entry


class LatexDisplayTests(unittest.TestCase):
    def test_latex_text_and_math(self):
        cases = [
            (r'\&', '&'),
            (r'J{\"{o}}rg', 'J\u00f6rg'),
            (r"P{\'{e}}rez", 'P\u00e9rez'),
            (r'Nicole B\"auerle', 'Nicole B\u00e4uerle'),
            (r"Jes\'us Mu\~noz Morcillo", 'Jes\u00fas Mu\u00f1oz Morcillo'),
            (r'{IEEE} $\mathbf{x}_{k}$', r'IEEE $\mathbf{x}_{k}$'),
            (r'\(x_{k}\) \& A', r'\(x_{k}\) & A'),
        ]
        for source, expected in cases:
            with self.subTest(source=source):
                self.assertEqual(latex_to_display_text(source), expected)

    def test_rendered_entry_preserves_bibtex(self):
        entry = {
            'ENTRYTYPE': 'inproceedings',
            'ID': 'test',
            'title': r'J{\"{o}}rg \& P{\'{e}}rez $x_{k}$',
            'author': r'Nicole B\"auerle and Uwe D. Hanebeck',
            'booktitle': r'{IEEE} \& {KIT}',
            'year': '2026',
        }
        original = dict(entry)
        raw = '@inproceedings{test, title = {' + entry['title'] + '}}'
        output = io.StringIO()
        write_entry(entry, output, 'Uwe D. Hanebeck', raw)
        rendered = output.getvalue()
        self.assertIn('J\u00f6rg &amp; P\u00e9rez $x_{k}$', rendered)
        self.assertIn('Nicole B\u00e4uerle, Uwe D. Hanebeck', rendered)
        self.assertIn('IEEE &amp; KIT', rendered)
        self.assertIn(html.escape(raw, quote=False), rendered)
        self.assertEqual(entry, original)


if __name__ == '__main__':
    unittest.main()