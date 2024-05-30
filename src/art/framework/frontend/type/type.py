#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type """
from abc import abstractmethod
from art.framework.core.adt.tree.tree import Tree
from art.framework.core.utils.flags import Flags
from art.framework.frontend.type.type_layout import TypeLayout


class Type(Tree):
    """
    """
    def __init__(self,
                 id,
                 label,
                 kind,
                 cardinality=0,
                 layout=None,
                 value=None,
                 attributes=None,  # narrow down attributes, like REAL_TYPE:(modifier:const,parameter)
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)
        self.kind = kind
        self.cardinality = cardinality  # scalar (0), vector/1D-array(1), matrix/2D-array(2), etc.
        self.layout = layout if layout is not None else TypeLayout(version=version)

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.kind,
                     self.cardinality,
                     self.layout))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.kind == other.kind and
                      self.cardinality == other.cardinality and
                      self.layout == other.layout)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        raise NotImplemented(self.__lt__.__qualname__)

    def __le__(self, other):
        """
        """
        raise NotImplemented(self.__le__.__qualname__)

    @abstractmethod
    def equivalent(self, other):
        """
        """
        raise NotImplemented(self.equivalent.__qualname__)

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.kind}:{self.cardinality}:{self.layout}"
