#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from art.framework.core.colors import Colors
from art.framework.core.flags import Flags
from art.framework.core.tree import Tree
from art.framework.core.visitable import Visitable
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind


class ParseTree(Tree, Visitable):
    """
    """
    def __init__(self,
                 id,
                 kind=ParseTreeKind.UNKNOWN,
                 label='',
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 papa=None,
                 version='1.0'):
        """
        """
        super().__init__(id,
                         label,
                         value,
                         attributes,
                         flags,
                         color,
                         papa,
                         version)
        self._kind = kind
        self._symbol = None  # IR backend symbol

    @property
    def kind(self):
        """
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        """
        self._kind = kind

    @property
    def symbol(self):
        """
        """
        return self._symbol

    @symbol.setter
    def symbol(self, symbol):
        """
        """
        self._symbol = symbol

    def accept(self, visitor, *args, **kwargs):
        """
        """
        super().accept(visitor, *args, **kwargs)
