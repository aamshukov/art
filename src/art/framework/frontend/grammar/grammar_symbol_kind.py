# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol type """
from enum import IntEnum, auto


class GrammarSymbolKind(IntEnum):
    """
    """
    UNKNOWN = 0
    TERMINAL = auto()
    NON_TERMINAL = auto()
    EPSILON = auto()
