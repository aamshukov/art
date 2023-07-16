# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol """
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.frontend.grammar.grammar_symbol_associativity import GrammarSymbolAssociativity
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind


class GrammarSymbol(Entity):
    """
    """
    def __init__(self,
                 id,
                 name='',
                 symbol_type=GrammarSymbolKind.TERMINAL,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._name = name  # name (label) of the symbol
        self._type = symbol_type
        self._rules = list()  # rules this symbol belongs too, only fot non-terminals
        self._associativity = GrammarSymbolAssociativity.LEFT
        self._nullable = False  # if A ->* ε or TERMINAL
        self._flags = flags
        self._first = list()  # first set
        self._follow = list()  # follow set
        self._la = list()  # lookahead set

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._name}:{self._version}:"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self._name)
        result ^= hash(self._type)
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  Text.equal(self._name, other.name) and
                  self._type == other.type)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  Text.compare(self._name, other.name) < 0 and
                  self._type < other.type)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  Text.compare(self._name, other.name) <= 0 and
                  self._type <= other.type)
        return result

    @property
    def name(self):
        """
        """
        return self._name

    @property
    def type(self):
        """
        """
        return self._type

    @property
    def terminal(self):
        """
        """
        return self._type == GrammarSymbolKind.TERMINAL

    @property
    def non_terminal(self):
        """
        """
        return self._type == GrammarSymbolKind.NON_TERMINAL

    @property
    def rules(self):
        """
        """
        return self._rules

    @property
    def epsilon(self):
        """
        """
        return self._type == GrammarSymbolKind.EPSILON

    @property
    def associativity(self):
        """
        """
        return self._associativity

    @property
    def nullable(self):
        """
        """
        return self._nullable

    @nullable.setter
    def nullable(self, nullable):
        """
        """
        self._nullable = nullable

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

    @property
    def first(self):
        """
        """
        return self._first

    @property
    def follow(self):
        """
        """
        return self._follow

    @property
    def la(self):
        """
        """
        return self._la

    def validate(self):
        """
        """
        return True

    def decorate(self, full=False):
        """
        """
        quote = "'" if self.terminal else ""
        result = f"{quote}{self._name}{quote} " \
                 f"({self._type.name}, " \
                 f"{'NULLABLE' if self._nullable else 'NON-NULLABLE'}, " \
                 f"{self._associativity.name})"
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
            for sym in s:
                result = f'{result} {sym.name}'
            result = f'{result},'
        return result.strip(' ,')
