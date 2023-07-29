# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar rule """
from art.framework.core.domain_helper import DomainHelper
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags


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

    def decorate(self):
        """
        """
        lhs = self.lhs.decorate()
        rhs = [s.decorate() for s in self.rhs]
        result = f"{lhs}  ->  {'  '.join(rhs)}"
        return result
