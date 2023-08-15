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
        self.max_recursion_level = 0

    def inc_recursion_level(self):
        """
        """
        self.recursion_level += 1
        if self.recursion_level > self.max_recursion_level:
            self.max_recursion_level = self.recursion_level
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

    @staticmethod
    def build_recovery_synch_set(recovery_tokens,
                                 firsts,
                                 follows):
        """
        A -> α β
        SYNCH(A):
            1. a ∈ FOLLOW(A) => a ∈ SYNCH(A)
            2. place keywords that start statements in SYNCH(A)
            3. add symbols in FIRST(A) to SYNCH(A)
            https://matklad.github.io/2023/05/21/resilient-ll-parsing-tutorial.html
            ... also recursively include ancestor's FOLLOW sets into the recovery set
        """
        result = recovery_tokens
        for first in firsts:
            result += [item.name for sublist in first for item in sublist]
        for follow in follows:
            result += [item.name for sublist in follow for item in sublist]
        result = list(set(result))
        return sorted(result)
