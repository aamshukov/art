# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol """
from art.framework.core.domain_helper import DomainHelper
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
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

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self.id}:{self.name}:{self.value}:" \
               f"({DomainHelper.dict_to_string(self.attributes)}):{self.version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self.name)
        return result

    def __eq__(self, other):
        """
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        """
        return super().__le__(other)

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

    def decorate(self, full=False):
        """
        """
        quote = "'" if self.terminal else ""
        result = f"{quote}{self.name}{quote} " \
                 f"({self.type.name}, " \
                 f"{'NULLABLE' if self.nullable else 'NON-NULLABLE'}) "
        if full:
            result = f"\n{result}\n"
            result = f"{result} FIRST: [{GrammarSymbol.sets_to_string(self.first)}]\n"
            result = f"{result} FOLLOW:[{GrammarSymbol.sets_to_string(self.follow)}]\n"
            result = f"{result} LA:    [{GrammarSymbol.sets_to_string(self.la)}]\n"
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
