#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree factory """
from copy import deepcopy

from art.framework.core.base import Base
from art.framework.core.colors import Colors
from art.framework.core.flags import Flags
from art.framework.frontend.parser.parse_tree import ParseTree
from art.framework.frontend.symtable.symbol_factory import SymbolFactory


class ParseTreeFactory(Base):
    """
    """
    id_generator = 0

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def get_next_id():
        """
        """
        ParseTreeFactory.id_generator += 1
        return ParseTreeFactory.id_generator

    @staticmethod
    def create(kind,
               label='',
               value=None,
               attributes=None,
               flags=Flags.CLEAR,
               color=Colors.UNKNOWN,
               version='1.0'):
        """
        """
        return ParseTree(ParseTreeFactory.get_next_id(),
                         kind,
                         label=label,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         color=color,
                         version=version)

    @staticmethod
    def make_tree(kind, grammar, token):
        tree = ParseTreeFactory.create(kind, kind.name)
        tree.symbol = SymbolFactory.create(tree.label)
        tree.symbol.grammar_symbol = grammar.lookup_symbol(kind.name)
        tree.symbol.token = token
        return tree
