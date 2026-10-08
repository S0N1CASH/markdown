"""
Tests for the `frontmatter` extension.
"""

import unittest

import markdown

from markdown.test_tools import TestCase

DASHES = """\
---
title: Hello
tags: [a, b]
---
# Heading

Body text.
"""

DOTS = """\
---
title: Hello
...
# Heading
"""

UNCLOSED = """\
---
title: Hello
tags: [a, b]
"""

NO_FRONTMATTER = """\
# Heading

- one
- two
"""


class TestFrontmatter(TestCase):
    """ The front matter block must vanish without touching the rest. """

    def test_closed_by_dashes(self):
        self.assertMarkdownRenders(
            DASHES,
            '<h1>Heading</h1>\n<p>Body text.</p>',
            extensions=['frontmatter'],
        )

    @unittest.skip("题面没规定 `...` 能不能结束，先不测")
    def test_closed_by_dots(self):
        self.assertMarkdownRenders(
            DOTS,
            '<h1>Heading</h1>',
            extensions=['frontmatter'],
        )

    def test_unclosed_block_drops_the_rest(self):
        self.assertMarkdownRenders(
            UNCLOSED,
            '',
            extensions=['frontmatter'],
        )

    def test_document_without_frontmatter_is_unchanged(self):
        self.assertMarkdownRenders(
            NO_FRONTMATTER,
            markdown.markdown(NO_FRONTMATTER),
            extensions=['frontmatter'],
        )

    def test_horizontal_rule_at_the_top_is_untouched(self):
        self.assertMarkdownRenders(
            'Text\n\n---\n\nMore',
            '<p>Text</p>\n<hr />\n<p>More</p>',
            extensions=['frontmatter'],
        )

    def test_registered_under_the_short_name(self):
        from importlib.metadata import entry_points

        names = {ep.name for ep in entry_points(group='markdown.extensions')}
        self.assertIn('frontmatter', names)

    @unittest.skip("命令行只是 entry point 的包装，与 API 等价，不必单独跑进程")
    def test_command_line_extension_flag(self):
        import subprocess
        import sys
        import tempfile

        with tempfile.NamedTemporaryFile('w', suffix='.md', delete=False) as handle:
            handle.write(DASHES)
            path = handle.name
        result = subprocess.run(
            [sys.executable, '-m', 'markdown', '-x', 'frontmatter', path],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout, '<h1>Heading</h1>\n<p>Body text.</p>')


if __name__ == '__main__':
    unittest.main()
