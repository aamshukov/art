# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Tokenizer """
from collections import defaultdict

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
                 statistics,
                 diagnostics,
                 version='1.0'):
        """
        """
        super().__init__(id, content, statistics, diagnostics, version=version)
        self._keywords = ArtTokenizer.populate_keywords()

    @staticmethod
    def populate_keywords():
        """
        Populate keywords dictionary of string:TokenKind.
        """
        result = defaultdict(lambda: TokenKind.IDENTIFIER)
        result['integer'] = TokenKind.INTEGER
        result['real'] = TokenKind.REAL
        result['string'] = TokenKind.STRING
        result['boolean'] = TokenKind.BOOLEAN
        result['true'] = TokenKind.TRUE
        result['false'] = TokenKind.FALSE
        result['enum'] = TokenKind.ENUM
        result['struct'] = TokenKind.STRUCT
        result['record'] = TokenKind.RECORD
        result['let'] = TokenKind.LET
        result['var'] = TokenKind.VAR
        result['namespace'] = TokenKind.NAMESPACE
        result['import'] = TokenKind.IMPORT
        result['if'] = TokenKind.IF
        result['else'] = TokenKind.ELSE
        result['for'] = TokenKind.FOR
        result['while'] = TokenKind.WHILE
        result['do'] = TokenKind.DO
        result['switch'] = TokenKind.SWITCH
        result['case'] = TokenKind.CASE
        result['when'] = TokenKind.WHEN
        result['match'] = TokenKind.MATCH
        result['pattern'] = TokenKind.PATTERN
        result['continue'] = TokenKind.CONTINUE
        result['break'] = TokenKind.BREAK
        result['goto'] = TokenKind.GOTO
        result['return'] = TokenKind.REAL
        result['partial'] = TokenKind.PARTIAL
        result['is'] = TokenKind.IS
        result['as'] = TokenKind.AS
        result['and'] = TokenKind.AND
        result['or'] = TokenKind.OR
        result['xor'] = TokenKind.XOR
        result['not'] = TokenKind.NOT
        result['neg'] = TokenKind.NEG
        result['fn'] = TokenKind.FUNCTION
        result['proc'] = TokenKind.PROCEDURE
        result['lazy'] = TokenKind.LAZY
        result['noop'] = TokenKind.NOOP
        result['type'] = TokenKind.TYPE
        return result

    def lookup(self, name):
        """
        """
        return self._keywords[name]

    def next_lexeme_impl(self):
        """
        """
        pass
