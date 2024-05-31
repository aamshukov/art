#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art enum declaration """
from art.language.art.declaration.art_decl import ArtDecl


class ArtEnumDecl(ArtDecl):
    """
    """
    def __init__(self,
                 label,
                 value,
                 version='1.0'):
        """
        """
        super().__init__(value=value, version=version)
        self.label = label
