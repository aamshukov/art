#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parse tree kinds """
from enum import IntEnum, auto


class ArtSyntaxKind(IntEnum):
    """
    This enum augments all possible syntax constructions and their combinations.
    Helps navigate parsing process.
    """
    UNKNOWN = 0
    EXPRESSION = auto()
    CONDITIONAL_EXPRESSION = auto()
    UNARY_EXPRESSION = auto()
    MULTIPLICATIVE_EXPRESSION = auto()
    ADDITIVE_EXPRESSION = auto()
    SHIFT_EXPRESSION = auto()
    RELATIONAL_EXPRESSION = auto()
    EQUALITY_EXPRESSION = auto()
    BITWISE_AND_EXPRESSION = auto()
    BITWISE_INCLUSIVE_OR_EXPRESSION = auto()
    BITWISE_EXCLUSIVE_OR_EXPRESSION = auto()
    LOGICAL_AND_EXPRESSION = auto()
    LOGICAL_OR_EXPRESSION = auto()

    PRIMARY_EXPRESSION = auto()
    ARRAY_BOUND_EXPRESSION = auto()
    CONDITIONAL_OR_EXPRESSION = auto()
