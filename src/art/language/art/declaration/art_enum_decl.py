#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art enum declaration """
from art.framework.core.utils.flags import Flags
from art.language.art.declaration.art_decl import ArtDecl
from art.language.art.declaration.art_decl_kind import ArtDeclKind


class ArtEnumDecl(ArtDecl):
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
                         kind=ArtDeclKind.ENUM_DECL,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)
        self.members = list()  # list of ArtEnumMemberDecl

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

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.members}"
