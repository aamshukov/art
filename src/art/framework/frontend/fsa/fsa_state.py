# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" FSA status """
from art.framework.core.vertex import Vertex
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class FsaState(Vertex):
    """
    """
    def __init__(self,
                 id,
                 label='',
                 token=TokenKind.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id, label, token, version=version)

    @property
    def token(self):
        """
        """
        return self.value

    @property
    def transitions(self):
        """
        """
        return self.edges
