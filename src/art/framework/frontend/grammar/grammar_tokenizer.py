# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar Tokenizer """
from art.framework.core.flags import Flags
from art.language.art.parser.art_tokenizer import ArtTokenizer


class GrammarTokenizer(ArtTokenizer):
    """
    """
    def __init__(self,
                 id,
                 content,
                 statistics,
                 diagnostics,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id,
                         content,
                         statistics,
                         diagnostics,
                         indent_size=0,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)

    def epilog(self):
        """
        """
        super().epilog()
