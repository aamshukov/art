#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer


class Test(unittest.TestCase):
    TOKENS = list()

    class TestLexicalAnalyzer(LexicalAnalyzer):
        def __init__(self, id, content, version='1.0'):
            super().__init__(id, content, version=version)
            self._k = 0
            self._n = len(Test.TOKENS)

        def next_lexeme_impl(self):
            self._token = Test.TOKENS[self._k]
            match self._k:
                case 0:
                    self._content_position = 1
                    self._token.kind = TokenKind.IDENTIFIER
                case 1:
                    self._content_position = 2
                    self._token.kind = TokenKind.WS
                case 2:
                    self._content_position = 3
                    self._token.kind = TokenKind.ASSIGNMENT
                case 3:
                    self._content_position = 4
                    self._token.kind = TokenKind.WS
                case 4:
                    self._content_position = 5
                    self._token.kind = TokenKind.OPEN_PAREN
                case 5:
                    self._content_position = 8
                    self._token.kind = TokenKind.IDENTIFIER
                case 6:
                    self._content_position = 9
                    self._token.kind = TokenKind.WS
                case 7:
                    self._content_position = 10
                    self._token.kind = TokenKind.PLUS
                case 8:
                    self._content_position = 11
                    self._token.kind = TokenKind.WS
                case 9:
                    self._content_position = 18
                    self._token.kind = TokenKind.IDENTIFIER
                case 10:
                    self._content_position = 19
                    self._token.kind = TokenKind.CLOSE_PAREN
                case 11:
                    self._content_position = 21
                    self._token.kind = TokenKind.GREATER_EQUAL
            self._k += 1
            if self._k == self._n:
                self._k = 0

    def __init__(self, *args, **kwargs):
        """
        p = (abc + boofoo)>=
        """
        super(Test, self).__init__(*args, **kwargs)
        Test.TOKENS.append(Token(TokenKind.IDENTIFIER))
        Test.TOKENS.append(Token(TokenKind.WS))
        Test.TOKENS.append(Token(TokenKind.ASSIGNMENT))
        Test.TOKENS.append(Token(TokenKind.WS))
        Test.TOKENS.append(Token(TokenKind.OPEN_PAREN))
        Test.TOKENS.append(Token(TokenKind.IDENTIFIER))
        Test.TOKENS.append(Token(TokenKind.WS))
        Test.TOKENS.append(Token(TokenKind.PLUS))
        Test.TOKENS.append(Token(TokenKind.WS))
        Test.TOKENS.append(Token(TokenKind.IDENTIFIER))
        Test.TOKENS.append(Token(TokenKind.CLOSE_PAREN))
        Test.TOKENS.append(Token(TokenKind.GREATER_EQUAL))

    def test_lexical_analyzer_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        lexer = Test.TestLexicalAnalyzer(0, content)
        assert Text.equal(content.data, lexer.content.data)
        assert content == lexer.content

    def test_lexical_analyzer_tokens_success(self):
        dp = StringDataProvider('p = (abc + boofoo)>=')
        data = dp.load()
        content = Content(0, data, '')
        lexer = Test.TestLexicalAnalyzer(0, content)
        assert Text.equal(content.data, lexer.content.data)
        assert content == lexer.content
        token = lexer.next_lexeme()
        assert token.kind == TokenKind.IDENTIFIER
        assert token.offset == 0
        assert token.length == 1
        assert token.literal == 'p'
        assert len(lexer.tokens) == 0
        assert lexer.prev_token == token
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        la_token = lexer.lookahead_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        token = lexer.next_lexeme()
        la_token = lexer.lookahead_lexeme()
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
