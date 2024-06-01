#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Declaration """
from art.framework.core.adt.tree.tree import Tree
from art.framework.core.utils.flags import Flags


class Decl(Tree):
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
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)
        self.kind = kind

    def __hash__(self):
        """
        """
        return hash((super().__hash__(),
                     self.__class__,
                     self.kind))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      self.kind == other.kind)
        else:
            result = NotImplemented
        return result

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.kind}"
