#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Scope """
from art.framework.core.utils.colors import Colors
from art.framework.core.utils.flags import Flags
from art.framework.core.adt.tree.tree import Tree
from art.framework.frontend.symtable.scope.scope_kind import ScopeKind


class Scope(Tree):
    """
    """
    def __init__(self,
                 id,
                 level,
                 label='',
                 papa=None,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id,
                         label,
                         papa,
                         value,
                         attributes,
                         flags,
                         Colors.UNKNOWN,
                         version)
        self.kind = ScopeKind.UNKNOWN_SCOPE
        self.level = level  # depth
        self.symbols = dict()  # name:symbol
        self.types = dict()  # synthetic (inferred or collected) types

    def get_type(self, type):  # noqa
        """
        """
        result = None
        for value in self.types.values():
            if type.equivalent(value):
                result = value
                break
        return result

    def add_type(self, type):
        """
        """
        if type.id not in self.types:
            self.types[type.id] = type

    def next_type_uid(self):
        """
        """
        return len(self.types) + 1
