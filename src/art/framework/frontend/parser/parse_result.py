#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from enum import IntEnum, auto
from art.framework.core.domain.base import Base
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class ParseResult(Base):
    """
    """
    class Status(IntEnum):
        """
        """
        UNKNOWN = 0
        OK = auto()         # valid tree
        ERROR = auto()      # tree is not valid, parsing did not succeed
        BACKTRACK = auto()  # non-terminal cannot be parsed - backtrack to the next alternative
        OPTIONAL = auto()   # optional non-terminal has been skipped

    def __init__(self, status, tree=None, hint=TokenKind.UNKNOWN):
        """
        """
        super().__init__()
        self.tree = tree
        self.status = status
        self.hint = hint  # in case of backtracking - suggested alternative, see array related calls
