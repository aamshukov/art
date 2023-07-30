#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.core.flags import Flags
from art.framework.core.logger import Logger
from art.framework.core.domain_helper import DomainHelper
from art.framework.core.platform import Platform


class Test(unittest.TestCase):
    def test_logger_success(self):
        path = r'd:\tmp'
        logger = Logger(path=path)
        logger.debug('kuku')
        assert os.path.exists(os.path.join(path, f'{Logger.LOGGER_NAME}.log'))

    def test_modify_flags_success(self):
        flags = Flags.DIRTY | Flags.PROCESSED | Flags.VISITED | Flags.LEAF | Flags.INVALID
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.PROCESSED == Flags.PROCESSED
        assert flags & Flags.VISITED == Flags.VISITED
        assert flags & Flags.LEAF == Flags.LEAF
        assert flags & Flags.INVALID == Flags.INVALID
        flags = Flags.modify_flags(flags,
                                   Flags.GENUINE | Flags.SYNTHETIC, Flags.PROCESSED | Flags.VISITED | Flags.INVALID)
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.GENUINE == Flags.GENUINE
        assert flags & Flags.SYNTHETIC == Flags.SYNTHETIC

    def test_epsilon_success(self):
        assert DomainHelper.real_numbers_equal(0.0, 0.0)
        assert DomainHelper.real_numbers_equal(Platform.epsilon(), Platform.epsilon())
        assert DomainHelper.real_numbers_equal(0.1, 0.1)
        assert not DomainHelper.real_numbers_equal(0.0000001, 0.00010001)
        assert DomainHelper.real_numbers_equal(47264780.00027800001, 47264780.00027800001)
        assert DomainHelper.real_numbers_equal(47264780E+27, 47264780E+27)
        assert DomainHelper.real_numbers_equal(47264780E-28, 47264780E-27)


if __name__ == '__main__':
    """
    """
    unittest.main()
