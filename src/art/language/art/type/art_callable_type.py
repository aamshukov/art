#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art callable type """
from abc import abstractmethod
from art.framework.core.utils.flags import Flags
from art.framework.frontend.type.type_kind import TypeKind
from art.language.art.type.art_type import ArtType


class ArtCallableType(ArtType):
    """
    """
    def __init__(self,
                 id=0,
                 name='',
                 kind=TypeKind.UNKNOWN_TYPE,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, name, kind, value, attributes, flags, version)

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
        return f"{super().stringify()}"
