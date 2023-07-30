#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type kinds """
from enum import IntEnum, auto


class TypeKind(IntEnum):
    """
    """
    UNKNOWN_TYPE = 0
    INTEGER_TYPE = auto()
    REAL_TYPE = auto()
    STRING_TYPE = auto()
    BOOLEAN_TYPE = auto()
    COMPOSITE_TYPE = auto()  # struct, record, enum, etc.
    CUSTOM_TYPE = auto()     # sub-type, slice, etc.
    FUNCTION_TYPE = auto()   # fn
    PROCEDURE_TYPE = auto()  # proc
    CALLABLE_TYPE = auto()   # lambda, closure, anonymous function/procedure, etc.
