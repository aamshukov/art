#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from art.framework.frontend.parser.backtracking.\
    recursive_descent.recursive_descent_parser import RecursiveDescentParser


class ArtParser(RecursiveDescentParser):
    """
    """
    def __init__(self, context, lexical_analyzer):
        """
        """
        super().__init__(context, lexical_analyzer)

    def parse(self, *args, **kwargs):
        """
        """
        pass
