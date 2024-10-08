#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Collection of algorithms """
import math
from enum import IntEnum
from functools import lru_cache
from art.framework.core.domain.base import Base


class Algorithms(Base):
    """
    """
    class Functions(IntEnum):
        """
        """
        MIN = 0
        MAX = 1

    @staticmethod
    def execute_range_minmax_queries(array, queries, function=Functions.MIN):
        """
        Range Minimum Query (RMQ) implementation based on Sparse Table lookup.
        https://www.youtube.com/watch?v=uUatD9AudXo&list=PLDV1Zeh2NRsB6SWUrDFW2RmDotAfPbeHu&index=55
        """
        assert function in set(item.value for item in Algorithms.Functions), f"Invalid function type {function}."
        n = len(array)  # N

        @lru_cache(maxsize=1024)
        def populate_logs_lut():
            """
            """
            logs = [0] * (n + 1)  # logs lut for floor(log(i)), 1 <= i <= N, index 0 unused
            for k in range(2, n + 1):
                logs[k] = logs[k//2] + 1
            return logs

        def build_luts():
            """
            Builds Sparse and Indices tables. Tables are cached for performance.
            """
            # populate the first row of luts
            p = math.floor(math.log2(n))  # P, row decimal_digit_number, the largest 2^P which fits in N
            sparse_table = [[float('-inf')] * n for _ in range(p + 1)]  # sparse table, P+1 rows and N columns
            indices_table = [[0] * n for _ in range(p + 1)]  # indices table, P+1 rows and N columns
            for k in range(0, n):
                sparse_table[0][k] = array[k]
                indices_table[0][k] = k
            # populate luts
            for pk in range(1, p + 1):
                k = 0
                while True:
                    if (k + (1 << pk)) > n:
                        break
                    lhs = sparse_table[pk - 1][k]
                    rhs = sparse_table[pk - 1][k + (1 << (pk - 1))]
                    if function == Algorithms.Functions.MIN:
                        sparse_table[pk][k] = min(lhs, rhs)
                        if lhs <= rhs:
                            indices_table[pk][k] = indices_table[pk - 1][k]
                        else:
                            indices_table[pk][k] = indices_table[pk - 1][k + (1 << (pk - 1))]
                    elif function == Algorithms.Functions.MAX:
                        sparse_table[pk][k] = max(lhs, rhs)
                        if lhs >= rhs:
                            indices_table[pk][k] = indices_table[pk - 1][k]
                        else:
                            indices_table[pk][k] = indices_table[pk - 1][k + (1 << (pk - 1))]
                    # indices ...
                    k += 1
            return sparse_table, indices_table

        logs_lut = populate_logs_lut()
        table, indices = build_luts()

        def min_value_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            return min(lhs, rhs)

        def max_value_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            return max(lhs, rhs)

        def min_index_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            if lhs <= rhs:
                index = indices[pk][lb]
            else:
                index = indices[pk][rb - k + 1]
            return index

        def max_index_query(lb, rb):
            pk = logs_lut[rb - lb + 1]
            k = 1 << pk
            lhs = table[pk][lb]
            rhs = table[pk][rb - k + 1]
            if lhs >= rhs:
                index = indices[pk][lb]
            else:
                index = indices[pk][rb - k + 1]
            return index

        result = list()
        for query in queries:
            if function == Algorithms.Functions.MIN:
                result.append((min_value_query(query[0], query[1]),
                               min_index_query(query[0], query[1])))
            elif function == Algorithms.Functions.MAX:
                result.append((max_value_query(query[0], query[1]),
                               max_index_query(query[0], query[1])))
        return result

    @staticmethod
    def merge_intervals(intervals):
        """
        Based on leetcode.com/problems/merge-intervals/solutions/4995042/efficient-easy-in-place-o-1-space
        Interval: [start : end]
        start, end might be negative
        """  # noqa
        def normalize(intervals):  # noqa
            """
            normalize intervals - start <= end
            """
            for interval in intervals:
                if interval[0] > interval[1]:
                    interval[1], interval[0] = interval[0], interval[1]

        def rearrange(intervals):  # noqa
            """
            sort by start
            """
            intervals.sort(key=lambda interval: interval[0])

        if not intervals:
            return intervals
        n = len(intervals)
        if n < 2:
            return intervals
        normalize(intervals)
        rearrange(intervals)
        k = 1  # start from the second interval
        while k < n:
            if intervals[k][0] <= intervals[k - 1][1]:  # start2 <= end1
                intervals[k - 1][1] = max(intervals[k - 1][1], intervals[k][1])  # max of ends
                intervals.pop(k)  # removed consumed interval
                n -= 1
            else:
                k += 1
        return intervals

    @staticmethod
    def calculate_alignment_up(value, alignment):
        """
        """
        # align value 'value' to boundary 'alignment' which should be power of 2
        return (value + (alignment - 1)) & ~(alignment - 1)  # up

    @staticmethod
    def calculate_alignment_down(value, alignment):
        """
        """
        # align value 'value' to boundary 'alignment' which should be power of 2
        return int(value & ~(alignment - 1))  # down

    @staticmethod
    def max_pow2_less(n):
        """
        """
        result = 0
        for k in reversed(range(0, n)):
            if (k & (k - 1)) == 0:
                result = k
                break
        return result

    @staticmethod
    def integer_log2(n):
        """
        https://www.boost.org/doc/libs/1_58_0/boost/integer/integer_log2.hpp
        """  # noqa
        mxpo2ls = Algorithms.max_pow2_less(n)  # noqa
        result = 0
        while n != 1:
            t = n >> mxpo2ls
            if t:
                result += mxpo2ls
                n = t
            mxpo2ls //= 2
        return result
