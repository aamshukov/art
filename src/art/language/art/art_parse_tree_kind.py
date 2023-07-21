#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parse tree kinds """
from enum import IntEnum, auto


class ArtParseTreeKind(IntEnum):
    """
    """
    UNKNOWN = auto()
    INDENT = auto()
    DEDENT = auto()
    TERMINAL = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    FULLY_QUALIFIED_IDENTIFIER = auto()
    EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    NON_ASSIGNMENT_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    CONDITIONAL_OR_EXPRESSION = auto()
    ASSIGNMENT_OPERATOR = auto()
