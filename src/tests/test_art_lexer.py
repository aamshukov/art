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

    def test_skip_whitespace_success(self):
        dp = StringDataProvider('')
        data = dp.load()
        content = Content(0, data, '')
        diagnostics = Diagnostics()
        statistics = Statistics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        tokenizer.skip_whitespace()
        assert tokenizer.codepoint == Text.eos_codepoint()
        dp = StringDataProvider(' ')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        tokenizer.skip_whitespace()
        assert tokenizer.codepoint == Text.eos_codepoint()
        dp = StringDataProvider('  ')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        tokenizer.skip_whitespace()
        dp = StringDataProvider('A ')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        tokenizer.skip_whitespace()
        assert tokenizer.character == 'A'
        tokenizer.skip_whitespace()
        dp = StringDataProvider('AB ')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        tokenizer.skip_whitespace()
        assert tokenizer.character == 'A'
        tokenizer.skip_whitespace()
        assert tokenizer.character == 'A'
        tokenizer.next_lexeme()
        tokenizer.skip_whitespace()
        # assert tokenizer.codepoint == Text.eos_codepoint() ??
        # dp = StringDataProvider(' A  သည်  B  C 🐍 သည်    ')
        # data = dp.load()
        # content = Content(0, data, '')
        # tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == 'A'
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == 'သ'
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == 'B'
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == 'C'
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == '🐍'
        # tokenizer.skip_whitespace()
        # assert tokenizer.character == 'သ'
        # tokenizer.skip_whitespace()
        # assert tokenizer.codepoint == Text.eos_codepoint()
        # tokenizer.skip_whitespace()
        # assert tokenizer.codepoint == Text.eos_codepoint()

    def test_identifier_start_success(self):
        assert ArtTokenizer.identifier_start(ord('a'))
        assert ArtTokenizer.identifier_start(ord('_'))
        assert ArtTokenizer.identifier_start(ord('$'))
        assert ArtTokenizer.identifier_start(ord('﹍'))
        assert ArtTokenizer.identifier_start(ord('Я'))
        assert ArtTokenizer.identifier_start(ord('彡'))
        assert ArtTokenizer.identifier_start(ord('ಠ'))
        assert ArtTokenizer.identifier_start(ord('益'))
        assert ArtTokenizer.identifier_start(ord('什'))
        assert ArtTokenizer.identifier_start(ord('သ'))

    def test_identifier_part_success(self):
        assert ArtTokenizer.identifier_part(ord('a'))
        assert ArtTokenizer.identifier_part(ord('_'))
        assert ArtTokenizer.identifier_part(ord('$'))
        assert ArtTokenizer.identifier_part(ord('﹍'))
        assert ArtTokenizer.identifier_part(ord('Я'))
        assert ArtTokenizer.identifier_part(ord('彡'))
        assert ArtTokenizer.identifier_part(ord('ಠ'))
        assert ArtTokenizer.identifier_part(ord('益'))
        assert ArtTokenizer.identifier_part(ord('什'))
        assert ArtTokenizer.identifier_part(ord('်'))


if __name__ == '__main__':
    """
    """
    unittest.main()
