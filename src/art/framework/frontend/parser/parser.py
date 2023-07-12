#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parser """
from abc import abstractmethod
from art.framework.core.base import Base
from art.framework.core.status import Status


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
        self._context = context  # parse context
        self._lexical_analyzer = lexical_analyzer  # master lexer, id = 0
        self._lexical_analyzers = list()  # slave lexers, might be introduced by #include(C/C++) or by import(art)
        self._grammar = grammar
        self._statistics = statistics
        self._diagnostics = diagnostics

    @property
    def context(self):
        """
        """
        return self._context

    @property
    def lexical_analyzer(self):
        """
        """
        return self._lexical_analyzer

    @property
    def grammar(self):
        """
        """
        return self._grammar

    @property
    def statistics(self):
        """
        """
        return self._statistics

    @property
    def diagnostics(self):
        """
        """
        return self._diagnostics

    def accept(self, token_kind):
        """
        """
        if self._lexical_analyzer.token.kind == token_kind:
            result = True
            self._lexical_analyzer.next_lexeme()
        else:
            result = False
            self._diagnostics.add(Status(f'Expected token {token_kind.name}, mismatch occurred at '
                                         f'{self._lexical_analyzer.get_content_position()}',
                                         'parser',
                                         Status.INVALID_TOKEN))
        return result

    @abstractmethod
    def parse(self,*args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
