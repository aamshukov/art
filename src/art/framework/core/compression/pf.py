#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Permutation fantasy based compression """
from art.framework.core.algorithm.permutation import Permutation
from art.framework.core.domain.base import Base


class Pf(Base):
    """
    """

    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self.version = version.strip()

    def encode(self, raw_data=None):
        """
        """
        data = list() if raw_data is None else raw_data
        result = data
        return result

    def decode(self, compressed_data):
        """
        """
        data = list() if compressed_data is None else compressed_data
        result = data
        return result

    @staticmethod
    def rank(p1, p2, v, size=8):
        """
        """
        rank = Permutation.rank(permutation)
        return rank

    @staticmethod
    def unrank(rank, size=8):
        """
        """
        p = Permutation.unrank(rank, size)
        p1 = list()
        p2 = list()
        v = list()
        n = size // 2
        ones = 0
        zeroes = 0
        for e in p:
            if e < n:
                p1.append(e)
                if zeroes < n and ones < n:
                    v.append(0)
                    zeroes += 1
            else:
                p2.append(e - n)
                if zeroes < n and ones < n:
                    v.append(1)
                    ones += 1
        return p1, p2, v

    @staticmethod
    def rle(bits):
        """
        """
        ones = 0
        zeroes = 0
        max_v = 0
        rle = list()
        for bit in bits:
            if bit == '0':
                if ones:
                    rle.append(ones - 1)
                    if ones > max_v:
                        max_v = ones
                    ones = 0
                zeroes += 1
            else:
                if zeroes:
                    rle.append(zeroes - 1)
                    if zeroes > max_v:
                        max_v = zeroes
                    zeroes = 0
                ones += 1
        return rle, max_v
