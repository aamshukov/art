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
    CLASS = auto()
    INTERFACE = auto()
    ABSTRACT = auto()
    MIXIN = auto()

    IMPORT = auto()
    NAMESPACE = auto()
    MODULE = auto()
    ALIAS = auto()

    LET = auto()
    VAR = auto()
    CONST = auto()
    READONLY = auto()

    SUPER = auto()
    BASE = auto()
    SELF = auto()
    THIS = auto()

    IF = auto()
    ELSE = auto()

    FOR = auto()
    WHILE = auto()
    DO = auto()
    REPEAT = auto()

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
    NOOP = auto()  # noop

    PARTIAL = auto()
    FINALLY = auto()
    DEFER = auto()

    IS = auto()
    AS = auto()

    AND = auto()
    OR = auto()
    NOT = auto()  # !
    NEG = auto()  # negate

    FUNCTION = auto()  # fn
    PROCEDURE = auto()  # proc
    LAMBDA = auto()
    LAZY = auto()
    RECURSIVE = auto()

    TYPE = auto()
    DEF = auto()

    WITH = auto()
    SCOPED = auto()

    ASYNC = auto()
    AWAIT = auto()
    LOCK = auto()
    YIELD = auto()

    ASSERT = auto()

    PRAGMA = auto()

    LEFT_PARENTHESIS = auto()  # (
    RIGHT_PARENTHESIS = auto()  # )
    LEFT_SQUARE_BRACKET = auto()  # [
    RIGHT_SQUARE_BRACKET = auto()  # ]
    LEFT_CURLY_BRACKET = auto()  # {
    RIGHT_CURLY_BRACKET = auto()  # }

    PLUS_SIGN = auto()  # +
    HYPHEN_MINUS = auto()  # -
    ASTERISK = auto()  # * MUL
    FORWARD_SLASH = auto()  # / DIV
    BACK_SLASH = auto()  # \

    EQUALS_SIGN = auto()  # = ASSIGNMENT
    LESS_THAN_SIGN = auto()  # <
    GREATER_THAN_SIGN = auto()  # >

    EQUAL = auto()  # ==
    NOT_EQUAL = auto()  # !=
    LESS_EQUAL = auto()  # <=
    GREATER_EQUAL = auto()  # >=
    SPACESHIP = auto()  # <=>

    SEMICOLON = auto()  # ;
    COLON = auto()  # :
    DOT = auto()  # .
    RANGE = auto()  # ..
    ELLIPSES = auto()  # ...
    COMMA = auto()  # ,

    BITWISE_AND = auto()  # &
    BITWISE_OR = auto()  # |
    BITWISE_XOR = auto()  # |



    # >>
    # <<
    AMPERSAND = auto()  # &
    AMPERSAND_AMPERSAND = auto() # &&
    BAR_BAR = auto()  # ||
    NOT_T = auto()  # !
    ADDITION_ASSIGNMENT = auto()  # +=
    SUBSTRACTION_ASSIGNMENT = auto()  # -=
    # *=
    # /=
    # >>=
    # <<=
    # &=
    # |=
    # ^=
    #


    ERRONEOUS = auto()
