import sys
import unittest
import re
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build import inline, render_body, load_reports


class ParsedLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])

    def handle_data(self, data):
        self.text.append(data)


class RenderBodyTests(unittest.TestCase):
    def test_blank_lines_do_not_restart_ordered_list(self):
        rendered = render_body(("", "1. 第一项", "", "2. 第二项", "", "3. 第三项"))

        self.assertEqual(rendered.count("<ol>"), 1)
        self.assertEqual(rendered.count("</ol>"), 1)
        self.assertEqual(rendered.count("<li>"), 3)

    def test_section_heading_starts_a_new_ordered_list(self):
        rendered = render_body(("【前端】", "1. 第一项", "", "2. 第二项", "", "【后端】", "3. 第三项"))

        self.assertEqual(rendered.count("<ol>"), 2)
        self.assertIn("</ol>\n<h3>后端</h3>\n<ol>", rendered)

    def test_plain_project_hashes_become_direct_github_links(self):
        rendered = inline("（trading-bot-dashboard：abcdef12、1234567；trading-bot：89abcdef；eth-wallet-generator：40d4dda9）")

        self.assertIn('href="https://github.com/Virae-Labs/trading-bot-dashboard/commit/abcdef12"', rendered)
        self.assertIn('href="https://github.com/Virae-Labs/trading-bot-dashboard/commit/1234567"', rendered)
        self.assertIn('href="https://github.com/Virae-Labs/trading-bot/commit/89abcdef"', rendered)
        self.assertIn('href="https://github.com/Virae-Labs/eth-wallet-generator/commit/40d4dda9"', rendered)

    def test_existing_full_commit_link_is_not_wrapped_again(self):
        rendered = inline(
            "（trading-bot：[abcdef12](https://github.com/HQSV-Labs/trading-bot/commit/abcdef1234567890abcdef1234567890abcdef12)）"
        )

        self.assertEqual(rendered.count("<a href="), 1)

    def test_existing_short_commit_link_is_not_wrapped_again(self):
        rendered = inline(
            "（trading-bot：[abcdef12](https://github.com/Virae-Labs/trading-bot/commit/abcdef12)）"
        )

        self.assertEqual(rendered.count("<a href="), 1)
        self.assertIn('href="https://github.com/Virae-Labs/trading-bot/commit/abcdef12"', rendered)

    def test_hash_outside_project_reference_stays_plain(self):
        self.assertEqual(inline("版本 abcdef12"), "版本 abcdef12")

    def test_descriptive_labels_and_multiple_links(self):
        source = '( [trading-bot abcdef12](https://github.com/Virae-Labs/trading-bot/commit/abcdef12)、[使用说明](https://example.com/docs?a=1&b=2) )'
        parsed = ParsedLinks()
        parsed.feed(inline(source))
        self.assertEqual(parsed.links, ['https://github.com/Virae-Labs/trading-bot/commit/abcdef12', 'https://example.com/docs?a=1&b=2'])
        self.assertEqual(''.join(parsed.text), '( trading-bot abcdef12、使用说明 )')

    def test_code_and_unsafe_links_remain_inert(self):
        rendered = inline('`[example](https://example.com)` [bad](javascript:alert) <script>alert(1)</script>')
        self.assertIn('<code>[example](https://example.com)</code>', rendered)
        self.assertNotIn('<a ', rendered)
        self.assertNotIn('<script>', rendered)
        self.assertIn('&lt;script&gt;', rendered)

    def test_all_archived_report_links_are_anchors(self):
        for report in load_reports():
            with self.subTest(date=report.day):
                expected = re.findall(r'\]\((https?://[^\s)]+)\)', '\n'.join(report.lines))
                parsed = ParsedLinks()
                parsed.feed(render_body(report.lines))
                self.assertTrue(expected)
                for url in expected:
                    self.assertIn(url, parsed.links)
                self.assertNotRegex(''.join(parsed.text), r'\]\(https?://')


if __name__ == "__main__":
    unittest.main()
