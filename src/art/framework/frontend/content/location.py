#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Location """
from art.framework.core.domain.base import Base
from art.framework.core.text.text import Text


class Location(Base):
    """
    """
    def __init__(self,
                 offset,
                 length,
                 source):
        """
        """
        super().__init__()
        self.offset = offset    # offset in context (absolute address)
        self.length = length    # length of lexeme
        self.source = source    # lexical analyser which recognizes this lexeme,
                                # could be from different files,  file path, DB schema, etc.

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.offset,
                     self.length,
                     self.source))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (self.offset == other.offset and
                      self.length == other.length and
                      Text.equal(self.source, other.source))
        else:
            result = NotImplemented
        return result

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.offset}:{self.length}:{self.source}"
