# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Quadruple """
from art.framework.core.domain.entity import Entity
from art.framework.core.patterns.visitor.visitable import Visitable


class Quadruple(Entity, Visitable):
    """
    """
    def __init__(self,
                 id,
                 operation=None,  # operation code, OperationCode
                 argument1=None,
                 argument2=None,
                 result=None,
                 version='1.0'):
        """
        """
        super().__init__(id, version=version)
        self.operation = operation
        self.argument1 = argument1
        self.argument2 = argument2
        self.result = result

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.operation,
                     self.argument1,
                     self.argument2,
                     self.result))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other))
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other))
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other))
        else:
            result = NotImplemented
        return result

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.operation}:{self.argument1}:{self.argument2}:{self.result}"

    def accept(self, visitor, *args, **kwargs):
        """
        """
        visitor.visit(self, *args, **kwargs)
