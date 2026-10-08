# Front Matter Extension for Python-Markdown
# ==========================================

# Discards a YAML-style front matter block sitting at the top of a document.

# See the [documentation](https://Python-Markdown.github.io/extensions/meta_data)
# for the closely related `meta` extension.

"""
This extension drops the leading front matter block of a document: the block
opens with a line containing only `---` and ends with the next line containing
only `---` or `...`. The closing line, the opening line and every line between
them are removed, so none of it reaches the block parser. A document whose
opening line has no closing line loses everything from that line onward.
Everything outside the block renders exactly as it would without this extension.

The delimiter patterns are the ones `meta` already uses, so a line like
`--- title: Site` counts as the opening line.
"""

from __future__ import annotations

from . import Extension
from ..preprocessors import Preprocessor
import re

BEGIN_RE = re.compile(r'^-{3}(\s.*)?')
END_RE = re.compile(r'^(-{3}|\.{3})(\s.*)?')


class FrontmatterPreprocessor(Preprocessor):
    """ Remove the front matter block, if the document starts with one. """

    def run(self, lines: list[str]) -> list[str]:
        if not lines or not BEGIN_RE.match(lines[0]):
            return lines
        for index in range(1, len(lines)):
            if END_RE.match(lines[index]):
                return lines[index + 1:]
        return []


class FrontmatterExtension(Extension):
    """ Front matter extension for Python-Markdown. """

    def extendMarkdown(self, md):
        """ Register the processor.

        | Class Instance                                                              | Registry                                                      | Name           | Priority |
        | --------------------------------------------------------------------------- | ------------------------------------------------------------- | -------------- | :------: |
        | [`FrontmatterPreprocessor`][markdown.extensions.frontmatter.FrontmatterPreprocessor] | [`preprocessors`][markdown.preprocessors.build_preprocessors] | `frontmatter` | `28` |

        """
        # Priority 28 keeps the block removed before `meta` (27) ever sees it,
        # and after `normalize_whitespace` (30) has settled line endings.
        md.preprocessors.register(FrontmatterPreprocessor(md), 'frontmatter', 28)
