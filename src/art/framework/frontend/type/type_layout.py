#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type layout """
from art.framework.core.domain.value import Value


class TypeLayout(Value):
    """
    """
    def __init__(self,
                 alignment=0,
                 abstract_size=0,
                 platform_size=0,
                 value=None,
                 version='1.0'):
        """
        """
        super().__init__(value=value, version=version)
        self.alignment = alignment  # alignment in memory, 0 no aligned, power of 2 - aligned
        self.abstract_size = abstract_size  # size in bits, abstract width, like C type hierarchy
        self.platform_size = platform_size  # size in bits, platform specific width

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.alignment,
                     self.abstract_size,
                     self.platform_size))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.alignment == other.alignment and
                      self.abstract_size == other.abstract_size and
                      self.platform_size == other.platform_size)
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

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.alignment}:{self.abstract_size}:{self.platform_size}"
