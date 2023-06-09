#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token kinds """
from enum import IntEnum, auto


class TokenKind(IntEnum):
    """
    """
    UNKNOWN = auto()

    EPSILON = auto()

    WS = auto()    # whitespace
    EOL = auto()   # end of line
    EOS = auto()   # end of stream (file)

    INDENT = auto()  # literal = '    '
    DEDENT = auto()  # literal = '    '

    IDENTIFIER = auto()

    INT = auto()
    INTEGER = auto()

    REAL = auto()
    FLOAT = auto()
    DOUBLE = auto()
    DECIMAL = auto()

    BOOL = auto()
    BOOLEAN = auto()
    TRUE = auto()
    FALSE = auto()

    STRING = auto()

    ENUM = auto()

    STRUCT = auto()
    RECORD = auto()

    CONST = auto()
    READONLY = auto()

    LET = auto()
    VAR = auto()

    NAMESPACE = auto()
    IMPORT = auto()

    IF = auto()
    ELSE = auto()

    FOR = auto()
    WHILE = auto()
    DO = auto()

    SWITCH = auto()
    CASE = auto()
    WHEN = auto()
    MATCH = auto()
    PATTERN = auto()
    DEFAULT = auto()

    CONTINUE = auto()
    BREAK = auto()
    LEAVE = auto()
    GOTO = auto()
    RETURN = auto()

    PARTIAL = auto()

    IS = auto()
    AS = auto()

    AND = auto()
    OR = auto()
    NOT = auto()
    NEG = auto()

    FN = auto()
    LAZY = auto()
    NOOP = auto()

    TYPE = auto()

    # #
    # :
    # .
    # ..
    # ...
    # ,
    # [
    # ]
    # (
    # )
    # {
    # }
    #
    # +
    # -
    # *
    # /
    # >>
    # <<
    # =
    # ==
    # !=
    # <
    # <=
    # >
    GT_EQ = auto()  # >=
    SPACESHIP = auto()  # <=>
    AMPERSAND = auto()  # &
    # &&
    # |
    # ||
    # ^
    # !
    #
    # =
    # +=
    # -=
    # *=
    # /=
    # >>=
    # <<=
    # &=
    # |=
    # ^=
    #
