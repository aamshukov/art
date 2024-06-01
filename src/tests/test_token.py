#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text.text import Text
from art.framework.frontend.lexical_analyzer.tokenizer.token import Token
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_token_name_success(self):
        token = Token(TokenKind.BOOLEAN_KW)
        print(token)
        assert token.kind == TokenKind.BOOLEAN_KW
        assert Text.equal(token.label, TokenKind.BOOLEAN_KW.name)

    def test_token_new_success(self):
        token1 = Token(TokenKind.BOOLEAN_KW)
        token2 = token1
        assert token1 == token2
        token1 = Token(TokenKind.CASE_KW)
        assert token1.kind == TokenKind.CASE_KW
        assert Text.equal(token1.label, TokenKind.CASE_KW.name)
        assert token2.kind == TokenKind.BOOLEAN_KW
        assert Text.equal(token2.label, TokenKind.BOOLEAN_KW.name)
        st1 = str(token1)
        print(st1)
        assert st1 == "Token:1.0:CASE_KW         : '', 'Location:0:0:', Flags.CLEAR|GENUINE"


if __name__ == '__main__':
    """
    """
    unittest.main()
