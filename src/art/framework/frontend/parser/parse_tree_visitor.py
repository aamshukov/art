#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree visitor """
from abc import abstractmethod
from art.framework.core.patterns.visitor.visitor import Visitor


class ParseTreeVisitor(Visitor):
    """
    """
    class TvpPair:
        __slots__ = ['tree', 'value', 'papa']

        def __init__(self, tree, value, papa):
            self.tree = tree
            self.value = value
            self.papa = papa

    def __init__(self, tree):
        """
        """
        super().__init__()
        self.tree = tree

    @abstractmethod
    def visit(self, tree, *args, **kwargs):
        """
        """
        raise NotImplemented(self.visit.__qualname__)
