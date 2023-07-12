#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree domain helper """
from art.framework.core.base import Base
from art.framework.core.colors import Colors
from art.framework.core.flags import Flags
from art.framework.frontend.parser.parse_tree import ParseTree
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind


class ParseTreeDomainHelper(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def to_string(tree):
        """
        """
        match tree.kind:
            case ParseTreeKind.UNKNOWN:
                return ParseTreeDomainHelper.to_string_unknown(tree)
            case ParseTreeKind.IDENTIFIER:
                return ParseTreeDomainHelper.to_string_identifier(tree)
            case ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER:
                return ParseTreeDomainHelper.to_string_fq_identifier(tree)

    @staticmethod
    def to_string_unknown(tree):
        """
        """
        return ParseTreeKind.UNKNOWN.name

    @staticmethod
    def to_string_identifier(tree):
        """
        """
        symbol_str = '' if not tree.symbol else tree.symbol.to_string()
        return f'{ParseTreeKind.IDENTIFIER.name}:{tree.label}:{tree.value}:{symbol_str}'

    @staticmethod
    def to_string_fq_identifier(tree):
        """
        """
        symbol_str = '' if not tree.symbol else tree.symbol.to_string()
        return '' #??f'{ParseTreeKind.IDENTIFIER.name}:{tree.label}:{tree.value}:{symbol_str}'
