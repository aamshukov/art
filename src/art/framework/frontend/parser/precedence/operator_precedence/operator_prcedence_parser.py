#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Operator precedence parser """
from enum import IntEnum
from abc import abstractmethod
from art.framework.frontend.parser.parser import Parser


class OperatorPrecedenceParser(Parser):
    """
    """
    class PrecedenceKind(IntEnum):
        """
        """
        UNKNOWN_RELATION = 0,
        LESS_RELATION = 1,    # ⋖, op1 has higher precedence than op2
        EQUAL_RELATION = 2,   # ≗, op1 an op2 have the same precedence
        GREATER_RELATION = 3  # ⋗, op1 has lower precedence than op2

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

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
