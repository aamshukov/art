#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parse tree kinds """
from enum import IntEnum, auto


class ArtParseTreeKind(IntEnum):
    """
    """
    UNKNOWN = 0
    ERRONEOUS = auto()
    INDENT = auto()
    DEDENT = auto()
    CORRUPTED_DEDENT = auto()
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
    PRIMARY_EXPRESSION = auto()
    ASSIGNMENT_OPERATOR = auto()
    ARRAY_MODIFIERS_OPT = auto()
    ARRAY_MODIFIERS = auto()
    ARRAY_BOUND_EXPRESSION = auto()
    ARRAY_LOWER_BOUND = auto()
    ARRAY_UPPER_BOUND = auto()
    ARRAY_DIMENSION = auto()
    ARRAY_DIMENSIONS = auto()
    ARRAY_SPECIFIER = auto()
    TYPE_ARGUMENT = auto()
    TYPE_ARGUMENTS = auto()
    TYPE_ARGUMENT_SEQ_OPT= auto()
    TYPE_ARGUMENT_SEQ = auto()
    TYPE_PARAMETER = auto()
    TYPE_PARAMETERS = auto()
    TYPE_PARAMETER_SEQ_OPT = auto()
    TYPE_PARAMETER_SEQ = auto()
    TYPE_NAME = auto()
    TYPE = auto()
    INTEGRAL_TYPE = auto()
    ARRAY_TYPE_RANK_SPECIFIER_OPT = auto()
    ARRAY_TYPE_RANK_SPECIFIER = auto()
    ARRAY_TYPE_RANKS = auto()
    ARGUMENT = auto()
    ARGUMENTS_OPT = auto()
    ARGUMENTS = auto()
    ARGUMENT_NAME_OPT = auto()
    ARGUMENT_NAME = auto()
    ARGUMENT_VALUE = auto()
    INVOCATION_EXPRESSION = auto()
    OBJECT_CREATION_EXPRESSION = auto()
    ARRAY_ELEMENT_ACCESS =auto()
