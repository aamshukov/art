#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art declaration """
from art.framework.core.utils.flags import Flags
from art.framework.frontend.declaration.decl import Decl


class ArtDecl(Decl):
    """
    """
    def __init__(self,
                 id,
                 label,
                 kind,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         kind=kind,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)

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
