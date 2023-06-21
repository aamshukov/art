#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token """
from art.framework.core.value import Value
from art.framework.core.flags import Flags
from art.framework.frontend.token.token_kind import TokenKind


class Token(Value):
    """
    """
    def __init__(self, kind, source='', version='1.0'):
        """
        """
        super().__init__(version)
        self._kind = kind  # type of lexeme
        self._offset = 0  # offset in context (absolute address)
        self._length = 0  # length of lexeme
        self._literal = ''  # string or char literal (if unicode - always decoded), numeric value, etc.
        self._source = source  # lexical analyser which recognizes this lexeme, could be from different files
        self._flags = Flags.CLEAR | Flags.GENUINE

    def __repr__(self):
        """
        """
        return f"{self._kind.name.ljust(16)}: '{self._literal}', {self._offset}," \
               f"{self._length}, '{self._source}', {self._flags}, {self.version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = (super().__hash__() ^
                  hash(self._kind) ^
                  hash(self._offset) ^
                  hash(self._length) ^
                  hash(self._literal) ^
                  hash(self._source))
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self._kind == other.kind and
                  self._offset == other.offset and
                  self._length == other.length and
                  self._literal == other.literal and
                  self._source == other.source)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._kind < other.kind and
                  self._offset < other.offset and
                  self._length < other.length and
                  self._literal < other.literal and
                  self._source < other.source)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._kind <= other.kind and
                  self._offset <= other.offset and
                  self._length <= other.length and
                  self._literal <= other.literal and
                  self._source <= other.source)
        return result

    @property
    def kind(self):
        """
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        """
        self._kind = kind

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

    @offset.setter
    def offset(self, offset):
        """
        """
        self._offset = offset

    @property
    def length(self):
        """
        """
        return self._length

    @length.setter
    def length(self, length):
        """
        """
        self._length = length

    @property
    def literal(self):
        """
        """
        return self._literal

    @literal.setter
    def literal(self, literal):
        """
        """
        self._literal = literal

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

    def validate(self):
        """
        """
        return True

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
        self._offset = 0
        self._length = 0
        self._literal = ''
        self._source = ''
        self._flags = Flags.CLEAR | Flags.GENUINE
