#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Depth First Search () DFS visitor """
from abc import abstractmethod
from art.framework.core.patterns.visitor.visitor import Visitor


class GraphVisitor(Visitor):
    """
    """
    def __init__(self, graph):
        """
        """
        super().__init__()
        self.graph = graph

    @abstractmethod
    def visit(self, vertex, *args, **kwargs):
        """
        """
        raise NotImplemented(self.visit.__qualname__)
