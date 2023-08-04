#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol factory """
from copy import deepcopy
from art.framework.core.base import Base
from art.framework.core.flags import Flags
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class GrammarSymbolFactory(Base):
    """
    """
    id_generator = 0

    UNKNOWN_SYMBOL = GrammarSymbol(id_generator,
                                   GrammarSymbolKind.UNKNOWN.name,
                                   GrammarSymbolKind.UNKNOWN,
                                   TokenKind.UNKNOWN)
    EPSILON_SYMBOL = GrammarSymbol(int(GrammarSymbolKind.EPSILON),
                                   'ε',
                                   GrammarSymbolKind.EPSILON,
                                   TokenKind.EPSILON)
    ERRONEOUS_SYMBOL = GrammarSymbol(-1,
                                     TokenKind.ERRONEOUS.name,
                                     GrammarSymbolKind.NON_TERMINAL,
                                     TokenKind.ERRONEOUS)

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def get_next_id():
        """
        """
        GrammarSymbolFactory.id_generator += 1
        return GrammarSymbolFactory.id_generator

    @staticmethod
    def create(name='',
               symbol_type=GrammarSymbolKind.TERMINAL,
               token_kind=TokenKind.UNKNOWN,
               value=None,
               attributes=None,
               flags=Flags.CLEAR,
               version='1.0'):
        """
        """
        return GrammarSymbol(GrammarSymbolFactory.get_next_id(),
                             name,
                             symbol_type,
                             token_kind,
                             value,
                             attributes,
                             flags,
                             version)

    @staticmethod
    def unknown_symbol():
        """
        """
        return deepcopy(GrammarSymbolFactory.UNKNOWN_SYMBOL)

    @staticmethod
    def epsilon_symbol():
        """
        """
        return deepcopy(GrammarSymbolFactory.EPSILON_SYMBOL)

    @staticmethod
    def erroneous_symbol():
        """
        """
        return deepcopy(GrammarSymbolFactory.ERRONEOUS_SYMBOL)
