# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol tree action """
from enum import IntEnum, auto


class GrammarSymbolTreeAction(IntEnum):
    """
    """
    PROPAGATE = auto()
    REMOVE = auto()
