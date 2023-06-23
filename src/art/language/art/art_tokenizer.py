# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Tokenizer """
from collections import defaultdict, deque
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
        self._nesting_level = 0  # parentheses (() [] {}) nesting level
        self._beginning_of_line = True
        self._pending_indents = 0  # indents (if > 0) or dedents (if < 0) - from Python source code
        self._indents = deque()  # stack of indent, off-side rule support, Peter Landin
        self._indents.append(0)

    @staticmethod
    def populate_keywords():
        """
        Populate keywords dictionary of string:TokenKind.
        """
        result = dict()
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
        result['async'] = TokenKind.ASYNC
        result['await'] = TokenKind.AWAIT
        return result

    def lookup(self, name):
        """
        """
        if name in self._keywords:
            return self._keywords[name]
        else:
            return TokenKind.IDENTIFIER

    def consume_whitespaces(self):
        """
        Usually called from tokenizer and the position already at WS,
        it means in any case return TokenKind.WS.
        """
        self.next_codepoint()
        while Text.whitespace(self.codepoint):
            self.next_codepoint()
        self._token.kind = TokenKind.WS

    @staticmethod
    def identifier_start(codepoint):
        """
        """
        assert Text.valid_codepoint(codepoint)
        return (Text.letter(codepoint) or
                Text.underscore(codepoint) or
                Text.dollar_sign(codepoint) or
                Text.currency_sign(codepoint) or
                Text.connector_punctuation(codepoint) or
                # ?? Text.other_symbol(codepoint) or
                Text.pictographs(codepoint) or
                Text.miscellaneous_symbols(codepoint) or
                Text.dingbats(codepoint) or
                Text.emoji(codepoint))

    @staticmethod
    def identifier_part(codepoint):
        """
        """
        assert Text.valid_codepoint(codepoint)
        return (Text.letter(codepoint) or
                Text.decimal_digit(codepoint) or
                Text.underscore(codepoint) or
                Text.letter_number(codepoint) or
                Text.dollar_sign(codepoint) or
                Text.currency_sign(codepoint) or
                Text.connector_punctuation(codepoint) or
                Text.spacing_mark(codepoint) or
                Text.non_spacing_mark(codepoint) or
                # ?? Text.other_symbol(codepoint) or
                Text.pictographs(codepoint) or
                Text.miscellaneous_symbols(codepoint) or
                Text.dingbats(codepoint) or
                Text.emoji(codepoint))

    def scan_identifier(self):
        """
        """
        self.next_codepoint()
        while self.identifier_part(self.codepoint):
            self.next_codepoint()
        self._token.kind = TokenKind.IDENTIFIER

    def process_indentation(self):
        """
        """
        self._beginning_of_line = False
        if self._content_position < self._end_content:
            indent = 0
            while (self._content_position < self._end_content and
                   self.codepoint == 0x00000020):  # ' ':
                self.next_codepoint()
                indent += 1
            ignore = ((indent == 0 and self.codepoint == 0x0000000A) or  # blank line
                      self.codepoint == 0x00000023)  # comment
            if not ignore and self._nesting_level == 0:
                if indent == self._indents[0]:
                    pass
                elif indent > self._indents[0]:
                    self._pending_indents += 1
                    self._indents.append(indent)
                else:  # indent == self._indents[0]
                    while self._indents and indent < self._indents[0]:
                        self._pending_indents -= 1
                        self._indents.popleft()
            if self._pending_indents != 0:
                if self._pending_indents > 0:
                    self._pending_indents -= 1
                    self._token.kind = TokenKind.INDENT
                else:
                    self._pending_indents += 1
                    self._token.kind = TokenKind.DEDENT

    def next_lexeme_impl(self):
        """
        """
        if self._beginning_of_line:
            self.process_indentation()
            if (self._token.kind == TokenKind.INDENT or
                    self._token.kind == TokenKind.DEDENT):
                return
        codepoint = self.codepoint
        if codepoint == Text.eos_codepoint():
            self._token.kind = TokenKind.EOS
        elif Text.whitespace(codepoint):
            self.consume_whitespaces()
        elif self.identifier_start(codepoint):
            self.scan_identifier()
        elif (Text.binary_digit(codepoint) or
              Text.octal_digit(codepoint) or
              Text.decimal_digit(codepoint) or
              Text.hexadecimal_digit(codepoint)):
            pass
        elif Text.left_parenthesis(codepoint):  # '('
            self._nesting_level += 1
        elif Text.right_parenthesis(codepoint):  # ')'
            self._nesting_level -= 1
        elif Text.left_square_bracket(codepoint):  # '['
            self._nesting_level += 1
        elif Text.right_square_bracket(codepoint):  # ']'
            self._nesting_level -= 1
        elif Text.left_curly_bracket(codepoint):  # '{'
            self._nesting_level += 1
        elif Text.right_curly_bracket(codepoint):  # '}'
            self._nesting_level -= 1
        elif Text.plus_sign(codepoint):  # '+'
            pass
        elif Text.hyphen_minus(codepoint):  # '-'
            pass
        elif Text.asterisk(codepoint):  # '*'
            pass
        elif Text.forward_slash(codepoint):  # '/'
            pass
        elif Text.back_slash(codepoint):  # '\\'
            if self.lookahead_codepoint() == 'n':  # special case for indent
                self._beginning_of_line = True
        elif Text.equals_sign(codepoint):  # '='
            pass
        elif Text.less_than_sign(codepoint):  # '<'
            pass
        elif Text.greater_than_sign(codepoint):  # '>'
            pass
        elif Text.dot(codepoint):  # '.'
            pass
        elif Text.colon(codepoint):  # ':'
            pass
        elif Text.comma(codepoint):  # ','
            pass
        elif Text.semicolon(codepoint):  # ';'
            pass
        elif Text.vertical_line(codepoint):  # '|'
            pass
        elif Text.grave_accent(codepoint):  # '`'
            pass
        elif Text.tilde(codepoint):  # '~'
            pass
        elif Text.exclamation_mark(codepoint):  # '!'
            pass
        elif Text.question_mark(codepoint):  # '?'
            pass
        elif Text.apostrophe(codepoint):  # '''
            pass
        elif Text.quotation_mark(codepoint):  # '"'
            pass
        elif Text.commercial_at(codepoint):  # '@'
            pass
        elif Text.number_sign(codepoint):  # '#'
            pass
        elif Text.percent_sign(codepoint):  # '%'
            pass
        elif Text.circumflex_accent(codepoint):  # '^'
            pass
        elif Text.ampersand(codepoint):  # '&'
            pass

    def epilog(self):
        """
        """
        super().epilog()
        if self._token.kind == TokenKind.IDENTIFIER:  # check if it is keyword
            self._token.kind = self.lookup(self._token.literal)
