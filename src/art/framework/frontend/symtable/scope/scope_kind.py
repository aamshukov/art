#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Scope kinds """
from enum import IntEnum, auto
from art.framework.core.tree import Tree


class ScopeKind(IntEnum):
    """
    """
    UNKNOWN_SCOPE = auto()
    GLOBAL_SCOPE = auto()
    NAMESPACE_SCOPE = auto()
    STRUCTURE_SCOPE = auto()
    FUNCTION_SCOPE = auto()
    PARAMETER_SCOPE = auto()
    BLOCK_SCOPE = auto()
