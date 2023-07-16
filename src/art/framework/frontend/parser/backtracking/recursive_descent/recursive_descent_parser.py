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

    @abstractmethod
    def skip_tokens(self, *args, **kwargs):
        """
        Panic mode error recovery help routine.
        Skip input tokens until a stop token is found.
        """
        raise NotImplemented(self.skip_tokens.__qualname__)

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.parse.__qualname__)
