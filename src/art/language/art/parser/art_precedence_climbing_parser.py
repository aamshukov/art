#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art precedence climbing parser """
from art.framework.frontend.parser.precedence.precedence_climbing_pratt.pratt_parser import \
    PrattParser


class ArtPrecedenceClimbingParser(PrattParser):
    """
    """
    def __init__(self,
                 operators,
                 context,
                 lexical_analyzer,
                 grammar,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__(operators,
                         context,
                         lexical_analyzer,
                         grammar,
                         statistics,
                         diagnostics)

    def parse(self, *args, **kwargs):
        """
        """
        pass
