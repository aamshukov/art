#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Syntax token trivia """
from art.framework.core.domain.value import Value


class TokenTrivia(Value):
    """
    """
    def __init__(self,
                 token,
                 version='1.0'):
        """
        Might be one of WS, EOL, EOS, INDENT, DEDENT, SINGLE_LINE_COMMENT, MULTI_LINE_COMMENT
        """
        super().__init__(version=version)
        self.token = token

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.token))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.token == other.token)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      self.token < other.token)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      self.token <= other.token)
        else:
            result = NotImplemented
        return result

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.token}"
