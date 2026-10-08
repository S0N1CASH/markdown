"""
Front matter extension: drop the `---` block at the top of a document.
"""

from __future__ import annotations

from . import Extension
from ..preprocessors import Preprocessor


class FrontmatterPreprocessor(Preprocessor):
    """ Remove everything from a leading `---` line down to the next `---`. """

    def run(self, lines: list[str]) -> list[str]:
        if not lines or lines[0].strip() != '---':
            return lines
        for index in range(1, len(lines)):
            if lines[index].strip() == '---':
                return lines[index + 1:]
        return []


class FrontmatterExtension(Extension):
    """ Front matter extension for Python-Markdown. """

    def extendMarkdown(self, md):
        md.preprocessors.register(FrontmatterPreprocessor(md), 'frontmatter', 28)
