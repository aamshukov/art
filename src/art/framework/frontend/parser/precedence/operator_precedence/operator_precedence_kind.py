#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Operator precedence kind """
from enum import IntEnum


class OperatorPrecedenceKind(IntEnum):
    """
    """
    UNKNOWN = 0,          # unknown relation
    LESS_RELATION = 1,    # ⋖, op1 has higher precedence than op2
    EQUAL_RELATION = 2,   # ≗, op1 an op2 have the same precedence
    GREATER_RELATION = 3  # ⋗, op1 has lower precedence than op2
