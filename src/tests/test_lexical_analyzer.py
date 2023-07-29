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
from art.framework.frontend.lexical_analyzer.tokenizer.token import Token
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.lexical_analyzer.tokenizer.tokenizer import Tokenizer


class Test(unittest.TestCase):
    class TestTokenizer(Tokenizer):
        def __init__(self, id, content, version='1.0'):
            super().__init__(id, content, Statistics(), Diagnostics(), version=version)
            self.k = 0

        def inc_k(self):
            self.k += 1

        def dec_k(self):
            self.k -= 1

        def validate(self):
            raise NotImplemented(self.validate.__qualname__)

        def next_lexeme_impl(self):
            match self.k:
                case 0:
                    self.content_position = 1
                    self.token = Token(TokenKind.IDENTIFIER)
                case 1:
                    self.content_position = 2
                    self.token = Token(TokenKind.WS)
                case 2:
                    self.content_position = 3
                    self.token = Token(TokenKind.EQUALS_SIGN)
                case 3:
                    self.content_position = 4
                    self.token = Token(TokenKind.WS)
                case 4:
                    self.content_position = 5
                    self.token = Token(TokenKind.LEFT_PARENTHESIS)
                case 5:
                    self.content_position = 8
                    self.token = Token(TokenKind.IDENTIFIER)
                case 6:
                    self.content_position = 9
                    self.token = Token(TokenKind.WS)
                case 7:
                    self.content_position = 10
                    self.token = Token(TokenKind.PLUS_SIGN)
                case 8:
                    self.content_position = 11
                    self.token = Token(TokenKind.WS)
                case 9:
                    self.content_position = 18
                    self.token = Token(TokenKind.IDENTIFIER)
                case 10:
                    self.content_position = 19
                    self.token = Token(TokenKind.RIGHT_PARENTHESIS)
                case 11:
                    self.content_position = 20
                    self.token = Token(TokenKind.GREATER_THAN_OR_EQUAL)
                case _:
                    self.token = Token(TokenKind.EOS)
            self.k += 1

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

    @staticmethod
    def assert_token(lx, tk, kind, prev_kind, offset, length, literal, tokens_count):
        assert tk.kind == kind
        assert tk.offset == offset
        assert tk.length == length
        assert Text.equal(tk.literal, literal)
        assert lx.prev_token.kind == prev_kind

    def test_lexical_analyzer_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(data, '')
        assert len(data) == content.count
        assert data == content.data
        tokenizer = Test.TestTokenizer(0, content)
        lexer = Test.TestLexicalAnalyzer(0, tokenizer)
        assert content.data == tokenizer.content.data
        assert content == tokenizer.content

    def test_lexical_analyzer_tokens_success(self):
        dp = StringDataProvider('p = (abc + boofoo)>=')
        data = dp.load()
        content = Content(data, '')
        tokenizer = Test.TestTokenizer(0, content)
        lexer = Test.TestLexicalAnalyzer(0, tokenizer)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.IDENTIFIER, TokenKind.UNKNOWN, 0, 1, 'p', 0)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 0)
        la_token = lexer.lookahead_lexeme()
        Test.assert_token(lexer, la_token, TokenKind.EQUALS_SIGN, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 1)
        la_token = lexer.lookahead_lexeme()
        Test.assert_token(lexer, la_token, TokenKind.EQUALS_SIGN, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        la_token = lexer.lookahead_lexeme()
        Test.assert_token(lexer, la_token, TokenKind.EQUALS_SIGN, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        la_tokens = lexer.lookahead_lexemes(2)
        Test.assert_token(lexer, la_tokens[0], TokenKind.EQUALS_SIGN, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        Test.assert_token(lexer, la_tokens[1], TokenKind.WS, TokenKind.IDENTIFIER, 3, 1, ' ', 2)
        la_tokens = lexer.lookahead_lexemes(2)
        Test.assert_token(lexer, la_tokens[0], TokenKind.EQUALS_SIGN, TokenKind.IDENTIFIER, 2, 1, '=', 1)
        Test.assert_token(lexer, la_tokens[1], TokenKind.WS, TokenKind.IDENTIFIER, 3, 1, ' ', 2)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.EQUALS_SIGN, TokenKind.WS, 2, 1, '=', 1)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.EQUALS_SIGN, 3, 1, ' ', 2)
        la_token = lexer.lookahead_lexeme()
        Test.assert_token(lexer, la_token, TokenKind.LEFT_PARENTHESIS, TokenKind.EQUALS_SIGN, 4, 1, '(', 3)
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.EQUALS_SIGN, 3, 1, ' ', 2)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.LEFT_PARENTHESIS, TokenKind.WS, 4, 1, '(', 3)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.IDENTIFIER, TokenKind.LEFT_PARENTHESIS, 5, 3, 'abc', 1)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 8, 1, ' ', 1)
        la_tokens = lexer.lookahead_lexemes(1)
        la_tokens = lexer.lookahead_lexemes(2)
        la_tokens = lexer.lookahead_lexemes(3)
        la_tokens = lexer.lookahead_lexemes(4)
        la_tokens = lexer.lookahead_lexemes(10)
        assert len(la_tokens) == 10
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.PLUS_SIGN, TokenKind.WS, 9, 1, '+', 1)
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
        assert token.kind == TokenKind.EOS
        la_token = lexer.lookahead_lexeme()
        assert token.kind == TokenKind.EOS
        token = lexer.next_lexeme()
        assert token.kind == TokenKind.EOS
        token = lexer.next_lexeme()
        assert token.kind == TokenKind.EOS

    def test_lexical_analyzer_tokens_skip_success(self):
        dp = StringDataProvider('p = (abc + boofoo)>=')
        data = dp.load()
        content = Content(data, '')
        tokenizer = Test.TestTokenizer(0, content)
        lexer = Test.TestLexicalAnalyzer(0, tokenizer)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.IDENTIFIER, TokenKind.UNKNOWN, 0, 1, 'p', 0)
        la_token = lexer.lookahead_lexeme(skip=[TokenKind.WS])
        Test.assert_token(lexer, la_token, TokenKind.EQUALS_SIGN, TokenKind.UNKNOWN, 2, 1, '=', 0)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 1, 1, ' ', 0)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.EQUALS_SIGN, TokenKind.WS, 2, 1, '=', 1)
        la_tokens = lexer.lookahead_lexemes(1)
        la_tokens = lexer.lookahead_lexemes(2)
        la_tokens = lexer.lookahead_lexemes(3)
        la_token = lexer.lookahead_lexeme(skip=[TokenKind.WS])
        Test.assert_token(lexer, la_token, TokenKind.LEFT_PARENTHESIS, TokenKind.WS, 4, 1, '(', 0)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.EQUALS_SIGN, 3, 1, ' ', 1)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.LEFT_PARENTHESIS, TokenKind.WS, 4, 1, '(', 1)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.IDENTIFIER, TokenKind.LEFT_PARENTHESIS, 5, 3, 'abc', 1)
        token = lexer.next_lexeme()
        Test.assert_token(lexer, token, TokenKind.WS, TokenKind.IDENTIFIER, 8, 1, ' ', 1)


if __name__ == '__main__':
    """
    """
    unittest.main()
