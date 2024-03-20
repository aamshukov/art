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

    @abstractmethod
    def equivalent(self, other):
        """
        """
        raise NotImplemented(self.equivalent.__qualname__)
