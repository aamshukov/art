#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from art.framework.core.utils.colors import Colors
from art.framework.core.utils.flags import Flags
from art.framework.core.adt.tree.tree import Tree


class ParseTree(Tree):
    """
    """
    def __init__(self,
                 id,
                 kind,
                 label='',
                 papa=None,
                 value=None,  # IR backend symbol
                 attributes=None,
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id,
                         label,
                         papa,
                         value,
                         attributes,
                         flags,
                         color,
                         version)
        self.kind = kind

    @property
    def symbol(self):
        """
        """
        return self.value

    @symbol.setter
    def symbol(self, symbol):
        """
        """
        self.value = symbol

    def validate(self):
        """
        """
        return True

    def accept(self, visitor, *args, **kwargs):
        """
        """
        visitor.visit(self, *args, **kwargs)
