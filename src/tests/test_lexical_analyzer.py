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


class Test(unittest.TestCase):
    class TestTokenizer(Tokenizer):
        def __init__(self, id, content, version='1.0'):
            super().__init__(id, content, Statistics(), Diagnostics(), version=version)
            self._k = 0

        def inc_k(self):
            self._k += 1

        def dec_k(self):
            self._k -= 1

        def next_lexeme_impl(self):
            match self._k:
                case 0:
                    self._content_position = 1
                    self._token = Token(TokenKind.IDENTIFIER)
                case 1:
                    self._content_position = 2
                    self._token = Token(TokenKind.WS)
                case 2:
                    self._content_position = 3
                    self._token = Token(TokenKind.EQUAL)
                case 3:
                    self._content_position = 4
                    self._token = Token(TokenKind.WS)
                case 4:
                    self._content_position = 5
                    self._token = Token(TokenKind.LEFT_PARENTHESIS)
                case 5:
                    self._content_position = 8
                    self._token = Token(TokenKind.IDENTIFIER)
                case 6:
                    self._content_position = 9
                    self._token = Token(TokenKind.WS)
                case 7:
                    self._content_position = 10
                    self._token = Token(TokenKind.PLUS_SIGN)
                case 8:
                    self._content_position = 11
                    self._token = Token(TokenKind.WS)
                case 9:
                    self._content_position = 18
                    self._token = Token(TokenKind.IDENTIFIER)
                case 10:
                    self._content_position = 19
                    self._token = Token(TokenKind.RIGHT_PARENTHESIS)
                case 11:
                    self._content_position = 20
                    self._token = Token(TokenKind.GREATER_EQUAL)
                case _:
                    self._token = Token(TokenKind.EOS)
            self._k += 1

    class TestLexicalAnalyzer(LexicalAnalyzer):
        def __init__(self, id, tokenizer, version='1.0'):
            super().__init__(id,
                             tokenizer,
                             Statistics(),
                             Diagnostics(),
                             version=version)

    def __init__(self, *args, **kwargs):
        """
        p = (abc + boofoo)>=
        """
        super(Test, self).__init__(*args, **kwargs)

    def test_lexical_analyzer_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert data == content.data
        tokenizer = Test.TestTokenizer(0, content)
        lexer = Test.TestLexicalAnalyzer(0, tokenizer)
        assert content.data == tokenizer.content.data
        assert content == tokenizer.content

    def test_lexical_analyzer_tokens_success(self):
        def assert_token(lx, tk, kind, prev_kind, offset, length, literal, tokens_count):
            assert tk.kind == kind
            assert tk.offset == offset
            assert tk.length == length
            assert Text.equal(tk.literal, literal)
            assert lx.prev_token.kind == prev_kind

        dp = StringDataProvider('p = (abc + boofoo)>=')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        lexer = Test.TestLexicalAnalyzer(0, tokenizer)
        token = lexer.next_lexeme()
        assert_token(lexer, token, TokenKind.IDENTIFIER, TokenKind.UNKNOWN, 0, 1, 'p', 0)
        token = lexer.next_lexeme()
        assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 0)
        la_token = lexer.lookahead_lexeme()
        assert_token(lexer, la_token, TokenKind.EQUAL, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 1)
        la_token = lexer.lookahead_lexeme()
        assert_token(lexer, la_token, TokenKind.WS, TokenKind.IDENTIFIER, 3, 1, ' ', 2)
        assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 2)
        la_token = lexer.lookahead_lexeme()
        assert_token(lexer, la_token, TokenKind.LEFT_PARENTHESIS, TokenKind.IDENTIFIER, 4, 1, '(', 3)
        assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 3)
        tokenizer.dec_k()
        tokenizer.dec_k()
        tokenizer.dec_k()
        token = lexer.next_lexeme()
        assert_token(lexer, token, TokenKind.EQUAL, TokenKind.WS, 2, 1, '=', 2)
        token = lexer.next_lexeme()
        assert_token(lexer, token, TokenKind.WS, TokenKind.EQUAL, 3, 1, ' ', 1)
        tokenizer.inc_k()
        tokenizer.inc_k()
        la_token = lexer.lookahead_lexeme()
        la_token = lexer.lookahead_lexeme()
        tokenizer.dec_k()
        tokenizer.dec_k()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        tokenizer.dec_k()
        tokenizer.dec_k()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        tokenizer.dec_k()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        # after this EOS
        la_token = lexer.lookahead_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()


if __name__ == '__main__':
    """
    """
    unittest.main()
