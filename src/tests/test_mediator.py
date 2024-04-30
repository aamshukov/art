#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest

from art.framework.core.configuration.configuration import Configuration
from art.framework.core.logging.logger import Logger
from art.framework.core.patterns.mediator.mediator import Mediator
from art.framework.core.patterns.mediator.messages.command import Command


class Test(unittest.TestCase):
    def test_mediator_domain(self):
        command = Command('1')
        assert type(command) is Command

    def test_mediator(self):
        configuration = Configuration()
        logger = Logger()
        mediator = Mediator(configuration, logger)
        assert True


if __name__ == '__main__':
    """
    """
    unittest.main()
