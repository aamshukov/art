#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token kinds """
from enum import IntEnum, auto


class TokenKind(IntEnum):
    """
    """
    UNKNOWN = 0

    EPSILON = auto()

    WS = auto()    # whitespace
    EOL = auto()   # end of line
    EOS = auto()   # end of stream (file)

    INDENT = auto()  # literal = '    '
    DEDENT = auto()  # literal = '    '
    CORRUPTED_DEDENT = auto()  # corrupted sequence of indents/dedents

    IDENTIFIER = auto()

    INTEGER = auto()  # integer number
    INTEGER_KW = auto()

    REAL = auto()  # real number
    REAL_KW = auto()

    BOOLEAN_KW = auto()
    TRUE = auto()
    FALSE = auto()

    STRING = auto()     # string literal
    STRING_KW = auto()  # string type

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
    PASS = auto()  # pass

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

    COMP_EQUAL = auto()  # eq
    EQUALS_SIGN = auto()  # = ASSIGNMENT
    EQUAL = auto()  # ==

    COMP_NOT_EQUAL = auto()  # ne
    EXCLAMATION_MARK = auto()  # !
    NOT_EQUAL = auto()  # !=

    COMP_LESS_THAN = auto()  # lt
    LESS_THAN_SIGN = auto()  # <
    COMP_LESS_THAN_OR_EQUAL = auto()  # le
    LESS_THAN_OR_EQUAL = auto()  # <=
    SHIFT_LEFT = auto()  # <<
    SHIFT_LEFT_OR_EQUAL = auto()  # <<=

    COMP_GREATER_THAN = auto()  # gt
    GREATER_THAN_SIGN = auto()  # >
    COMP_GREATER_THAN_OR_EQUAL = auto()  # ge
    GREATER_THAN_OR_EQUAL = auto()  # >=
    SHIFT_RIGHT = auto()  # >>
    SHIFT_RIGHT_OR_EQUAL = auto()  # >>=

    SPACESHIP = auto()  # <=>

    DOT = auto()  # .
    RANGE = auto()  # ..
    ELLIPSES = auto()  # ...

    PLUS_SIGN = auto()  # +
    INCREMENT = auto()  # ++
    ADD_ASSIGNMENT = auto()  # +=

    HYPHEN_MINUS = auto()  # -
    DECREMENT = auto()  # --
    SUB_ASSIGNMENT = auto()  # -=
    ARROW = auto()  # ->
    DOUBLE_ARROW = auto()  # =>

    ASTERISK = auto()  # * MUL
    MUL_ASSIGNMENT = auto()  # *=

    FORWARD_SLASH = auto()  # / DIV
    DIV_ASSIGNMENT = auto()  # /=

    PERCENT_SIGN = auto()  # % MOD
    MOD_ASSIGNMENT = auto()  # %=

    BITWISE_AND = auto()  # &
    BITWISE_AND_ASSIGNMENT = auto()  # &=
    BITWISE_OR = auto()  # |
    BITWISE_OR_ASSIGNMENT = auto()  # |=
    BITWISE_XOR = auto()  # ^
    BITWISE_XOR_ASSIGNMENT = auto()  # ^=
    BITWISE_NOT = auto()  # ~
    BITWISE_NOT_ASSIGNMENT = auto()  # ~=

    COLON = auto()  # :
    COLONS = auto()  # ::
    SEMICOLON = auto()  # ;
    COMMA = auto()  # ,
    QUESTION_MARK = auto()  # ?
    COMMERCIAL_AT = auto()  # @
    GRAVE_ACCENT = auto()  # `

    BACK_SLASH = auto()  # \

    SINGLE_LINE_COMMENT = auto()  # # //
    MULTI_LINE_COMMENT = auto()  # /* */

    COLUMN_KW = auto()  # column
    ROW_KW = auto()  # row
    JAGGED_KW = auto()
    UNCHECKED_KW = auto()  # unchecked

    ERRONEOUS = auto()
