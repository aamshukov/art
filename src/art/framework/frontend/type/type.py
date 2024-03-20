#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type """
from abc import abstractmethod
from art.framework.core.utils.helper import DomainHelper
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

    @abstractmethod
    def equivalent(self, other):
        """
        """
        raise NotImplemented(self.equivalent.__qualname__)
