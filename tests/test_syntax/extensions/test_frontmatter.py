"""
Tests for the `frontmatter` extension.

License: BSD (see LICENSE.md for details).
"""

import subprocess
import sys
import tempfile
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
        # Only a first line that opens the block is consumed; a `---` deeper in
        # the document is still rendered as a horizontal rule.
        self.assertMarkdownRenders(
            'Text\n\n---\n\nMore',
            '<p>Text</p>\n<hr />\n<p>More</p>',
            extensions=['frontmatter'],
        )

    def test_registered_under_the_short_name(self):
        from importlib.metadata import entry_points

        names = {ep.name for ep in entry_points(group='markdown.extensions')}
        self.assertIn('frontmatter', names)

    def test_command_line_extension_flag(self):
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
