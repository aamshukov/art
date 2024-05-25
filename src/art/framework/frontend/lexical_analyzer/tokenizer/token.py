#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token """
from art.framework.core.text.text import Text
from art.framework.core.domain.value import Value
from art.framework.core.utils.flags import Flags
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class Token(Value):
    """
    """
    def __init__(self,
                 kind,
                 source='',
                 value=0,
                 version='1.0'):
        """
        """
        super().__init__(value, version)
        self.kind = kind  # type of lexeme
        self.offset = 0  # offset in context (absolute address)
        self.length = 0  # length of lexeme
        self.literal = ''  # string or char literal (if unicode - always decoded), numeric value, etc.
        self.source = source  # lexical analyser which recognizes this lexeme, could be from different files
        self.flags = Flags.CLEAR | Flags.GENUINE
        self.leading_trivia = list()
        self.trailing_trivia = list()

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.kind,
                     self.offset,
                     self.length,
                     self.literal,
                     self.value,
                     self.source))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.kind == other.kind and
                      self.offset == other.offset and
                      self.length == other.length and
                      Text.equal(self.literal, other.literal) and
                      self.value == other.value and
                      self.source == other.source)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      self.kind < other.kind and
                      self.offset < other.offset and
                      self.length < other.length and
                      Text.compare(self.literal, other.literal) < 0 and
                      self.value < other.value and
                      self.source < other.source)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      self.kind <= other.kind and
                      self.offset <= other.offset and
                      self.length <= other.length and
                      Text.compare(self.literal, other.literal) <= 0 and
                      self.value <= other.value and
                      self.source <= other.source)
        else:
            result = NotImplemented
        return result

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
        return f"{super().stringify()}:{self.kind.name.ljust(16)}: '{self.literal}', '{self.value}'," \
               f"{self.offset}, {self.length}, '{self.source}', {self.flags}"

    def accept(self, token):
        """
        """
        self.kind = token.kind
        self.offset = token.offset
        self.length = token.length
        self.literal = token.literal
        self.value = token.value
        self.source = token.source
        self.flags = token.flags

    def reset(self):
        """
        """
        self.kind = TokenKind.UNKNOWN
        self.offset = 0
        self.length = 0
        self.literal = ''
        self.value = 0
        self.source = ''
        self.flags = Flags.CLEAR | Flags.GENUINE
