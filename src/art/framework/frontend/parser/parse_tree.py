#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from art.framework.core.text.text import Text
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

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.label))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      Text.equal(self.label, other.label))
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      Text.compare(self.label, other.label) < 0)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      Text.compare(self.label, other.label) <= 0)
        else:
            result = NotImplemented
        return result

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
