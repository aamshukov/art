#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token """
from art.framework.core.text.text import Text
from art.framework.core.domain.value import Value
from art.framework.core.utils.flags import Flags
from art.framework.frontend.content.location import Location
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class Token(Value):
    """
    """
    def __init__(self,
                 kind,
                 location=None,
                 value=None,
                 version='1.0'):
        """
        """
        super().__init__(value, version)
        self.kind = kind  # type of lexeme
        self.literal = ''  # string or char literal (if unicode - always decoded), numeric value, etc.
        self.location = location if location is not None else Location(0, 0, '')
        self.flags = Flags.CLEAR | Flags.GENUINE
        self.leading_trivia = list()
        self.trailing_trivia = list()

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.kind,
                     self.literal,
                     self.location,
                     self.value))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.kind == other.kind and
                      Text.equal(self.literal, other.literal) and
                      self.location == other.location and
                      self.value == other.value)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        raise NotImplemented(self.__lt__.__qualname__)

    def __le__(self, other):
        """
        """
        raise NotImplemented(self.__le__.__qualname__)

    @property
    def label(self):
        """
        """
        return self.kind.name

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.kind.name.ljust(16)}: '{self.literal}', '{self.location}', {self.flags}"

    def accept(self, token):
        """
        """
        self.kind = token.kind
        self.literal = token.literal
        self.location = token.location
        self.value = token.value
        self.flags = token.flags

    def reset(self):
        """
        """
        self.kind = TokenKind.UNKNOWN
        self.literal = ''
        self.location = Location(0, 0, '')
        self.value = 0
        self.flags = Flags.CLEAR | Flags.GENUINE
