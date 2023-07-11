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
                 statistics,
                 diagnostics):
        """
        """
        super().__init__()
        self._context = context  # parse context
        self._lexical_analyzer = lexical_analyzer  # master lexer, id = 0
        self._lexical_analyzers = list()  # slave lexers, might be introduced by #include(C/C++) or by import(art)
        self._statistics = statistics
        self._diagnostics = diagnostics

    @property
    def context(self):
        """
        """
        return self._context

    def accept(self, token_kind, lexical_analyzer=None):
        """
        """
        lexer = lexical_analyzer if lexical_analyzer else self._lexical_analyzer
        if lexer.token.kind == token_kind:
            lexer.next_lexeme()
        else:
            self._diagnostics.add(Status(f'Invalid token {token_kind.name} occurred at '
                                         f'{lexer.get_content_position()}',
                                         'parser',
                                         Status.INVALID_TOKEN))

    @abstractmethod
    def parse(self,*args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
