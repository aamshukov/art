#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree  """
from art.framework.core.tree import Tree
from art.framework.core.visitable import Visitable
from art.framework.frontend.parser.parse_tree_mixin import ParseTreeMixin


class ParseTree(Tree, ParseTreeMixin, Visitable):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    def accept(self, visitor, *args, **kwargs):
        """
        """
        pass
