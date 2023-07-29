#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Recursive descent parser """
from abc import abstractmethod
from art.framework.frontend.parser.parser import Parser


class RecursiveDescentParser(Parser):
    """
    """
    def __init__(self,
                 context,
                 lexical_analyzer,
                 grammar,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__(context,
                         lexical_analyzer,
                         grammar,
                         statistics,
                         diagnostics)
        self.recursion_level = 0

    def inc_recursion_level(self):
        """
        """
        self.recursion_level += 1
        return self.recursion_level

    def dec_recursion_level(self):
        """
        """
        self.recursion_level -= 1
        assert self.recursion_level >= 0, f"Internal parser error. Recursion level: {self.recursion_level}."
        return self.recursion_level

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
