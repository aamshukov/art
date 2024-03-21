#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.core.adt.graph.vertex import Vertex


class Test(unittest.TestCase):
    def test_repr_str_success(self):
        vertex = Vertex(1, "odin")
        repr1 = repr(vertex)
        str1 = str(vertex)
        assert repr1 == str1


if __name__ == '__main__':
    """
    """
    unittest.main()
