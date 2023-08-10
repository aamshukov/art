# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context Free Grammar """
import os
from abc import abstractmethod
from functools import lru_cache
from art.framework.core.base import Base
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.grammar.grammar_symbol_factory import GrammarSymbolFactory


class Grammar(Base):
    """
    Context Free Grammar
    """
    def __init__(self, name='', logger=None):
        """
        """
        super().__init__()
        self.name = name
        self.logger = logger
        self.rules = list()
        self.pool = dict()  # name:symbol mapping
        self.pool['ε'] = GrammarSymbolFactory.epsilon_symbol()
        self.pool['λ'] = GrammarSymbolFactory.epsilon_symbol()
        self.pool[GrammarSymbolFactory.ERRONEOUS_SYMBOL.name] = GrammarSymbolFactory.erroneous_symbol()
        self.pool[GrammarSymbolFactory.UNKNOWN_SYMBOL.name] = GrammarSymbolFactory.unknown_symbol()

    @property
    @lru_cache
    def start(self):
        """
        Return start symbol of the grammar.
        """
        assert self.rules, 'Rules must not be empty.'
        return self.rules[0].lhs

    @property
    def epsilon(self):
        """
        """
        return self.pool['ε']

    @abstractmethod
    def load(self, data_provider):
        """
        """
        raise NotImplemented(self.load.__qualname__)

    def decorate(self):
        """
        """
        result = ""
        lhs = GrammarSymbol(0, '')
        for rule in self.rules:
            if lhs != rule.lhs:
                lhs = rule.lhs
                result += '\n'
            result += f'{rule.decorate()}\n'
        return result

    def decorate_pool(self):
        """
        """
        result = ""
        for symbol in self.pool.values():
            result = f'{result}{symbol.decorate(full=True)}\n'
        return result
