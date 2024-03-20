#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.algorithm.unification import Unification


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_unification_success(self):
        unification = Unification()
        unification.unify('', '')


if __name__ == '__main__':
    """
    """
    unittest.main()
