#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parser """
from abc import abstractmethod
from art.framework.core.base import Base


class Parser(Base):
    """
    """
    def __init__(self, context, lexical_analyzer):
        """
        """
        super().__init__()
        self._context = context  # parse context
        self._lexical_analyzer = lexical_analyzer  # master lexer, id = 0
        self._lexical_analyzers = list()  # slave lexers, might be introduced by #include(C/C++) or by import(art)

    @property
    def context(self):
        """
        """
        return self._context

    @abstractmethod
    def parse(self, visitor, *args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
