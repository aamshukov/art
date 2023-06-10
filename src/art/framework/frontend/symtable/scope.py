#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Scope """
from art.framework.core.tree import Tree
from art.framework.frontend.symtable.scope_kind import ScopeKind


class Scope(Tree):
    """
    """
    def __init__(self, id, level, version='1.0'):
        """
        """
        super().__init__(id, version)
        self._kind = ScopeKind.UNKNOWN_SCOPE
        self._level = level  # depth
        self._symbols = dict()  # name:symbol
        self._types = dict()  # synthetic (introduced) types

    @property
    def kind(self):
        """
        """
        return self._kind

    @property
    def level(self):
        """
        """
        return self._level

    @property
    def symbols(self):
        """
        """
        return self._symbols
