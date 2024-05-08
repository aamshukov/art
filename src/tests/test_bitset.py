#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.adt.bitset.bitset import BitSet


class Test(unittest.TestCase):
    def test_bitset_0_success(self):
        bitset = BitSet(0)
        assert True


if __name__ == '__main__':
    """
    """
    unittest.main()
