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
    def __init__(self, context, lexical_analyzer):
        """
        """
        super().__init__(context, lexical_analyzer)

    @abstractmethod
    def parse(self, visitor, *args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
