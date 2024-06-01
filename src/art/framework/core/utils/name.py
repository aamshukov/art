#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Declaration name """
from art.framework.core.utils.flags import Flags
from art.framework.core.domain.value import Value


class Name(Value):
    """
    """
    def __init__(self,
                 name,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(name, version)
        self.flags = flags

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other)
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

    @property
    def name(self):
        """
        """
        return self.value

    def validate(self):
        """
        """
        return self.value is not None

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.flags}"
