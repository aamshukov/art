#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art enum member declaration """
from art.framework.core.utils.flags import Flags
from art.language.art.declaration.art_decl import ArtDecl
from art.language.art.declaration.art_decl_kind import ArtDeclKind
from art.language.art.type.art_type_kind import ArtTypeKind


class ArtEnumMemberDecl(ArtDecl):
    """
    label value of type
    """
    def __init__(self,
                 id,
                 label,
                 value,
                 type,  # noqa
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         kind=ArtDeclKind.ENUM_MEMBER_DECL,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)
        self.type = type

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.type))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and self.type == other.type)
        else:
            result = NotImplemented
        return result

    def validate(self):
        """
        """
        return (ArtTypeKind.scalar(self.type.kind) and
                (ArtTypeKind.integer(self.type.kind) or
                 ArtTypeKind.real(self.type.kind) or
                 ArtTypeKind.string(self.type.kind) or
                 ArtTypeKind.boolean(self.type.kind)))

    def stringify(self):
        """
        """
        return f"{self.type}:{super().stringify()}"
