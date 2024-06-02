# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol """
import os
from art.framework.core.text.text import Text
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class GrammarSymbol(Entity):
    """
    """
    def __init__(self,
                 id,
                 name='',
                 symbol_type=GrammarSymbolKind.TERMINAL,
                 token_kind=TokenKind.UNKNOWN,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.name = name  # name (label) of the symbol
        self.type = symbol_type
        self.token = token_kind
        self.rules = list()  # rules this symbol belongs too, only fot non-terminals
        self.nullable = False  # if A ->* ε or TERMINAL
        self.first = list()  # first set
        self.follow = list()  # follow set
        self.la = list()  # lookahead set

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.name))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      Text.equal(self.name, other.name))
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      Text.compare(self.name, other.name) < 0)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      Text.compare(self.name, other.name) <= 0)
        else:
            result = NotImplemented
        return result

    @property
    def terminal(self):
        """
        """
        return self.type == GrammarSymbolKind.TERMINAL

    @property
    def non_terminal(self):
        """
        """
        return self.type == GrammarSymbolKind.NON_TERMINAL

    @property
    def epsilon(self):
        """
        """
        return self.type == GrammarSymbolKind.EPSILON

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{self.name}:{self.type}:{self.token}:{super().stringify()}"

    def decorate(self, full=False):
        """
        """
        quote = "'" if self.terminal else ""
        result = f"{quote}{self.name}{quote} " \
                 f"({self.type.name}, " \
                 f"{'NULLABLE' if self.nullable else 'NON-NULLABLE'}) "
        if full:
            result = f"{os.linesep}{result}{os.linesep}"
            result = f"{result} FIRST: [{GrammarSymbol.sets_to_string(self.first)}]{os.linesep}"
            result = f"{result} FOLLOW:[{GrammarSymbol.sets_to_string(self.follow)}]{os.linesep}"
            result = f"{result} LA:    [{GrammarSymbol.sets_to_string(self.la)}]{os.linesep}"
        return result

    @staticmethod
    def sets_to_string(sets):
        """
        """
        result = ''
        for s in sets:
            sr = ''
            for sym in s:
                sr += f' {sym.name}'
            sr = f'{{{sr.strip()}}}'
            result = f'{result}, {sr}'
        return result.strip(' ,')
