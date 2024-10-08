#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art scalar type """
from art.framework.core.utils.flags import Flags
from art.language.art.type.art_type import ArtType
from art.language.art.type.art_type_kind import ArtTypeKind


class ArtScalarType(ArtType):
    """
    """
    def __init__(self,
                 id,
                 label,
                 kind,
                 layout=None,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         kind=kind | ArtTypeKind.SCALAR_MASK,
                         cardinality=0,
                         layout=layout,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)

    def equivalent(self, other):
        """
        """
        return ArtTypeKind.scalar(other.kind) and super().equivalent(other)
