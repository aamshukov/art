#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token """
from abc import abstractmethod
from art.framework.core.value import Value
from art.framework.core.flags import Flags
from art.framework.frontend.token.token_kind import TokenKind


class Token(Value):
    """
    """

    def __init__(self, kind, source=None, version='1.0'):
        """
        """
        super().__init__(version)
        self._kind = kind  # type of lexeme
        self._offset = -1  # offset in context (absolute address)
        self._length = 0  # length of lexeme
        self._literal = ''  # string or char literal (if unicode - always decoded), numeric value
        self._source = source  # lexical analyser which recognizes this lexeme, could be from different files
        self._flags = Flags.CLEAR | Flags.GENUINE

    @abstractmethod
    def __hash__(self):
        """
        """
        result = super().__hash__() ^ hash(self._kind.value)
        return result

    @abstractmethod
    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self._kind.value == other.kind.value)
        return result

    @abstractmethod
    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._kind.value < other.kind.value)
        return result

    @abstractmethod
    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._kind.value <= other.kind.value)
        return result

    def validate(self):
        """
        """
        pass

    @property
    def kind(self):
        """
        """
        return self._kind

    @property
    def name(self):
        """
        """
        return self._kind.name

    @property
    def offset(self):
        """
        """
        return self._offset

    @property
    def length(self):
        """
        """
        return self._length

    @property
    def literal(self):
        """
        """
        return self._literal

    @property
    def source(self):
        """
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        """
        self._source = source

    @property
    def flags(self):
        """
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        """
        self._flags = flags

    def accept(self, token):
        """
        """
        self._kind = token.kind
        self._offset = token.offset
        self._length = token.length
        self._literal = token.literal
        self._source = token.source
        self._flags = token.flags

    def reset(self):
        """
        """
        self._kind = TokenKind.UNKNOWN
        self._offset = -1
        self._length = 0
        self._literal = ''
        self._source = None
        self._flags = Flags.CLEAR | Flags.GENUINE
