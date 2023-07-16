#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree kinds """
from enum import IntEnum, auto


class ParseTreeKind(IntEnum):
    """
    """
    UNKNOWN = auto()
    LITERAL = auto()
    IDENTIFIER = auto()
    FULLY_QUALIFIED_IDENTIFIER = auto()
    ASSIGNMENT_OPERATOR = auto()
