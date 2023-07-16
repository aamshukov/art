#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree domain helper """
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
from art.framework.core.base import Base
from art.framework.core.graph_algorithms import GraphAlgorithms
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind
from art.framework.frontend.parser.parse_tree_visitor import ParseTreeVisitor


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
            case ParseTreeKind.LITERAL:
                return ParseTreeDomainHelper.to_string_literal(tree)
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
    def to_string_literal(tree):
        """
        """
        return f'{ParseTreeKind.LITERAL.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_identifier(tree):
        """
        """
        return f'{ParseTreeKind.IDENTIFIER.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_fq_identifier(tree):
        """
        D:\Python\envs\python311-64bit\Lib\site-packages\pptree\pptree.py
        """
        class FqIdVisitor(ParseTreeVisitor):
            def __init__(self, _tree):
                """
                """
                super().__init__(_tree)
                self._data_sink = ''

            @property
            def data(self):
                """
                """
                return self._data_sink

            def visit(self, _tree, *args, **kwargs):
                """
                """
                if _tree.kind == ParseTreeKind.IDENTIFIER:
                    if self._data_sink:
                        self._data_sink += '.'
                    self._data_sink = f'{self._data_sink}{_tree.symbol.token.literal}'
                return self._data_sink

        visitor = FqIdVisitor(tree)
        tree.accept(visitor, recursive=False)
        return visitor.data

    @staticmethod
    def generate_graphviz(tree, filepath):
        """
        What a weird logic... anytree.
        """
        def get_label(symbol):
            return f'{symbol.label}:{symbol.token.literal}'

        if tree:
            preorder, postorder = GraphAlgorithms.calculate_tree_traverses(tree)
            cached_nodes = dict()
            for node in preorder:
                cached_nodes[node.id] = Node(f'{get_label(node.symbol)}:{node.id}')
            nodes = list()
            for node in preorder:
                papa = None
                if node.papa:
                    papa = cached_nodes[node.papa.id]
                new_node = Node(f'{get_label(node.symbol)}:{node.id}', parent=papa)
                kids = [cached_nodes[kid.id] for kid in node.kids]
                new_node.children = kids
                nodes.append(new_node)
            if nodes:
                DotExporter(nodes[0]).to_picture(filepath)
