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

    # error
    ERRONEOUS = auto()

    # grammar
    TERMINAL = auto()
    IDENTIFIER = auto()
    IDENTIFIERS = auto()

    # literals
    LITERAL = auto()

    # indentation
    INDENT = auto()
    DEDENT = auto()
    CORRUPTED_DEDENT = auto()

    # type
    TYPE = auto()
    TYPE_NAME = auto()
    TYPE_PARAMETER_SEQ_OPT = auto()
    TYPE_PARAMETER_SEQ = auto()
    TYPE_PARAMETERS = auto()
    TYPE_PARAMETER = auto()
    TYPE_ARGUMENT_SEQ_OPT= auto()
    TYPE_ARGUMENT_SEQ = auto()
    TYPE_ARGUMENTS = auto()
    TYPE_ARGUMENT = auto()
    TYPE_ARGUMENT_UNION = auto()
    TYPE_ALIAS = auto()
    TYPE_PREDICATE = auto()
    ARRAY_TYPE_RANK_SPECIFIER_OPT = auto()
    ARRAY_TYPE_RANK_SPECIFIER = auto()
    ARRAY_TYPE_RANKS_OPT = auto()
    ARRAY_TYPE_RANKS = auto()
    ARRAY_TYPE_SPECIFIER_OPT = auto()
    ARRAY_TYPE_SPECIFIER = auto()
    ARRAY_DIMENSIONS = auto()
    ARRAY_DIMENSION = auto()
    ARRAY_LOWER_BOUND = auto()
    ARRAY_UPPER_BOUND = auto()
    ARRAY_BOUND_EXPRESSION = auto()
    ARRAY_MODIFIERS_OPT = auto()
    ARRAY_MODIFIERS = auto()
    ARRAY_SLICING_SPECIFIER = auto()
    ARRAY_SLICE_SPECIFIER_OPT = auto()
    ARRAY_SLICE_SPECIFIER = auto()
    ARRAY_SLICING_STEP_OPT = auto()
    ARRAY_SLICING_STEP = auto()
    INTEGRAL_TYPE = auto()

    # expression
    EXPRESSIONS = auto()
    EXPRESSION = auto()
    NON_ASSIGNMENT_EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    ASSIGNMENT_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    MULTIPLICATIVE_EXPRESSION = auto()
    ADDITIVE_EXPRESSION = auto()
    SHIFT_EXPRESSION = auto()
    RELATIONAL_EXPRESSION = auto()
    EQUALITY_EXPRESSION = auto()
    AND_EXPRESSION = auto()
    EXCLUSIVE_OR_EXPRESSION = auto()
    INCLUSIVE_OR_EXPRESSION = auto()
    CONDITIONAL_AND_EXPRESSION = auto()
    CONDITIONAL_OR_EXPRESSION = auto()
    PRIMARY_EXPRESSION = auto()
    MEMBER_ACCESS = auto()
    ARRAY_ELEMENTS = auto()
    ARRAY_ELEMENT_ACCESS = auto()
    INVOCATION_EXPRESSION = auto()
    PRE_INCREMENT_EXPRESSION = auto()
    PRE_DECREMENT_EXPRESSION = auto()
    POST_INCREMENT_EXPRESSION = auto()
    POST_DECREMENT_EXPRESSION = auto()
    OBJECT_CREATION_EXPRESSION = auto()
    PARENTHESIZED_EXPRESSION = auto()

    # argument
    ARGUMENTS_OPT = auto()
    ARGUMENTS = auto()
    ARGUMENT = auto()
    ARGUMENT_NAME_OPT = auto()
    ARGUMENT_NAME = auto()
    ARGUMENT_VALUES = auto()
    ARGUMENT_VALUE_OPT = auto()
    ARGUMENT_VALUE = auto()
    ARGUMENT_VALUE_UNION = auto()
    ARGUMENT_MODIFIERS_OPT = auto()
    ARGUMENT_MODIFIERS = auto()

    # infrastructure
    FULLY_QUALIFIED_IDENTIFIER = auto()
