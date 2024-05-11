# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Instruction operation code """
from enum import IntEnum, auto


class OperationCode(IntEnum):
    """
    """
    Unknown = 0
    Noop = auto()  # no-operation
    # HIR - high-level intermediate representation (IR), usually AST/CST forest
    HirSize = auto()
    # MIR - mid-level intermediate representation (IR)
    MirSize = auto()
    # LIR - low-level intermediate representation (IR)
    LirSize = auto()
