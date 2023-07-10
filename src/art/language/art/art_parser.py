#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from abc import abstractmethod
from art.framework.frontend.parser.recursive_descent_parser import RecursiveDescentParser


class ArtParser(RecursiveDescentParser):
    """
    """
    def __init__(self, context, lexical_analyzer):
        """
        """
        super().__init__(context, lexical_analyzer)

    def parse(self, visitor, *args, **kwargs):
        """
        """
        pass
