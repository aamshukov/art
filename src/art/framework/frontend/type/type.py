#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type """
from abc import abstractmethod
from art.framework.core.text.text import Text
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags
from art.framework.frontend.type.type_kind import TypeKind


class Type(Entity):
    """
    """
    def __init__(self,
                 id=0,
                 name='',
                 kind=TypeKind.UNKNOWN_TYPE,
                 value=None,
                 attributes=None,  # narrow down attributes, like REAL_TYPE:(modifier:const,parameter)
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.name = name
        self.kind = kind
        self.size = 0  # size in bits, abstract width, like C type hierarchy
        self.platform_size = 0  # size in bits, platform specific width
        self.alignment = 0  # alignment in memory, 0 no aligned, power of 2 - aligned
        self.cardinality = 0  # scalar (0), vector/1D-array(1), matrix/2D-array(2), etc.

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
        return f"{super().stringify()}:{self.name}"
