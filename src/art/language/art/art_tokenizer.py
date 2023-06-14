# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Tokenizer """
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.token.tokenizer import Tokenizer


class ArtTokenizer(Tokenizer):
    """
    """
    def __init__(self,
                 id,
                 content,
                 version='1.0'):
        """
        """
        super().__init__(id, content, version=version)

    def next_lexeme_impl(self):
        """
        """
        pass

    def advance(self):
        """
        Consume codepoint and advances input position (pointer).
        """
        result = Text.bad_codepoint()
        return result

    def peek(self):
        """
        Peek the next codepoint not advancing input position (pointer).
        """
        result = Text.bad_codepoint()
        if self._content_position < self._end_content:
            pass
        return result

    def consume_unicode_escape(self, n):
        """
        Parce unicode escape(s):
            \uHexDigitHexDigitHexDigitHexDigit - up to 0xFFFF
            \uHexDigitHexDigitHexDigitHexDigit \uHexDigitHexDigitHexDigitHexDigit - up to 0x10FFFF with surrogates
            \UHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigit - codepoint
        The current position points past \u or \U.
            n = 4 means \u
            n = 8 means \U
        """
        result = Text.bad_codepoint()
        calculated = 0
        for k in range(n):
            codepoint = self.next_codepoint()
            if Text.hexadecimal_digit(codepoint):
                calculated = (calculated << 4) | codepoint

        return result
