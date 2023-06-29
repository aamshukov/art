# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Tokenizer """
from collections import defaultdict, deque
from art.framework.core.flags import Flags
from art.framework.core.status import Status
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
        self._indent_size = 4  # ??
        self._pending_indents = 0  # indents (if > 0) or dedents (if < 0) - from Python source code
        self._indents = deque()  # stack of indent, off-side rule support, Peter Landin
        self._indents.append(0)

    @staticmethod
    def populate_keywords():
        """
        Populate keywords dictionary of string:TokenKind.
        """
        result = dict()
        result['int'] = TokenKind.INTEGER
        result['integer'] = TokenKind.INTEGER
        result['real'] = TokenKind.REAL
        result['float'] = TokenKind.REAL
        result['double'] = TokenKind.REAL
        result['decimal'] = TokenKind.REAL
        result['number'] = TokenKind.REAL
        result['bool'] = TokenKind.BOOLEAN
        result['boolean'] = TokenKind.BOOLEAN
        result['true'] = TokenKind.TRUE
        result['false'] = TokenKind.FALSE
        result['string'] = TokenKind.STRING
        result['enum'] = TokenKind.ENUM
        result['struct'] = TokenKind.STRUCT
        result['record'] = TokenKind.RECORD
        result['class'] = TokenKind.CLASS
        result['interface'] = TokenKind.INTERFACE
        result['abstract'] = TokenKind.ABSTRACT
        result['mixin'] = TokenKind.MIXIN
        result['import'] = TokenKind.IMPORT
        result['namespace'] = TokenKind.NAMESPACE
        result['module'] = TokenKind.MODULE
        result['alias'] = TokenKind.ALIAS
        result['let'] = TokenKind.LET
        result['var'] = TokenKind.VAR
        result['const'] = TokenKind.CONST
        result['readonly'] = TokenKind.READONLY
        result['super'] = TokenKind.SUPER
        result['base'] = TokenKind.BASE
        result['self'] = TokenKind.SELF
        result['this'] = TokenKind.THIS
        result['if'] = TokenKind.IF
        result['else'] = TokenKind.ELSE
        result['for'] = TokenKind.FOR
        result['while'] = TokenKind.WHILE
        result['do'] = TokenKind.DO
        result['repeat'] = TokenKind.REPEAT
        result['switch'] = TokenKind.SWITCH
        result['case'] = TokenKind.CASE
        result['when'] = TokenKind.WHEN
        result['match'] = TokenKind.MATCH
        result['pattern'] = TokenKind.PATTERN
        result['default'] = TokenKind.DEFAULT
        result['continue'] = TokenKind.CONTINUE
        result['break'] = TokenKind.BREAK
        result['leave'] = TokenKind.LEAVE
        result['goto'] = TokenKind.GOTO
        result['return'] = TokenKind.REAL
        result['noop'] = TokenKind.NOOP
        result['pass'] = TokenKind.PASS
        result['partial'] = TokenKind.PARTIAL
        result['finally'] = TokenKind.FINALLY
        result['defer'] = TokenKind.DEFER
        result['is'] = TokenKind.IS
        result['as'] = TokenKind.AS
        result['and'] = TokenKind.AND
        result['or'] = TokenKind.OR
        result['xor'] = TokenKind.BITWISE_XOR
        result['not'] = TokenKind.NOT
        result['neg'] = TokenKind.NEG
        result['fn'] = TokenKind.FUNCTION
        result['proc'] = TokenKind.PROCEDURE
        result['lambda'] = TokenKind.LAMBDA
        result['lazy'] = TokenKind.LAZY
        result['recursive'] = TokenKind.RECURSIVE
        result['type'] = TokenKind.TYPE
        result['def'] = TokenKind.DEF
        result['with'] = TokenKind.WITH
        result['scoped'] = TokenKind.SCOPED
        result['async'] = TokenKind.ASYNC
        result['await'] = TokenKind.AWAIT
        result['lock'] = TokenKind.LOCK
        result['yield'] = TokenKind.YIELD
        result['assert'] = TokenKind.ASSERT
        result['pragma'] = TokenKind.PRAGMA
        result['eq'] = TokenKind.COMP_EQUAL
        result['ne'] = TokenKind.COMP_NOT_EQUAL
        result['lt'] = TokenKind.COMP_LESS_THAN
        result['le'] = TokenKind.COMP_LESS_THAN_OR_EQUAL
        result['gt'] = TokenKind.COMP_GREATER_THAN
        result['ge'] = TokenKind.COMP_GREATER_THAN_OR_EQUAL

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
        self.advance()
        while Text.whitespace(self._codepoint):
            self.advance()
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
        self.advance()
        while self.identifier_part(self._codepoint):
            self.advance()
        self._token.kind = TokenKind.IDENTIFIER

    def comment_start(self):
        """
        """
        crr = self._codepoint
        nxt = self.peek()
        return (crr == 0x00000023 or                          # #
                (crr == 0x0000002F and nxt == 0x0000002F) or  # //
                (crr == 0x0000002F and nxt == 0x0000002A))    # /*

    def process_indentation(self):
        """
        """
        content_position = self._content_position
        codepoint = self._codepoint
        self._beginning_of_line = False
        if self._content_position < self._end_content:
            indent = 0
            while (self._content_position < self._end_content and
                   self._codepoint == 0x00000020):  # ' ':
                self.advance()
                indent += 1
            ignore = ((indent == 0 and Text.eol(self._codepoint)) or  # blank line
                      self.comment_start())  # comment
            # assert (indent % self._indent_size == 0,
            #         f"Invalid indent, must be multiple of {self._indent_size}.")
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
            else:
                self._content_position = content_position  # rollback
                self._codepoint = codepoint

    def scan_number(self):
        """
        Binary:      0b101111100011   0b__101_1_1_1100_011
        Octal:       0o5743 or 05743  0o_57__4_3 or 0__57_4____3
        Decimal:     3043             3___0__4_3
        Hexadecimal: 0xBE3            0xB__E_3
        Real:        3.14159265359  3.1415E2    3.1415e2    3_5.1__41_5E2    3.1_41_5e2
                     3.141__26_3_9  3.1415E+2   3.1415e+2   3_6.1__41_5E+2   3.1_41_5e+2
                     3.141_______5  3.1415E-2   3.1415e-2   3_7.1__41_5E-2   3.1_41_5e-2
        Digit separator: _
        All numbers are 64 bits.
        """
        codepoint = self._codepoint
        if Text.zero_digit(codepoint):
            codepoint = self.advance()
            match codepoint:
                case ('b' | 'B'):
                    radix = 2
                case ('o' | 'O'):
                    radix = 8
                case ('x' | 'X'):
                    radix = 16
                case _:
                    radix = 8
        else:
            radix = 10

    def scan_string(self, quote):
        """
        """
        self.advance()
        while (not Text.eol(self._codepoint) and
               not Text.eos(self._codepoint) and
               self._codepoint != quote or
               (self._codepoint == quote and self._escaped)):
            self.advance()
        if self._codepoint == quote:
            self.advance()
            self._token.kind = TokenKind.STRING
        else:
            self._diagnostics.add(Status(f'Unclosed string literal at '
                                         f'{self.content.get_location(self._content_position)}',
                                         'tokenizer',
                                         Status.INVALID_STRING_LITERAL))

    def scan_comments(self, single_line):
        """
        Scans single (# //) or multi (/**/) line comments.
        Multi line comments can be nested.
        """
        self.advance()
        if single_line:
            while (not Text.eol(self._codepoint) and
                   not Text.eos(self._codepoint)):
                self.advance()
            self._token.kind = TokenKind.SINGLE_LINE_COMMENT
        else:
            level = 1  # nesting level
            while not Text.eos(self._codepoint):
                crr = self._codepoint
                nxt = self.peek()
                if crr == 0x0000002F and nxt == 0x0000002A:  # /*, exact codepoints
                    self.advance()
                    self.advance()
                    level += 1
                elif crr == 0x0000002A and nxt == 0x0000002F:  # */, exact codepoints
                    self.advance()
                    self.advance()
                    level -= 1
                    if level == 0:
                        break
                else:
                    self.advance()
            if level == 0:
                self._token.kind = TokenKind.MULTI_LINE_COMMENT

    def next_lexeme_impl(self):
        """
        Not optimized manual implementation of the lexical analyzer.
        For more advanced and optimized version see C++ implementation
        of arcturus and frontend (projects). That implementation uses custom
        generated FSA (goto transitions) which recognizes keywords without lookup,
        recognizes integers and real (float/double) numbers, comments, etc.
        """
        if self._beginning_of_line:
            self.process_indentation()
            if (self._token.kind == TokenKind.INDENT or
                    self._token.kind == TokenKind.DEDENT):
                return
        codepoint = self._codepoint
        if codepoint == Text.eos_codepoint():
            self._token.kind = TokenKind.EOS
        elif Text.whitespace(codepoint):
            self.consume_whitespaces()
        elif self.identifier_start(codepoint):
            self.scan_identifier()
        elif Text.hexadecimal_digit(codepoint):  # covers all digits bin, oct, dec, hex
            self.scan_number()
        elif Text.left_parenthesis(codepoint):  # '('
            self._nesting_level += 1
            self._token.kind = TokenKind.LEFT_PARENTHESIS
            self.advance()
        elif Text.right_parenthesis(codepoint):  # ')'
            self._nesting_level -= 1
            self._token.kind = TokenKind.RIGHT_PARENTHESIS
            self.advance()
        elif Text.left_square_bracket(codepoint):  # '['
            self._nesting_level += 1
            self._token.kind = TokenKind.LEFT_SQUARE_BRACKET
            self.advance()
        elif Text.right_square_bracket(codepoint):  # ']'
            self._nesting_level -= 1
            self._token.kind = TokenKind.RIGHT_SQUARE_BRACKET
            self.advance()
        elif Text.left_curly_bracket(codepoint):  # '{'
            self._nesting_level += 1
            self._token.kind = TokenKind.LEFT_CURLY_BRACKET
            self.advance()
        elif Text.right_curly_bracket(codepoint):  # '}'
            self._nesting_level -= 1
            self._token.kind = TokenKind.RIGHT_CURLY_BRACKET
            self.advance()
        elif self._codepoint == 0x0000000D:  # fast path for \r\n
            self.advance()
            if self._codepoint == 0x0000000A:  # if \r\n
                self.advance()
            self._beginning_of_line = True
            self._token.kind = TokenKind.EOL
        elif Text.eol(codepoint):
            self._beginning_of_line = True
            self._token.kind = TokenKind.EOL
            self.advance()
        elif Text.equals_sign(codepoint):  # '=' '==' '=>' eq as kw
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.EQUAL
                self.advance()
            elif Text.greater_than_sign(codepoint):
                self._token.kind = TokenKind.DOUBLE_ARROW
                self.advance()
            else:
                self._token.kind = TokenKind.EQUALS_SIGN
        elif Text.exclamation_mark(codepoint):  # '!' '!=' ne as kw
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.NOT_EQUAL
                self.advance()
            else:
                self._token.kind = TokenKind.EXCLAMATION_MARK
        elif Text.less_than_sign(codepoint):  # '<' '<=' '<=>' lt, le as kws
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                codepoint = self.advance()
                if Text.greater_than_sign(codepoint):
                    self._token.kind = TokenKind.SPACESHIP
                    self.advance()
                else:
                    self._token.kind = TokenKind.LESS_THAN_OR_EQUAL
            else:
                self._token.kind = TokenKind.LESS_THAN_SIGN
        elif Text.greater_than_sign(codepoint):  # '>' '>=' gt, ge as kws
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.GREATER_THAN_OR_EQUAL
                self.advance()
            else:
                self._token.kind = TokenKind.GREATER_THAN_SIGN
        elif Text.dot(codepoint):  # '.' '..' '...', do not consider fraction part like .025
            codepoint = self.advance()
            if Text.dot(codepoint):
                codepoint = self.advance()
                if Text.dot(codepoint):
                    self._token.kind = TokenKind.ELLIPSES
                    self.advance()
                else:
                    self._token.kind = TokenKind.RANGE
            else:
                self._token.kind = TokenKind.DOT
        elif Text.plus_sign(codepoint):  # '+' '++' '+='
            codepoint = self.advance()
            if Text.plus_sign(codepoint):
                self._token.kind = TokenKind.INCREMENT
                self.advance()
            elif Text.equals_sign(codepoint):
                self._token.kind = TokenKind.ADD_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.PLUS_SIGN
        elif Text.hyphen_minus(codepoint):  # '-' '--' '-=' '->'
            codepoint = self.advance()
            if Text.hyphen_minus(codepoint):
                self._token.kind = TokenKind.DECREMENT
                self.advance()
            elif Text.equals_sign(codepoint):
                self._token.kind = TokenKind.SUB_ASSIGNMENT
                self.advance()
            elif Text.greater_than_sign(codepoint):
                self._token.kind = TokenKind.ARROW
                self.advance()
            else:
                self._token.kind = TokenKind.HYPHEN_MINUS
        elif Text.asterisk(codepoint):  # '*' '*='
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.MUL_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.ASTERISK
        elif Text.forward_slash(codepoint):  # '/' '/=' '//' '/*'
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.DIV_ASSIGNMENT
                self.advance()
            elif Text.forward_slash(codepoint):
                self.scan_comments(single_line=True)
            elif Text.asterisk(codepoint):
                self.scan_comments(single_line=False)
            else:
                self._token.kind = TokenKind.FORWARD_SLASH
        elif Text.percent_sign(codepoint):  # '%' '%='
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.MOD_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.PERCENT_SIGN
        elif Text.ampersand(codepoint):  # '&' '&='
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.BITWISE_AND_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.BITWISE_AND
        elif Text.vertical_line(codepoint):  # '|' '|='
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.BITWISE_OR_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.BITWISE_OR
        elif Text.circumflex_accent(codepoint):  # '^' '^='
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.BITWISE_XOR_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.BITWISE_XOR
        elif Text.circumflex_accent(codepoint):  # '~' '~=' neg as kw
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.BITWISE_XOR_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.BITWISE_XOR
        elif Text.tilde(codepoint):  # '~'
            codepoint = self.advance()
            if Text.equals_sign(codepoint):
                self._token.kind = TokenKind.BITWISE_NOT_ASSIGNMENT
                self.advance()
            else:
                self._token.kind = TokenKind.BITWISE_NOT
        elif Text.colon(codepoint):  # ':' '::'
            codepoint = self.advance()
            if Text.colon(codepoint):
                self._token.kind = TokenKind.COLONS
                self.advance()
            else:
                self._token.kind = TokenKind.COLON
        elif Text.semicolon(codepoint):  # ';'
            self._token.kind = TokenKind.SEMICOLON
            self.advance()
        elif Text.comma(codepoint):  # ','
            self._token.kind = TokenKind.COMMA
            self.advance()
        elif Text.question_mark(codepoint):  # '?'
            self._token.kind = TokenKind.QUESTION_MARK
            self.advance()
        elif Text.commercial_at(codepoint):  # '@'
            self._token.kind = TokenKind.COMMERCIAL_AT
            self.advance()
        elif Text.grave_accent(codepoint):  # '`'
            self._token.kind = TokenKind.GRAVE_ACCENT
            self.advance()
        elif Text.back_slash(codepoint):  # '\\'
            self._diagnostics.add(Status(f'Loose "\\" character at '
                                         f'{self.content.get_location(self._content_position)}',
                                         'tokenizer',
                                         Status.INVALID_CHARACTER))
            self.advance()
        elif Text.apostrophe(codepoint):  # '''
            self.scan_string(codepoint)
        elif Text.quotation_mark(codepoint):  # '"'
            self.scan_string(codepoint)
        elif Text.number_sign(codepoint):  # '#'
            self.scan_comments(single_line=True)
        else:
            self._diagnostics.add(Status(f'Invalid character at '
                                         f'{self.content.get_location(self._content_position)}',
                                         'tokenizer',
                                         Status.INVALID_UNICODE_ESCAPE))
            self.advance()

    def epilog(self):
        """
        """
        super().epilog()
        if self._token.kind == TokenKind.IDENTIFIER:  # check if it is keyword
            self._token.kind = self.lookup(self._token.literal)
