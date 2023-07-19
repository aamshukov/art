#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse domain helper """
from anytree import Node
from anytree.exporter import DotExporter
from art.framework.core.base import Base
from art.framework.core.graph_algorithms import GraphAlgorithms


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
