#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import math
import random
import unittest
from art.framework.core.compression.pf import Pf
from art.framework.core.transformation.bwt.bwt import Bwt
from art.framework.core.utils.helper import DomainHelper


class Test(unittest.TestCase):
    def test_pf_unrank_success(self):
        p1, p2, v = Pf.unrank(10)
        print(p1)
        print(p2)
        print(v)
        assert p1 == [3, 0, 1, 2]
        assert p2 == [2, 3, 0, 1]
        assert v == [1, 1, 0, 1, 1]

    def test_pf_unrank_15_success(self):
        n = math.factorial(8)
        for k in range(n):
            p1, p2, v = Pf.unrank(k)
            print(f'Iteration: {k}')
            print(p1)
            print(p2)
            print(v)
            print()

    def test_pf_unrank_bwt_success(self):
        n = math.factorial(8)
        ppv = list()
        for k in range(n):
            p1, p2, v = Pf.unrank(k)
            ppv.extend(v)
        ppv = list(map(lambda e: str(e), ppv))
        ppv = ''.join(ppv)
        print(ppv)
        bwt = Bwt.encode(ppv)
        bwt = ''.join(bwt)
        print(bwt)

    @staticmethod
    def pf_unrank_bwt_from_file(offset, n):
        ppv = list()
        with(open(r"D:\Tmp\pf.dat", mode="rb")) as stream:
            stream.seek(offset, 0)
            for _ in range(n):
                байты = stream.read(8 * 15)  # noqa
                for k in range(8):
                    number = 0
                    bits = 0
                    for bit in DomainHelper.bits(байты):
                        number = (number << 1) | bit
                        bits += 1
                        if bits == 15:
                            p1, p2, v = Pf.unrank(number)
                            ppv.extend(v)
                            number = 0
                            bits = 0
        ppv = list(map(lambda e: str(e), ppv))
        ppv = ''.join(ppv)
        print(f'ppv len: {len(ppv)}')
        print(ppv)
        bwt = Bwt.encode(ppv)
        bwt = ''.join(bwt)
        print(f'bwt len: {len(bwt)}')
        print(bwt)
        ppv2 = Bwt.decode(bwt)
        print(f'ppv2 len: {len(ppv2)}')
        print(ppv2)
        assert ppv2 == ppv
        bwt = bwt.replace('$', '')
        rle, max_v = Pf.rle(bwt)
        print(f'rle len: {len(rle)}, max value: {max_v}')
        print(rle)

    def test_pf_unrank_bwt_from_file_success(self):
        Test.pf_unrank_bwt_from_file(0, 2)

    def test_pf_unrank_bwt_from_file_random_success(self):
        for _ in range(100):
            random.seed()
            offset = random.randint(0, 16263761)
            Test.pf_unrank_bwt_from_file(offset, 2)


if __name__ == '__main__':
    """
    """
    unittest.main()
