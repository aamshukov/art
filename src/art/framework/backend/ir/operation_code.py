# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Instruction operation code """
from enum import IntEnum, auto


class OperationCode(IntEnum):
    """
    """
    UNKNOWN = 0
    # HIR - high-level intermediate representation (IR), usually AST/CST forest
    HIR_NOOP = auto()  # no-operation
    HIR_SIZE = auto()
    # MIR - mid-level intermediate representation (IR)
    MIR_NOOP = auto()  # no-operation
    MIR_IF_TRUE = auto()
    MIR_IF_FALSE = auto()
    MIR_GOTO = auto()
    MIR_LABEL = auto()
    MIR_RETURN = auto()
    MIR_SIZE = auto()
    # LIR - low-level intermediate representation (IR)
    LIR_NOOP = auto()  # no-operation
    LIR_SIZE = auto()
