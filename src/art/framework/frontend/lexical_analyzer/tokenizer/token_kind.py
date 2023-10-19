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

    # error
    ERRONEOUS = auto()

    # grammar
    EPSILON = auto()
    TERMINAL = auto()
    IDENTIFIER = auto()

    # infrastructure
    WS = auto()                         # whitespace
    EOL = auto()                        # end of line, NEWLINE
    EOS = auto()                        # end of stream (file)

    # indentation
    INDENT = auto()                     # literal = '    '
    DEDENT = auto()                     # literal = '    '
    CORRUPTED_DEDENT = auto()           # corrupted sequence of indents/dedents

    # literals
    INTEGER = auto()                    # integer literal number 123
    REAL = auto()                       # real literal number 3.14159
    BOOLEAN = auto()                    # true false, boolean literal
    STRING = auto()                     # string literal "str" 'str'

    # keywords
    INTEGER_KW = auto()                 # integer, int type
    REAL_KW = auto()                    # real, float, double, decimal, number type
    BOOLEAN_KW = auto()                 # boolean, bool type
    TRUE_KW = auto()                    # true
    FALSE_KW = auto()                   # false
    STRING_KW = auto()                  # string type

    IMPORT_KW = auto()
    NAMESPACE_KW = auto()
    MODULE_KW = auto()
    ALIAS_KW = auto()

    TYPE_KW = auto()
    DEF_KW = auto()

    END_KW = auto()                     # if ... end, while ... end

    INTERFACE_KW = auto()
    CLASS_KW = auto()
    STRUCT_KW = auto()
    RECORD_KW = auto()                  # immutable struct
    ENUM_KW = auto()
    MIXIN_KW = auto()

    ABSTRACT_KW = auto()
    PARTIAL_KW = auto()
    SUPER_KW = auto()
    BASE_KW = auto()
    SELF_KW = auto()
    THIS_KW = auto()

    LET_KW = auto()
    VAR_KW = auto()
    AUTO_KW = auto()

    CONST_KW = auto()
    READONLY_KW = auto()
    ONCE_KW = auto()

    IF_KW = auto()
    ELSE_KW = auto()

    FOR_KW = auto()
    WHILE_KW = auto()
    LOOP_KW = auto()
    DO_KW = auto()
    REPEAT_KW = auto()
    UNTIL_KW = auto()

    SWITCH_KW = auto()
    CASE_KW = auto()
    WHEN_KW = auto()
    MATCH_KW = auto()
    PATTERN_KW = auto()
    DEFAULT_KW = auto()
    WITH_KW = auto()

    CONTINUE_KW = auto()
    BREAK_KW = auto()
    LEAVE_KW = auto()
    GOTO_KW = auto()
    RETURN_KW = auto()
    NOOP_KW = auto()                    # noop
    PASS_KW = auto()                    # pass

    FINALLY_KW = auto()
    DEFER_KW = auto()

    FUNCTION_KW = auto()                # fn
    PROCEDURE_KW = auto()               # proc
    LAMBDA_KW = auto()                  # lm
    LAZY_KW = auto()
    OPTIONAL_KW = auto()                # opt optional
    RECURSIVE_KW = auto()

    IS_KW = auto()
    AS_KW = auto()

    IN_KW = auto()

    SCOPED_KW = auto()                  # with

    ASYNC_KW = auto()
    AWAIT_KW = auto()
    LOCK_KW = auto()
    YIELD_KW = auto()

    ASSERT_KW = auto()
    PRAGMA_KW = auto()

    COLUMN_KW = auto()                  # column, array memory layout
    ROW_KW = auto()                     # row, array memory layout
    JAGGED_KW = auto()                  # is jagged array
    SPARSE_KW = auto()                  # sparse array with implicitly replicated value, see Chapel
    UNCHECKED_KW = auto()               # unchecked
    DYNAMIC_KW = auto()                 # dynamic allocated array

    ADD_KW = auto()
    SUB_KW = auto()
    MUL_KW = auto()
    DIV_KW = auto()
    MOD_KW = auto()
    SHL_KW = auto()                     # shift left
    SHR_KW = auto()                     # shift right

    AND_KW = auto()
    OR_KW = auto()
    NOT_KW = auto()                     # !
    NEG_KW = auto()                     # negate neg

    EQUAL_KW = auto()                   # eq
    NOT_EQUAL_KW = auto()               # ne
    LESS_THAN_KW = auto()               # lt
    LESS_THAN_OR_EQUAL_KW = auto()      # le
    GREATER_THAN_KW = auto()            # gt
    GREATER_THAN_OR_EQUAL_KW = auto()   # ge

    # punctuations
    LEFT_PARENTHESIS = auto()           # (
    RIGHT_PARENTHESIS = auto()          # )
    LEFT_SQUARE_BRACKET = auto()        # [
    RIGHT_SQUARE_BRACKET = auto()       # ]
    LEFT_CURLY_BRACKET = auto()         # {
    RIGHT_CURLY_BRACKET = auto()        # }
    DOT = auto()                        # .
    RANGE = auto()                      # ..
    ELLIPSES = auto()                   # ...
    COLON = auto()                      # :
    COLONS = auto()                     # ::
    SEMICOLON = auto()                  # ;
    COMMA = auto()                      # ,
    QUESTION_MARK = auto()              # ?
    NULL_COALESCING_OPERATOR = auto()   # null-coalescing operator, C#
    COMMERCIAL_AT = auto()              # @
    GRAVE_ACCENT = auto()               # `
    BACK_SLASH = auto()                 # \

    EQUALS_SIGN = auto()                # = ASSIGNMENT
    EQUAL = auto()                      # ==
    NOT_EQUAL = auto()                  # !=
    EXCLAMATION_MARK = auto()           # !

    LESS_THAN_SIGN = auto()             # <
    LESS_THAN_OR_EQUAL = auto()         # <=
    SHIFT_LEFT = auto()                 # <<
    SHIFT_LEFT_ASSIGNMENT = auto()      # <<=

    GREATER_THAN_SIGN = auto()          # >
    GREATER_THAN_OR_EQUAL = auto()      # >=
    SHIFT_RIGHT = auto()                # >>
    SHIFT_RIGHT_ASSIGNMENT = auto()     # >>=

    SPACESHIP = auto()                  # <=>

    PLUS_SIGN = auto()                  # +
    INCREMENT = auto()                  # ++
    ADD_ASSIGNMENT = auto()             # +=

    HYPHEN_MINUS = auto()               # -
    DECREMENT = auto()                  # --
    SUB_ASSIGNMENT = auto()             # -=

    ARROW = auto()                      # ->
    DOUBLE_ARROW = auto()               # =>

    ASTERISK = auto()                   # * MUL
    MUL_ASSIGNMENT = auto()             # *=
    FORWARD_SLASH = auto()              # / DIV
    DIV_ASSIGNMENT = auto()             # /=
    PERCENT_SIGN = auto()               # % MOD
    MOD_ASSIGNMENT = auto()             # %=

    BITWISE_AND = auto()                # &
    LOGICAL_AND = auto()                # &&
    BITWISE_AND_ASSIGNMENT = auto()     # &=
    BITWISE_OR = auto()                 # |
    LOGICAL_OR = auto()                 # ||
    BITWISE_OR_ASSIGNMENT = auto()      # |=
    BITWISE_XOR = auto()                # ^
    BITWISE_XOR_ASSIGNMENT = auto()     # ^=
    BITWISE_NOT = auto()                # ~  tilde
    BITWISE_NOT_ASSIGNMENT = auto()     # ~=

    # comments
    SINGLE_LINE_COMMENT = auto()        # # //
    MULTI_LINE_COMMENT = auto()         # /* */

    @staticmethod
    def get_keywords():
        """
        Get keywords dictionary of string:TokenKind.
        """
        result = dict()
        result['int'] = TokenKind.INTEGER_KW
        result['integer'] = TokenKind.INTEGER_KW
        result['real'] = TokenKind.REAL_KW
        result['float'] = TokenKind.REAL_KW
        result['double'] = TokenKind.REAL_KW
        result['decimal'] = TokenKind.REAL_KW
        result['number'] = TokenKind.REAL_KW
        result['bool'] = TokenKind.BOOLEAN_KW
        result['boolean'] = TokenKind.BOOLEAN_KW
        result['true'] = TokenKind.TRUE_KW
        result['false'] = TokenKind.FALSE_KW
        result['string'] = TokenKind.STRING_KW
        result['import'] = TokenKind.IMPORT_KW
        result['namespace'] = TokenKind.NAMESPACE_KW
        result['module'] = TokenKind.MODULE_KW
        result['alias'] = TokenKind.ALIAS_KW
        result['type'] = TokenKind.TYPE_KW
        result['def'] = TokenKind.DEF_KW
        result['end'] = TokenKind.END_KW
        result['interface'] = TokenKind.INTERFACE_KW
        result['class'] = TokenKind.CLASS_KW
        result['struct'] = TokenKind.STRUCT_KW
        result['record'] = TokenKind.RECORD_KW
        result['enum'] = TokenKind.ENUM_KW
        result['mixin'] = TokenKind.MIXIN_KW
        result['abstract'] = TokenKind.ABSTRACT_KW
        result['partial'] = TokenKind.PARTIAL_KW
        result['super'] = TokenKind.SUPER_KW
        result['base'] = TokenKind.BASE_KW
        result['self'] = TokenKind.SELF_KW
        result['this'] = TokenKind.THIS_KW
        result['let'] = TokenKind.LET_KW
        result['var'] = TokenKind.VAR_KW
        result['auto'] = TokenKind.AUTO_KW
        result['const'] = TokenKind.CONST_KW
        result['readonly'] = TokenKind.READONLY_KW
        result['once'] = TokenKind.ONCE_KW
        result['if'] = TokenKind.IF_KW
        result['else'] = TokenKind.ELSE_KW
        result['for'] = TokenKind.FOR_KW
        result['while'] = TokenKind.WHILE_KW
        result['loop'] = TokenKind.LOOP_KW
        result['do'] = TokenKind.DO_KW
        result['repeat'] = TokenKind.REPEAT_KW
        result['until'] = TokenKind.UNTIL_KW
        result['switch'] = TokenKind.SWITCH_KW
        result['case'] = TokenKind.CASE_KW
        result['when'] = TokenKind.WHEN_KW
        result['match'] = TokenKind.MATCH_KW
        result['pattern'] = TokenKind.PATTERN_KW
        result['default'] = TokenKind.DEFAULT_KW
        result['with'] = TokenKind.WITH_KW
        result['continue'] = TokenKind.CONTINUE_KW
        result['break'] = TokenKind.BREAK_KW
        result['leave'] = TokenKind.LEAVE_KW
        result['goto'] = TokenKind.GOTO_KW
        result['return'] = TokenKind.RETURN_KW
        result['noop'] = TokenKind.NOOP_KW
        result['pass'] = TokenKind.PASS_KW
        result['finally'] = TokenKind.FINALLY_KW
        result['defer'] = TokenKind.DEFER_KW
        result['fn'] = TokenKind.FUNCTION_KW
        result['proc'] = TokenKind.PROCEDURE_KW
        result['lm'] = TokenKind.LAMBDA_KW
        result['lambda'] = TokenKind.LAMBDA_KW
        result['closure'] = TokenKind.LAMBDA_KW
        result['lz'] = TokenKind.LAZY_KW
        result['lazy'] = TokenKind.LAZY_KW
        result['opt'] = TokenKind.OPTIONAL_KW
        result['optional'] = TokenKind.OPTIONAL_KW
        result['recursive'] = TokenKind.RECURSIVE_KW
        result['is'] = TokenKind.IS_KW
        result['as'] = TokenKind.AS_KW
        result['in'] = TokenKind.IN_KW
        result['scoped'] = TokenKind.SCOPED_KW
        result['async'] = TokenKind.ASYNC_KW
        result['await'] = TokenKind.AWAIT_KW
        result['lock'] = TokenKind.LOCK_KW
        result['yield'] = TokenKind.YIELD_KW
        result['assert'] = TokenKind.ASSERT_KW
        result['pragma'] = TokenKind.PRAGMA_KW
        result['column'] = TokenKind.COLUMN_KW
        result['col'] = TokenKind.COLUMN_KW
        result['row'] = TokenKind.ROW_KW
        result['jagged'] = TokenKind.JAGGED_KW
        result['sparse'] = TokenKind.SPARSE_KW
        result['unchecked'] = TokenKind.UNCHECKED_KW
        result['dynamic'] = TokenKind.DYNAMIC_KW
        result['add'] = TokenKind.ADD_KW
        result['sub'] = TokenKind.SUB_KW
        result['mul'] = TokenKind.MUL_KW
        result['div'] = TokenKind.DIV_KW
        result['mod'] = TokenKind.MOD_KW
        result['shl'] = TokenKind.SHL_KW
        result['shr'] = TokenKind.SHR_KW
        result['and'] = TokenKind.AND_KW
        result['or'] = TokenKind.OR_KW
        result['not'] = TokenKind.NOT_KW
        result['neg'] = TokenKind.NEG_KW
        result['eq'] = TokenKind.EQUAL_KW
        result['ne'] = TokenKind.NOT_EQUAL_KW
        result['lt'] = TokenKind.LESS_THAN_KW
        result['le'] = TokenKind.LESS_THAN_OR_EQUAL_KW
        result['gt'] = TokenKind.GREATER_THAN_KW
        result['ge'] = TokenKind.GREATER_THAN_OR_EQUAL_KW
        return result
