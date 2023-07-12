# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art tokenizer """
from collections import deque
from art.framework.core.status import Status
from art.framework.core.text import Text
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
                 indent_size=4,
                 version='1.0'):
        """
        """
        super().__init__(id, content, statistics, diagnostics, version=version)
        self._keywords = ArtTokenizer.populate_keywords()
        self._nesting_level = 0  # parentheses (() [] {}) nesting level
        self._beginning_of_line = True
        self._indent_size = indent_size
        self._indents_level = 0  # level of nested indents/dedents
        self._pending_indents = 0  # indents (if > 0) or dedents (if < 0) - from Python source code
        self._indents = deque()  # stack of indents, off-side rule support, Peter Landin
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
        https://docs.python.org/3/reference/lexical_analysis.html#indentation
        """
        content_position = self._content_position
        codepoint = self._codepoint
        if self._beginning_of_line:
            self._beginning_of_line = False
            if self._content_position < self._end_content:
                indent = 0
                while (self._content_position < self._end_content and
                       self._codepoint == 0x00000020):  # ' ':
                    self.advance()
                    indent += 1
                ignore = ((indent >= 0 and Text.eol(self._codepoint)) or  # blank line, either '\n' or '   \n'
                          self.comment_start())  # comment
                if not ignore and self._nesting_level == 0:
                    if indent == self._indents[self._indents_level]:
                        pass
                    elif indent > self._indents[self._indents_level]:
                        self._indents_level += 1
                        self._pending_indents += 1
                        self._indents.append(indent)
                    else:  # indent < self._indents[self._indents_level]
                        while (self._indents_level > 0 and
                               indent < self._indents[self._indents_level]):
                            self._indents_level -= 1
                            self._pending_indents -= 1
                            self._indents.pop()
                        if indent != self._indents[self._indents_level]:
                            self._token.kind = TokenKind.CORRUPTED_DEDENT
        if self._pending_indents != 0:
            if self._pending_indents < 0:
                self._pending_indents += 1
                self._token.kind = TokenKind.DEDENT
            else:
                self._pending_indents -= 1
                self._token.kind = TokenKind.INDENT
        else:
            self._content_position = content_position  # rollback
            self._codepoint = codepoint
        return (self._token.kind == TokenKind.INDENT or
                self._token.kind == TokenKind.DEDENT)

    @staticmethod
    def digits_separator(codepoint):
        """
        """
        return codepoint == 0x0000005F  # _

    @staticmethod
    def fraction_start(codepoint):
        """
        """
        return codepoint == 0x0000002E  # .

    @staticmethod
    def exponent_start(codepoint):
        """
        """
        return codepoint == 0x00000065 or codepoint == 0x00000045  # e or E

    @staticmethod
    def exponent_sign(codepoint):
        """
        """
        return codepoint == 0x0000002B or codepoint == 0x0000002D  # + or -

    @staticmethod
    def number_control_codepoint(codepoint):
        """
        """
        return (ArtTokenizer.digits_separator(codepoint) or
                ArtTokenizer.fraction_start(codepoint) or
                ArtTokenizer.exponent_start(codepoint) or
                ArtTokenizer.exponent_sign(codepoint))

    def get_radix(self):
        """
        """
        octal_prefix = False  # true if 0xxx
        codepoint = self._codepoint
        if Text.ascii_zero_digit(codepoint):  # only consider ASCII numbers
            match self.advance():
                case (0x00000062 | 0x00000042):  # b or B
                    radix = 2
                    digits = Text.ascii_binary_digit
                    self.advance()
                case (0x0000006F | 0x0000004F):  # o or O, genuine octal
                    radix = 8
                    digits = Text.ascii_octal_digit
                    self.advance()
                case (0x00000078 | 0x00000058):  # x or X
                    radix = 16
                    digits = Text.ascii_hexadecimal_digit
                    self.advance()
                case _:
                    # no need to advance as 0 already consumed
                    radix = 8
                    digits = Text.ascii_decimal_digit  # hopping to see real, if not - rescan as octal
                    octal_prefix = True
        else:
            radix = 10
            digits = Text.ascii_decimal_digit
        return codepoint, radix, octal_prefix, digits

    def parse_exponent(self, value):
        """
        E+123 e-123
        """
        digits = 0
        exponent_sign = False
        value.append(self._codepoint)
        self.advance()  # consume e or E
        while not Text.eos(self._codepoint):
            if Text.ascii_decimal_digit(self._codepoint):
                digits += 1
                value.append(self._codepoint)
                self.advance()
                continue
            elif ArtTokenizer.exponent_sign(self._codepoint):
                digits = 0
                if not exponent_sign:
                    exponent_sign = True
                    value.append(self._codepoint)
                    self.advance()
                    continue
            break
        return digits > 0

    def parse_fraction(self, value):
        """
        .123 .123E-307  .3234e+92  .E4  .e+5
        .1_2_3 .12__3E-307  .3_2_34e+92  1_23E4
        """
        separators = 0
        parse_exponent_result = True
        value.append(self._codepoint)
        self.advance()  # consume .
        while not Text.eos(self._codepoint):
            if Text.ascii_decimal_digit(self._codepoint):
                separators = 0
                value.append(self._codepoint)
                self.advance()
                continue
            elif ArtTokenizer.digits_separator(self._codepoint):
                separators += 1
                self.advance()
                continue
            elif ArtTokenizer.exponent_start(self._codepoint):
                parse_exponent_result = self.parse_exponent(value)
            break
        return not separators and parse_exponent_result

    def scan_number(self):
        """
        Binary:      0b101111100011   0b__101_1_1_1100_011
        Octal:       0o5743 or 05743  0o_57__4_3 or 0__57_4____3
        Decimal:     3043             3___0__4_3
        Hexadecimal: 0xBE3            0xB__E_3
        Real:        3.14159265359  3.1415E2    3.1415e2    3_5.1__41_5E2    3.1_41_5e2
                     3.141__26_3_9  3.1415E+2   3.1415e+2   3_6.1__41_5E+2   3.1_41_5e+2
                     3.141_______5  3.1415E-2   3.1415e-2   3_7.1__41_5E-2   3.1_41_5e-2
                     3234E-3  6e+5   43.
        Digit separator: _
        Not allowed at the beginning, before fraction, inside fraction ot at the end.
        Illegals: _10, 10_, 10_.5, 10._5, 10.e_-5, 10.e+5_34
        All numbers are 64 bits.
        """
        value = list()
        codepoint, radix, octal_prefix, digits = self.get_radix()
        if octal_prefix:
            value.append(codepoint)  # push first 0
        real = False  # is real number
        valid = True  # track erroneous or not status
        separators = 0
        if not octal_prefix and ArtTokenizer.number_control_codepoint(self._codepoint):
            valid = False  # separator(s) and others cannot start number
        if valid:
            content_position = self._content_position
            codepoint = self._codepoint
            n = 2 if octal_prefix else 1  # if octal (0xxx) and not real - rescan in real octal mode
            for k in range(n):  # mimic goto
                if k > 0:
                    self._content_position = content_position
                    self._codepoint = codepoint
                    digits = Text.ascii_octal_digit
                    value = value[:1]
                while not Text.eos(self._codepoint):
                    if digits(self._codepoint):
                        separators = 0
                        value.append(self._codepoint)
                        self.advance()
                        continue
                    elif ArtTokenizer.digits_separator(self._codepoint):
                        separators += 1
                        self.advance()
                        continue
                    elif ArtTokenizer.fraction_start(self._codepoint):
                        if radix == 10 or octal_prefix:  # only octal or decimal
                            valid = self.parse_fraction(value)
                            real = True
                        else:
                            valid = False
                    elif ArtTokenizer.exponent_start(self._codepoint):
                        if radix == 10 or octal_prefix:  # only octal or decimal
                            valid = self.parse_exponent(value)
                            real = True
                        else:
                            valid = False
                    break
                if real:
                    break
        if valid and (separators or not value):
            valid = False  # separator(s) and others cannot end number also should not be empty
        if valid:
            try:
                value = ''.join(map(str, map(chr, value)))
                if real:
                    self._token.value = float(value)   # first to parse
                    self._token.kind = TokenKind.REAL  # then tag
                else:
                    self._token.value = int(value, radix)  # first to parse
                    self._token.kind = TokenKind.INTEGER   # then tag
            except ValueError as ex:
                valid = False
        if not valid:
            self._diagnostics.add(Status(f'Invalid numeric literal at '
                                         f'{self.content.get_location(self._content_position)}',
                                         'tokenizer',
                                         Status.INVALID_REAL_LITERAL if real else Status.INVALID_INT_LITERAL))

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
        if self._indent_size:
            if self.process_indentation():
                return
        codepoint = self._codepoint
        if codepoint == Text.eos_codepoint():
            self._token.kind = TokenKind.EOS
        elif Text.whitespace(codepoint):
            self.consume_whitespaces()
        elif self.identifier_start(codepoint):
            self.scan_identifier()
        elif Text.ascii_hexadecimal_digit(codepoint):  # covers all ASCII digits bin, oct, dec, hex
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

