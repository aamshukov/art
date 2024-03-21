# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" FSA status """
from art.framework.core.adt.graph.vertex import Vertex
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

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__lt__(other)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__le__(other)
        else:
            result = NotImplemented
        return result

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
