#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.core.domain_helper import DomainHelper
from art.framework.frontend.fsa.fsa import Fsa


class Test(unittest.TestCase):
    DOT_PATH = r'd:\tmp\{}.txt'

    def test_fsa_success(self):
        fsa = Fsa(0)
        dot_path = Test.DOT_PATH.format(self.id().split('.')[-1])
        fsa.generate_graphviz_content(dot_path)
        assert os.path.exists(dot_path)


if __name__ == '__main__':
    """
    """
    unittest.main()
