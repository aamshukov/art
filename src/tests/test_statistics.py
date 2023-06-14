#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.statistics.statistics import (NUMBER_OF_LEXEMES,
                                                          NUMBER_OF_KEYWORDS,
                                                          NUMBER_OF_IDENTIFIERS)


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_statistics(self):
        statistics = Statistics()
        statistics.update_stats(Token(TokenKind.IDENTIFIER))
        statistics.update_stats(Token(TokenKind.BOOLEAN))
        assert statistics.quantities[NUMBER_OF_LEXEMES] == 2
        assert statistics.quantities[NUMBER_OF_KEYWORDS] == 1
        assert statistics.quantities[NUMBER_OF_IDENTIFIERS] == 1


if __name__ == '__main__':
    """
    """
    unittest.main()
