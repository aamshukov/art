#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art type parameter """
from art.framework.core.utils.flags import Flags
from art.language.art.type.art_type import ArtType
from art.language.art.type.art_type_kind import ArtTypeKind


class ArtTypeParameter(ArtType):
    """
    """
    def __init__(self,
                 id,
                 label,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         kind=ArtTypeKind.TYPE_PARAMETER,
                         cardinality=0,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)

    def equivalent(self, other):
        """
        """
        return super().equivalent(other)
