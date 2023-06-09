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
    # additional (artificial) tokens which are inserted into the token stream, syntactic sugar - desugaring ...
    SYNTHETIC = auto()
    # contextual, recognized in specific contexts, similar to C# get/set, async/await ...
    CONTEXTUAL = auto()
    LEAF = auto()
    OVERFLOW = auto()
    UNDERFLOW = auto()
    INVALID = auto()

    @staticmethod
    def modify_flags(flags, add, remove):
        return (flags & ~remove) | add
