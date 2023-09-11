#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Operator precedence level """
from enum import IntEnum


class OperatorPrecedenceLevel(IntEnum):
    """
    Operator precedence levels (binding power, Pratt) for the unary, binary or ternary operators.
    Bigger numbers mean higher precedence.
    """
    UNKNOWN = 0             # lowest precedence levels (binding power, Pratt) to start parsing
    COMMA = 10              # ,
    ASSIGNMENT = 20         # =  -=  +=  *=  /=  %=  &=  ^=  |=  -=  <<=  >>=
    CONDITIONAL = 30        # ? :
    LOGICAL_OR = 40         # ||  or
    LOGICAL_AND = 42        # &&  and
    BITWISE_OR = 50         # |
    BITWISE_XOR = 52        # ^  xor
    BITWISE_AND = 54        # &
    EQUALITY = 60           # == eq  != ne
    RELATIONAL = 62         # < lt  > gt  <= le  >= ge  is
    SPACESHIP = 64          # <=>
    SHIFT = 70              # << shl  >> shr
    ADDITIVE = 72           # + add  - sub
    MULTIPLICATIVE = 74     # * mul  / div  % mod
    PREFIX = 80             # unary operators: + ++ - -- ! not ~ neg
    POSTFIX = 82            # !
    INVOCATION = 90         # foo(a, b, c)
    ARRAY_ACCESS = 92       # a[1,2]
    MEMBER_ACCESS = 94      # .:  foo.bar
    PARENTHESIZED = 96      # (1+2)
    LITERAL = 100           # 1
    IDENTIFIER = 100        # foo
