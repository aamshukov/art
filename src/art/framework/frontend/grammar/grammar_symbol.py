# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol """
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.frontend.grammar.grammar_symbol_associativity import GrammarSymbolAssociativity
from art.framework.frontend.grammar.grammar_symbol_type import GrammarSymbolType


class GrammarSymbol(Entity):
    """
    """
    def __init__(self,
                 id,
                 name='',
                 symbol_type=GrammarSymbolType.TERMINAL,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._name = name  # name (label) of the symbol
        self._type = symbol_type
        self._associativity = GrammarSymbolAssociativity.LEFT
        self._nullable = False  # if A ->* ε or TERMINAL
        self._flags = flags
        self._first_set = list()  # first set for k = 1
        self._follow_set = list()  # first set for k = 1
        self._first_set2 = list()  # first set for k = 2
        self._follow2_set = list()  # first set for k = 1
        self._la_set = list()  # lookahead set for k = 1
        self._la2_set = list()  # lookahead set for k = 2

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
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  Text.equal(self._name, other.name))
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  Text.compare(self._name, other.name) < 0)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  Text.compare(self._name, other.name) <= 0)
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
        return self._type == GrammarSymbolType.TERMINAL

    @property
    def non_terminal(self):
        """
        """
        return self._type == GrammarSymbolType.NON_TERMINAL

    @property
    def epsilon(self):
        """
        """
        return self._type == GrammarSymbolType.EPSILON

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
    def la(self):
        """
        """
        return self._la_set

    @property
    def la2(self):
        """
        """
        return self._la2_set

    def validate(self):
        """
        """
        return True

    def decorate(self):
        """
        """
        quote = "'" if self.terminal else ""
        result = f"{quote}{self._name}{quote} ({self._type.name}, {'NULLABLE' if self._nullable else 'NON-NULLABLE'})"
        return result
