# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar rule """
from art.framework.core.text.text import Text
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags


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
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.name = name
        self.lhs = None
        self.rhs = list()

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

    def empty(self):
        """
        """
        assert self.lhs, 'LHS must not be empty.'
        assert self.rhs, 'RHS must not be empty.'
        return (self.lhs and
                self.lhs.non_terminal and
                self.rhs and
                self.rhs[0].epsilon)

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.name}:{self.decorate()}"

    def decorate(self):
        """
        """
        lhs = self.lhs.decorate()
        rhs = [s.decorate() for s in self.rhs]
        result = f"{lhs}  ->  {'  '.join(rhs)}"
        return result
