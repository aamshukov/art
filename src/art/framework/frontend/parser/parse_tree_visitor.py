#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree visitor """
from abc import abstractmethod
from art.framework.core.visitor import Visitor


class ParseTreeVisitor(Visitor):
    """
    """
    def __init__(self, tree):
        """
        """
        super().__init__()
        self.tree = tree

    def __repr__(self):
        return self.__class__.__name__

    __str__ = __repr__

    @abstractmethod
    def visit(self, tree, *args, **kwargs):
        """
        """
        raise NotImplemented(self.visit.__qualname__)
