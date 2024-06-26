#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Operator precedence parser """
from abc import abstractmethod
from collections import namedtuple
from art.framework.frontend.parser.parser import Parser


class OperatorPrecedenceParser(Parser):
    """
    """
    OperatorInfo = namedtuple('OperatorInfo', 'precedence associativity')

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
