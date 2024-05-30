#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type """
from abc import abstractmethod
from art.framework.core.adt.tree.tree import Tree
from art.framework.core.utils.flags import Flags


class Type(Tree):
    """
    """
    def __init__(self,
                 id,
                 label,
                 kind,
                 cardinality=0,
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
        self.alignment = 0  # alignment in memory, 0 no aligned, power of 2 - aligned
        self.abstract_size = 0  # size in bits, abstract width, like C type hierarchy
        self.platform_size = 0  # size in bits, platform specific width

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.kind, self.cardinality))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other) and self.kind == other.kind and self.cardinality == other.cardinality
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__lt__(other)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__le__(other)
        else:
            result = NotImplemented
        return result

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
        return f"{super().stringify()}:{self.kind}:{self.cardinality}"
