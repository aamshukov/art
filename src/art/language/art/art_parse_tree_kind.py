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
    UNARY_EXPRESSION = auto()
    CONDITIONAL_OR_EXPRESSION = auto()
    ASSIGNMENT_OPERATOR = auto()
    ARRAY_MODIFIERS = auto()
    ARRAY_BOUND_EXPRESSION = auto()
    ARRAY_LOWER_BOUND = auto()
    ARRAY_UPPER_BOUND = auto()
    ARRAY_DIMENSION = auto()
    ARRAY_DIMENSIONS = auto()
    ARRAY_SPECIFIER = auto()
    TYPE_ARGUMENT = auto()
    TYPE_ARGUMENTS = auto()
    TYPE_ARGUMENTS_SEQ = auto()
    TYPE_PARAMETER = auto()
    TYPE_PARAMETERS = auto()
    TYPE_PARAMETERS_SEQ = auto()
    TYPE_NAME = auto()
    TYPE = auto()
