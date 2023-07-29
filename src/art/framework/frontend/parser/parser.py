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
    def __init__(self,
                 context,
                 lexical_analyzer,
                 grammar,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__()
        self.context = context  # parse context
        self.lexical_analyzer = lexical_analyzer  # master lexer, id = 0
        self.lexical_analyzers = list()  # slave lexers, might be introduced by #include(C/C++) or by import(art)
        self.grammar = grammar
        self.statistics = statistics
        self.diagnostics = diagnostics

    @abstractmethod
    def parse(self,*args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
