# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar rule """
from art.framework.core.entity import Entity
from art.framework.core.text import Text


class GrammarRule(Entity):
    """
    Context Free Grammar rule:
        LHS -> RHS
        LHS: NonTerminal
        RHS -> (NonTerminal | Terminal)+
    """
    def __init__(self,
                 id,
                 name='',
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._name = name
        self._lhs = None
        self._rhs = list()

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
                  Text.equal(self._name, other.label))
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  Text.compare(self._name, other.label) < 0)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  Text.compare(self._name, other.label) <= 0)
        return result

    @property
    def name(self):
        """
        """
        return self._name

    @property
    def lhs(self):
        """
        """
        return self._lhs

    @lhs.setter
    def lhs(self, lhs):
        """
        """
        self._lhs = lhs

    @property
    def rhs(self):
        """
        """
        return self._rhs

    def empty(self):
        """
        """
        assert self._lhs, 'LHS must not be empty.'
        assert self._rhs, 'RHS must not be empty.'
        return (self._lhs and
                self._lhs.non_terminal and
                self._rhs and
                Text.epsilon(self._rhs[0]))

    def validate(self):
        """
        """
        return True

    def decorate(self):
        """
        """
        lhs = self._lhs.decorate()
        rhs = [s.decorate() for s in self._rhs]
        result = f"{lhs}  ->  {'  '.join(rhs)}"
        return result
