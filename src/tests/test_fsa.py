#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.frontend.fsa.fsa import Fsa
from art.framework.frontend.fsa.fsa_state import FsaState


class Test(unittest.TestCase):
    DOT_PATH = 'd:/tmp/art/'
    DOT_FILE = '{}/{}.dot'

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        if not os.path.exists(Test.DOT_PATH):
            os.makedirs(Test.DOT_PATH)

    def test_fsa_success(self):
        fsa = Fsa(0)
        s1 = FsaState(1, '1', 1)
        s2 = FsaState(2, '2', 2)
        fsa.start_state = s1
        fsa.add_state(s1)
        fsa.add_state(s2)
        fsa.add_final_state(s2)
        fsa.add_transition(s1, s2, 's1-s2')
        dot_path = Test.DOT_FILE.format(Test.DOT_PATH, self.id().split('.')[-1])
        fsa.generate_graphviz_content(dot_path)
        assert os.path.exists(dot_path)
        # for %i in (d:\tmp\art\*.dot) do D:\Soft\graphviz\2.38\release\bin\dot -Tpng %i -o %i.png


if __name__ == '__main__':
    """
    """
    unittest.main()
