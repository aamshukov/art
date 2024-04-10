#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
import random
from datetime import datetime
import networkx as nx
import numpy as np
from art.framework.core.algorithm.algorithms import Algorithms


class Test(unittest.TestCase):
    @staticmethod
    def generate_random_array_queries(n=3):
        p = np.random.rand(n, n)  # your "matrix of probabilities"
        adjacency = np.random.rand(*p.shape) <= p  # adjacency[ii, jj] is True with probability P[ii, jj]
        nx_graph = nx.from_numpy_array(adjacency, nx.Graph)
        array = list(nx_graph.nodes)
        queries = list(nx_graph.edges)
        random.shuffle(array)
        return array, queries

    def test_execute_range_minimum_queries(self):
        array = [4, 2, 3, 7, 1, 5, 3, 3, 9, 6, 7, -1, 4]
        queries = [(2, 7), (2, 10), (5, 9), (7, 9), (1, 11), (3, 5), (10, 14)]
        answers = Algorithms.execute_range_minmax_queries(array, queries)
        assert answers == [(1, 4), (1, 4), (3, 6), (3, 7), (-1, 11), (1, 4), (float('-inf'), 0)]

    def test_execute_range_minimum_queries_same(self):
        array = [5, 5, 5, 5, 5, 5, 5]
        queries = [(0, len(array) - 1)]
        answers = Algorithms.execute_range_minmax_queries(array, queries)
        assert answers == [(5, 0)]

    def test_execute_range_minimum_queries_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            array, queries = Test.generate_random_array_queries(n)
            answers = Algorithms.execute_range_minmax_queries(array, queries)
        now = datetime.now()
        print(f"End: {now}")

    def test_execute_range_maximum_queries(self):
        array = [4, 2, 3, 7, 1, 5, 3, 3, 9, 6, 7, -1, 4]
        queries = [(2, 7), (2, 10), (5, 9), (7, 9), (1, 11), (3, 5), (10, 14)]
        answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        assert answers == [(7, 3), (9, 8), (9, 8), (9, 8), (9, 8), (7, 3), (float('-inf'), 0)]

    def test_execute_range_maximum_queries_same(self):
        array = [5, 5, 5, 5, 5, 5, 5]
        queries = [(0, len(array) - 1)]
        answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        assert answers == [(5, 0)]

    def test_execute_range_maximum_queries_random(self):
        now = datetime.now()
        print(f"Start: {now}")
        n = 100  # watch recursion
        for k in range(100):
            now = datetime.now()
            print(f"Iteration: {k}  {now}")
            array, queries = Test.generate_random_array_queries(n)
            answers = Algorithms.execute_range_minmax_queries(array, queries, function=Algorithms.Functions.MAX)
        now = datetime.now()
        print(f"End: {now}")

    def test_merge_intervals0_success(self):
        intervals = [[5, 5], [5, 5], [5, 5]]
        result = Algorithms.merge_intervals(intervals)
        assert result == [[5, 5]]

    def test_merge_intervals1_success(self):
        intervals = [[1, 3], [2, 6], [8, 10], [15, 18]]
        result = Algorithms.merge_intervals(intervals)
        assert result == [[1, 6], [8, 10], [15, 18]]

    def test_merge_intervals2_success(self):
        intervals = [[1, -3], [-2, -6], [-8, 10], [15, -18]]
        result = Algorithms.merge_intervals(intervals)
        assert result == [[-18, 15]]

    def test_merge_intervals3_success(self):
        intervals = [[1, 4], [4, 5]]
        result = Algorithms.merge_intervals(intervals)
        assert result == [[1, 5]]

    def test_merge_intervals_random_success(self):
        n = 1000
        p = np.random.rand(n, n)  # your "matrix of probabilities"
        adjacency = np.random.rand(*p.shape) <= p  # adjacency[ii, jj] is True with probability P[ii, jj]
        nx_graph = nx.from_numpy_array(adjacency, nx.Graph)
        tuples = list(nx_graph.edges)
        intervals = [[t[0], t[1]] for t in tuples]
        random.shuffle(intervals)
        result = Algorithms.merge_intervals(intervals)
        assert result == [[0, n - 1]]


if __name__ == '__main__':
    """
    """
    unittest.main()
