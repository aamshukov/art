#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.diagnostics.status import Status
from art.framework.core.diagnostics.diagnostics import Diagnostics


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_diagnostics_success(self):
        diagnostics = Diagnostics()
        diagnostics.add(Status('SUCCESS', '', Status.SUCCESS))
        diagnostics.add(Status('INFO', '', Status.INFO))
        diagnostics.add(Status('WARNING', '', Status.WARNING))
        diagnostics.add(Status('ERROR', '', Status.ERROR))
        diagnostics.add(Status('FATAL_ERROR', '', Status.FATAL_ERROR))
        assert len(diagnostics.successes) == 1
        assert len(diagnostics.infos) == 1
        assert len(diagnostics.warnings) == 1
        assert len(diagnostics.errors) == 1
        assert len(diagnostics.fatal_errors) == 1


if __name__ == '__main__':
    """
    """
    unittest.main()
