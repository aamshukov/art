#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Graph data type """
import numpy as np
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.domain.entity import Entity
from art.framework.core.adt.graph.edge import Edge
from art.framework.core.utils.flags import Flags


class Graph(Entity):
    """
    """
    def __init__(self,
                 id=0,
                 label='',
                 value=None,       # graph specific value
                 attributes=None,  # graph specific attributes
                 flags=Flags.CLEAR,
                 digraph=False,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.label = label
        self.root = None  # optional, used in some digraph algorithms
        self.digraph = digraph  # directed or not
        self.vertices = dict()
        self.edges = dict()

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__lt__(other)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__le__(other)
        else:
            result = NotImplemented
        return result

    def matrix(self, value_type=float):
        """
        """
        size = len(self.vertices)
        result = np.zeros((size, size), dtype=value_type)
        for edge in self.edges.values():
            result[edge.endpoints[0].id][edge.endpoints[1].id] = edge.value
        return result

    def add_vertex(self, vertex):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id not in self.vertices, f"Vertex already exist: {vertex}"
        self.vertices[vertex.id] = vertex

    def remove_vertex(self, vertex):
        """
        """
        assert vertex is not None, "Invalid argument 'vertex'"
        assert vertex.id in self.vertices, f"Missing vertex: {vertex}"
        edges = self.edges.values()
        for edge in list(edges):
            vertex_u = edge.endpoints[0]
            vertex_v = edge.endpoints[1]
            if vertex_u.id == vertex.id or vertex_v.id == vertex.id:
                self.remove_edge(edge)
        assert len(vertex.adjacencies) == 0
        del self.vertices[vertex.id]

    def add_edge(self, vertex_u, vertex_v, edge_value=None):
        """
        Add new edge either U <-> V or only U -> V in case of digraph
        """
        assert vertex_u is not None, "Invalid argument 'vertex'"
        assert vertex_v is not None, "Invalid argument 'vertex'"
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        edge = Edge(len(self.edges) + 1, [vertex_u, vertex_v], edge_value, version=self.version)
        vertex_u.add_adjacence(vertex_v, edge)  # add adjacent, U -> V
        self.edges[edge.id] = edge
        if not self.digraph:
            edge = Edge(len(self.edges) + 1, [vertex_v, vertex_u], edge_value, version=self.version)
            vertex_v.add_adjacence(vertex_u, edge)  # add adjacent, U <- V
            self.edges[edge.id] = edge

    def remove_edge(self, edge):
        """
        Remove edge, only U -> V case is considered because when populated
        synthetic edges inserted in correct way:
        U -> V and then U <- V.
        """
        assert edge.id is not None, "Invalid argument 'edge'"
        vertex_u = edge.endpoints[0]
        vertex_v = edge.endpoints[1]
        assert vertex_u.id in self.vertices, f"Missing vertex: {vertex_u}"
        assert vertex_v.id in self.vertices, f"Missing vertex: {vertex_v}"
        vertex_u.remove_adjacence(vertex_v, edge)  # break U -> V relation
        del self.edges[edge.id]

    def get_vertex_degree(self, vertex):
        """
        """
        result = len(vertex.adjacencies)
        if self.digraph:
            for adjacency in vertex.adjacencies:
                if adjacency.vertex == vertex:
                    result += 1  # loop contributes 2 to a vertex's degree
        return result

    def is_leaf(self, vertex):
        degree = self.get_vertex_degree(vertex)
        return degree == 1 or degree == 0

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.label}"
