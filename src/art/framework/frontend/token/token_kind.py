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

    SHEBANG = auto()  #
    SEMICOLON = auto()  # ;
    COLON = auto()  # :
    DOT = auto()  # .
    DOT_DOT = auto()  # ..
    DOT_DOT_DOT = auto()  # ...
    COMMA = auto()  # ,
    OPEN_SQUARE_BRACKET = auto()  # [
    CLOSE_SQUARE_BRACKET = auto()  # ]
    OPEN_PAREN = auto()  # (
    CLOSE_PAREN = auto()  # )
    OPEN_CURLY_BRACKET = auto()  # {
    CLOSE_CURLY_BRACKET = auto()  # }
    OPEN_ANGLE_BRACKET = auto()  # <
    CLOSE_ANGLE_BRACKET = auto()  # >
    PLUS = auto()  # +
    MINUS = auto()  # -
    MULTIPLICATION = auto()  # *
    DIVISION = auto()  # /
    # >>
    # <<
    EQUAL = auto()  # ==
    NOT_EQUAL = auto()  # !=
    LESS_THAN = auto()  # <
    LESS_EQUAL = auto()  # <=
    GREATER_THAN = auto()  # >
    GREATER_EQUAL = auto()  # >=
    SPACESHIP = auto()  # <=>
    AMPERSAND = auto()  # &
    AMPERSAND_AMPERSAND = auto() # &&
    BAR = auto()  # |
    BAR_BAR = auto()  # ||
    XOR = auto()  # ^
    NOT_T = auto()  # !
    ASSIGNMENT = auto()  # =
    ASSIGNMENT_PLUS = auto()  # +=
    ASSIGNMENT_MINUS = auto()  # -=
    # *=
    # /=
    # >>=
    # <<=
    # &=
    # |=
    # ^=
    #

    ERRONEOUS = auto()
