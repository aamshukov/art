#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from enum import IntEnum, auto
from art.framework.core.base import Base


class ParseResult(Base):
    """
    """
    class Status(IntEnum):
        """
        """
        UNKNOWN = 0
        OK = auto()        # valid tree
        ERROR = auto()     # tree is not valid, parsing did not succeed
        OPTIONAL = auto()  # optional non-terminal has been skipped

    def __init__(self, status, tree=None):
        """
        """
        super().__init__()
        self.status = status
        self.tree = tree
