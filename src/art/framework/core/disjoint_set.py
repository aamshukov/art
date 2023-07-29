#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Disjount set / Union Find """
# https://algs4.cs.princeton.edu/15uf/UF.java.html
# by Robert Sedgewick and Kevin Wayne
from art.framework.core.base import Base


class DisjointSet(Base):
    """
    """
    def __init__(self, elements):
        """
        """
        super().__init__()
        self.count = len(elements)         # decimal_digit_number of elements
        assert self.count, "Disjoint set (union find) ctor, decimal_digit_number of element must be positive."
        self.parents = [0] * self.count   # parent[i] = parent of i
        self.ranks = [0] * self.count     # rank[i] = rank of subtree rooted at i
        self.mapping = dict()              # element to index map
        for k, element in enumerate(elements):
            self.parents[k] = k
            self.ranks[k] = 0
            self.mapping[element] = k

    def find(self, element):
        """
        """
        r = self.mapping[element]    # get index
        while r != self.parents[r]:  # locate root
            self.parents[r] = self.parents[self.parents[r]]  # path compression by halving, full path compression
            r = self.parents[r]                                # is more involving another loop from
        return r                                                # the original element and up to the root

    def union(self, element1, element2):
        """
        """
        r1 = self.find(element1)
        r2 = self.find(element2)
        if r1 != r2:
            if self.ranks[r1] < self.ranks[r2]:
                self.parents[r1] = r2
            elif self.ranks[r1] > self.ranks[r2]:
                self.parents[r2] = r1
            else:
                self.parents[r2] = r1
                self.ranks[r1] += 1
            self.count -= 1
