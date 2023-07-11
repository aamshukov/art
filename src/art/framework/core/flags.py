#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Flags enumeration """
from enum import Flag, auto


class Flags(Flag):
    """
    """
    CLEAR = auto()
    DIRTY = auto()
    PROCESSED = auto()
    COMPLETED = auto()
    VISITED = auto()
    MARKED = auto()
    DELETED = auto()
    GENUINE = auto()
    SYNTHETIC = auto()  # additional (artificial) tokens which are inserted
                        # into the token stream, syntactic sugar - desugaring ...
    CONTEXTUAL = auto()  # contextual, recognized in specific contexts,
                         # similar to C# get/set, async/await ...
    LEAF = auto()
    OVERFLOW = auto()
    UNDERFLOW = auto()
    INVALID = auto()
    ROOT_IN_AST = auto()  # aka ANTLR, expr : expr (’+’^ mexpr)* EOF!  \  mutually
    NOT_IN_AST = auto()   # aka ANTLR, expr : expr (’+’^ mexpr)* EOF!  /  exclusive

    @staticmethod
    def modify_flags(flags, add, remove):
        return (flags & ~remove) | add
