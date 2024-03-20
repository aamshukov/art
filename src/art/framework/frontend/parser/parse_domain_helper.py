#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse domain helper """
from anytree import Node
from anytree.exporter import DotExporter
from art.framework.core.domain.base import Base
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.adt.graph.graph_algorithms import GraphAlgorithms
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class ParseTreeDomainHelper(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def generate_graphviz(tree, filepath):
        """
        What a weird logic... anytree.
        """
        def get_label(symbol):
            if symbol.token:
                if symbol.token.kind == TokenKind.EOL:
                    return f'{symbol.label}:eol'
                elif symbol.token.kind == TokenKind.WS:
                    return f'{symbol.label}:ws'
                elif symbol.token.kind == TokenKind.INDENT:
                    return f'{symbol.label}:indent'
                elif symbol.token.kind == TokenKind.DEDENT:
                    return f'{symbol.label}:dedent'
                elif symbol.token.kind == TokenKind.DOT:
                    return f'{symbol.label}:dot'
                elif symbol.token.kind == TokenKind.RANGE:
                    return f'{symbol.label}:range'
                elif symbol.token.kind == TokenKind.ELLIPSES:
                    return f'{symbol.label}:ellipses'
                elif symbol.token.kind == TokenKind.COMMA:
                    return f'{symbol.label}:comma'
                elif symbol.token.kind == TokenKind.COLON:
                    return f'{symbol.label}:colon'
                elif symbol.token.kind == TokenKind.COLONS:
                    return f'{symbol.label}:colons'
                elif symbol.token.kind == TokenKind.SEMICOLON:
                    return f'{symbol.label}:semicolon'
                elif symbol.token.kind == TokenKind.GRAVE_ACCENT:
                    return f'{symbol.label}:grave_accent'
                elif symbol.token.kind == TokenKind.IDENTIFIER:
                    return f'{symbol.token.literal}'
                else:
                    return f'{symbol.label}:{symbol.token.literal}'
            else:
                return f'{symbol.label}'

        if tree:
            preorder, postorder = GraphAlgorithms.calculate_tree_traverses(tree)
            cached_nodes = dict()
            for node in preorder:
                cached_nodes[node.id] = Node(f'{get_label(node.symbol)}:{node.id}:'
                                             f'attrs({DomainHelper.dict_to_string(node.attributes)})')
            nodes = list()
            for node in preorder:
                papa = None
                if node.papa:
                    papa = cached_nodes[node.papa.id]
                new_node = cached_nodes[node.id]
                new_node.parent = papa
                kids = [cached_nodes[kid.id] for kid in node.kids]
                new_node.children = kids
                nodes.append(new_node)
            if nodes:
                DotExporter(nodes[0]).to_picture(filepath)
