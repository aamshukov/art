#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.core.diagnostics import Diagnostics
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.token.tokenizer import Tokenizer
from art.language.art.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    def test_lexical_analyzer_success(self):
        dp = StringDataProvider('')
        data = dp.load()
        content = Content(0, data, '')
        diagnostics = Diagnostics()
        statistics = Statistics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        k = 0
        # while lexer.next_lexeme().kind != lexer.eos():
        #     token = lexer.token
        #     match k:
        #         case 0:
        #             pass
        assert True


if __name__ == '__main__':
    """
    """
    unittest.main()
