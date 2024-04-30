#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.compression.pf.pf import Pf


class Test(unittest.TestCase):
    def test_rle_success(self):
        bits = '1010111000'
        print(bits)
        rle_encoded, max_v = Pf.rle_encode(bits)
        print(f'rle_encode len: {len(rle_encoded)}, max value: {max_v}')
        print(rle_encoded)
        rle_decoded = Pf.rle_decode(rle_encoded, max_v, bits[0] == '0')
        rle_decoded = list(map(lambda e: str(e), rle_decoded))
        rle_decoded = ''.join(rle_decoded)
        print(rle_decoded)
        assert rle_decoded == bits

    def test_rle2_success(self):
        bits = '11111111111111111111111111111111100000000000000001111111100000000000000000000000011111111111111110000000011111111111111110000000000000000111111111111111111111111111111111111111100000000111111111111111100000000000000001111111111111111111111111111111111111111111111111111111111111111000000001111111111111111111111110000000000000000000000001111111111111111000000001111111101111111100000000000000011111111000000001111111100000000000000001111111111111111111111111111111111111111111111110000000011111111000000000000000000000000111111110000000011111111000000000000000011111111000000000000000011111111000000000000000011111111000000000000000011111111111111111111111100000000111111110000000011111111000000001111111111111111111111110000000000000000111111111111111111111111000000001111111100000000000000000000000000000000111111111111111111111111111111111111111111111111000000001111111111111111111111111111111100000000111111111111111111111111111111111111111111111111111111111111111101111111111111111000000001111111111111111111111111111111111111111111111110000000000000000000000011111111111111111111111111111111000000000000000011111111000000001111111100000000000000000000000011111111000000000000000011111111111111110000000011111111000000000000000011111111000000000000000000000000000000000000000011111111111111110000000000000000111111110000000010000000011111111111111111111111100000000111111111111111111111111000000000000000011111111111111111111111111111111111111111111111111111111111111110000000000000000111111110000000000000000111111111111111100000000111111100000000111111110000000011111111111111111111111111111111111111111000000000000000011111111111111111111111111111111111111110000000000000000000000001111111111111111000000000000000011111111000000001111111111111111000000000000000011111111111111110000000011111111111111111111111111111111000000001111111111111111111111111111111111111111111111111111111100000000111111111111111111111111111111110000000000000000111111110000000011111111111111110000000011111111111111111111111100000000000000000000000000000000111111110000000000000000111111110000000011111111000000001111111111111111000000001111111111111111111111111111111100000000000000001111111111111110000000000000000000000000000000000000000000000000000000011111111000000000000000000000000000000001111111111111111111111111111111111111111111111110000000000000000011111111111111110000000011111111111111111111111111111111000000000000000000000000000000001111111100000000000000000000000011111111000000000000000111111111111111110000000011111111111111110000000011111111000000001111111100000000111111111111111100000000000000000000000011111111111111111111111100000000000000001111111100000000000000001111111100000000111111111111111111111111000000000000000000000000111111110000000011111111111111110000000011111111111111111111111111111111111111111111111100000000000000000000000000000000000000000000000011111110000000011111111000000000000000000000000000000001111111100000000111111110000000000000000000000000000000011111111111111110000000000000000011111111111111110000000000000000111111110000000011111111000000001111111100000000111111110000000000000000111111110000000000000000000000000000000000000000000000000000000000000000000000000000000011111110000000000000000000000000000000000000000111111110000000011111111000000000000000000000000111111110000000000000000000000000000000'  # noqa
        print(bits)
        rle_encoded, max_v = Pf.rle_encode(bits)
        print(f'rle_encode len: {len(rle_encoded)}, max value: {max_v}')
        print(rle_encoded)
        rle_decoded = Pf.rle_decode(rle_encoded, max_v, bits[0] == '0')
        rle_decoded = list(map(lambda e: str(e), rle_decoded))
        rle_decoded = ''.join(rle_decoded)
        print(rle_decoded)
        assert rle_decoded == bits


if __name__ == '__main__':
    """
    """
    unittest.main()