#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest

from art.framework.core.diagnostics.code import Code
from art.framework.core.diagnostics.status import Status
from art.framework.core.diagnostics.diagnostics import Diagnostics


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_diagnostics_success(self):
        diagnostics = Diagnostics()
        diagnostics.add(Status(messages='SUCCESS', custom_code=Code.Success))
        diagnostics.add(Status(messages='INFORMATION', custom_code=Code.Information))
        diagnostics.add(Status(messages='WARNING', custom_code=Code.Warning))
        diagnostics.add(Status(messages='ERROR', custom_code=Code.Error))
        diagnostics.add(Status(messages='FATAL_ERROR', custom_code=Code.FatalError))
        assert len(diagnostics.successes) == 1
        assert len(diagnostics.infos) == 1
        assert len(diagnostics.warnings) == 1
        assert len(diagnostics.errors) == 1
        assert len(diagnostics.fatal_errors) == 1


if __name__ == '__main__':
    """
    """
    unittest.main()
