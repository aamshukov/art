# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar Tokenizer """
from art.language.art.art_tokenizer import ArtTokenizer


class GrammarTokenizer(ArtTokenizer):
    """
    """
    def __init__(self,
                 id,
                 content,
                 statistics,
                 diagnostics,
                 version='1.0'):
        """
        """
        super().__init__(id, content, statistics, diagnostics, indent_size=0, version=version)

    def epilog(self):
        """
        """
        super().epilog()
