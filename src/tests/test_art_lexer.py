#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.diagnostics import Diagnostics
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @staticmethod
    def get_lexer(program):
        dp = StringDataProvider(program)
        data = dp.load()
        content = Content(0, data, '')
        content.build_line_map()
        diagnostics = Diagnostics()
        statistics = Statistics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        return lexer

    @staticmethod
    def evaluate(program, tokens, validate=True):
        literals = list()
        values = list()
        lexer = Test.get_lexer(program)
        for k, token in enumerate(tokens):
            lexer.next_lexeme()
            literals.append(lexer.token.literal)
            values.append(lexer.token.value)
            if validate:
                assert lexer.token.kind == TokenKind(token)
        return literals, values

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

    def test_lexical_analyzer_1_success(self):
        tokens = [TokenKind.EOS]
        Test.evaluate('', tokens)

    def test_lexical_analyzer_2_success(self):
        tokens = [TokenKind.IDENTIFIER,
                  TokenKind.EOS]
        Test.evaluate('a', tokens)

    def test_lexical_analyzer_3_success(self):
        tokens = [TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.EOS]
        Test.evaluate('a  b ', tokens)

    def test_lexical_analyzer_4_success(self):
        tokens = [TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.EOS]
        Test.evaluate('abc dcf ef', tokens)

    def test_lexical_analyzer_5_success(self):
        tokens = [TokenKind.INDENT,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.INTEGER_KW,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.EOS]
        Test.evaluate('  A   冬   integer ⌛ သည်  B  C 🐍 သည်   ', tokens)

    def test_lexical_analyzer_indentation_1_success(self):
        tokens = [TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.DEF,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.LEFT_PARENTHESIS,
                  TokenKind.RIGHT_PARENTHESIS,
                  TokenKind.EOL,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a1
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a2
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a3
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a4
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,  # a5
                  TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.DEDENT,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a6
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a7
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a8
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a9
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a10
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,  # a11
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,  # a12
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a13
                  TokenKind.WS,
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a14
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a15
                  TokenKind.WS,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a16
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a17
                  TokenKind.EOL,
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,  # a18
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a19
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.IDENTIFIER,  # a20
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # a21
                  TokenKind.EOL,
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,  # a22
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # end
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.EOS]
        program = """
        def foo()

            a1
        
                                        
                a2
                    a3
                        a4
                        a5      # comments
            a6
                      a7
                            a8
                                a9
                                    a10
                                    a11
                                    a12
                            a13              
                        a14
                    a15              
                    a16
            a17

            a18
                    a19
                            a20
            a21

        
            a22
        end
        """
        Test.evaluate(program, tokens, validate=True)

    def test_lexical_analyzer_indentation_2_success(self):
        tokens = [TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.WHILE,
                  TokenKind.WS,
                  TokenKind.LEFT_PARENTHESIS,
                  TokenKind.SELF,  # self
                  TokenKind.DOT,  # .
                  TokenKind.IDENTIFIER,  # _content_position
                  TokenKind.WS,
                  TokenKind.LESS_THAN_SIGN,
                  TokenKind.WS,
                  TokenKind.SELF,  # self
                  TokenKind.DOT,  # .
                  TokenKind.IDENTIFIER,  # _end_content
                  TokenKind.WS,
                  TokenKind.AND,
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.SELF,  # self
                  TokenKind.DOT,  # .
                  TokenKind.IDENTIFIER,  # _codepoint
                  TokenKind.WS,
                  TokenKind.EQUAL,
                  TokenKind.WS,
                  TokenKind.INTEGER,
                  TokenKind.RIGHT_PARENTHESIS,
                  TokenKind.COLON,
                  TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.SELF,  # self
                  TokenKind.DOT,  # .
                  TokenKind.IDENTIFIER,  # advance
                  TokenKind.LEFT_PARENTHESIS,
                  TokenKind.RIGHT_PARENTHESIS,
                  TokenKind.EOL,
                  TokenKind.DEDENT,
                  TokenKind.IDENTIFIER,  # end
                  TokenKind.EOL,
                  TokenKind.WS,
                  TokenKind.EOS
                  ]
        program = """
        while (self._content_position < self._end_content and
               self._codepoint == 0x00000020):  # ' ':
            self.advance()
        end
        """
        Test.evaluate(program, tokens, validate=True)

    def test_string_single_quote_empty_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = "''"
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_empty_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '""'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_1_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '" "'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_2_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '" a "'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = r'"\"prefix \" 😁🐍 ⏩⏰⌚⏳☔♈ \uD83D\uDC0D ♿ \U0001F40Dသန彡xyz你叫什么名字Я ⚓⚡⚪⚽⛄⛎⛔⛪⛲⛵⛺⛽✅✊✨❌❎❓❗➕➰➿⬛⭐⭕🀄🃏🆎🆑🈁🈚🈯🈲🈸🉐🌀\""'  # noqa
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_single_quote_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = r"'\'prefix \' 😁🐍 ⏩⏰⌚⏳☔♈ \uD83D\uDC0D ♿ \U0001F40Dသန彡xyz你叫什么名字Я ⚓⚡⚪⚽⛄⛎⛔⛪⛲⛵⛺⛽✅✊✨❌❎❓❗➕➰➿⬛⭐⭕🀄🃏🆎🆑🈁🈚🈯🈲🈸🉐🌀\''"  # noqa
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_eos_success(self):
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = r'"abc'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_eol_success(self):
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.EOS]
        program = """'a
        """
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == "'a"

    def test_single_line_number_sign_comments_success(self):
        tokens = [TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '# 123'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '   # 123'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '   '
        assert literals[1] == '# 123'

    def test_single_line_comments_success(self):
        tokens = [TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '// 123'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '   // 123'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '   '
        assert literals[1] == '// 123'

    def test_multi_line_comments_success(self):
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/**/'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* */'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* 123 */'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.WS,
                  TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* /**/ /* /* /* */ */ */ */ /* */'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '/* /**/ /* /* /* */ */ */ */'
        assert literals[1] == ' '
        assert literals[2] == '/* */'
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/**'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/*'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/* /*/ /* /* /* */ */ */ */ /* */'
        literals, _ = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_integers_success(self):
        tokens = [TokenKind.INTEGER,
                  TokenKind.EOS]
        numbers =\
            [
               '077', '77',
               '0', '0_1', '0__1', '1', '0b1', '0x1', '0xa', '0__1__3__56',
               '0b101111100011', '0b1_01_1_1_1100_011',
               '0o5743', '05743', '00005743', '0o57__4_3', '05_7_4____3',
               '3044563', '3___0__4_3', '12_345_6789',
               '0xBE3', '0x1F34EAFB', '0xB_____E3', '0x1_F_34E__A_F_B'
            ]
        for number in numbers:
            literals, values = Test.evaluate(number, tokens)
            assert len(literals) == len(tokens)
            assert len(values) == len(tokens)
            assert literals[0] == number

    def test_invalid_integers_success(self):
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        numbers = ['0xG000L', '0E0', '079', '123___',
                   '0b', '0b1.0', '0_b__101_1_1_1100_011', '0b__101_1_1_1100_011', '0b101_1_1_1100_011__',
                   '0oo5743', '05o743', '0o_57__4_3', '0__57_4____3',
                   '0xBkE3', '0x1_F_34E__A_F_B',
                   '089'
                   ]
        for number in numbers:
            literals, _ = Test.evaluate(number, tokens, validate=False)
            pass

    def test_reals_success(self):
        tokens = [TokenKind.REAL,
                  TokenKind.EOS]
        numbers = ['0.', '0.0', '0.1', '00.1', '1.00',
                   '0.e+2', '3234E-3', '6e+5', '43.', '3.14159359', '3.1415E2', '3.1415e2',
                   '3_5.1__41_5E2', '03.1_41_5e2',
                   '3.141__26_3_9', '3.1415E+2', '3.1415e+2', '3_6.1__41_5E+2', '0.31_41_5e+2',
                   '3.141_______5', '3.1415E-2', '3.1415e-2', '3_7.1__41_5E-2', '12.31_41_5e-2',
                   '0E+0', '0E-0'
                   ]
        for number in numbers:
            literals, values = Test.evaluate(number, tokens)
            assert len(literals) == len(tokens)
            assert len(values) == len(tokens)
            assert literals[0] == number

    def test_invalid_reals_success(self):
        tokens = [TokenKind.UNKNOWN, TokenKind.UNKNOWN,
                  TokenKind.EOS]
        numbers = ['1+3', '0b0.e+2', '0.0.1',
                   '.0', '0.', '.1', '1.', '0.0.1', '1.00', '0b0.e+2',
                   '3.14159359', '3.1415E2', '3.1415e2', '3_5.1__41_5E2', '0.3.1_41_5e2',
                   '3.141__26_3_9', '3.1415E+2', '3.1415e+2', '3_6.1__41_5E+2', '0.3.1_41_5e+2',
                   '3.141_______5', '3.1415E-2', '3.1415e-2', '3_7.1__41_5E-2', '12.3.1_41_5e-2']
        for number in numbers:
            literals, _ = Test.evaluate(number, tokens, validate=False)
            pass

    def test_operators_success(self):
        lexer = Test.get_lexer('<')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.LESS_THAN_SIGN
        lexer = Test.get_lexer('<<')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SHIFT_LEFT
        lexer = Test.get_lexer('<=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.LESS_THAN_OR_EQUAL
        lexer = Test.get_lexer('<<=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SHIFT_LEFT_OR_EQUAL
        lexer = Test.get_lexer('<=>')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SPACESHIP
        lexer = Test.get_lexer('lt')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_LESS_THAN
        lexer = Test.get_lexer('le')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_LESS_THAN_OR_EQUAL
        lexer = Test.get_lexer('>')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_SIGN
        lexer = Test.get_lexer('>>')  # >  >
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_SIGN
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_SIGN
        lexer = Test.get_lexer('>=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_OR_EQUAL
        lexer = Test.get_lexer('>>=')  # >  >=
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_SIGN
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_OR_EQUAL
        lexer = Test.get_lexer('gt')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_GREATER_THAN
        lexer = Test.get_lexer('ge')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_GREATER_THAN_OR_EQUAL

    def test_equality_operators_success(self):
        lexer = Test.get_lexer('==')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.EQUAL
        lexer = Test.get_lexer('eq')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_EQUAL
        lexer = Test.get_lexer('!=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.NOT_EQUAL
        lexer = Test.get_lexer('ne')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.COMP_NOT_EQUAL

    def test_assignment_operators_success(self):
        lexer = Test.get_lexer('=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.EQUALS_SIGN
        lexer = Test.get_lexer('+=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ADD_ASSIGNMENT
        lexer = Test.get_lexer('-=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SUB_ASSIGNMENT
        lexer = Test.get_lexer('*=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.MUL_ASSIGNMENT
        lexer = Test.get_lexer('/=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DIV_ASSIGNMENT
        lexer = Test.get_lexer('%=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.MOD_ASSIGNMENT
        lexer = Test.get_lexer('&=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.BITWISE_AND_ASSIGNMENT
        lexer = Test.get_lexer('|=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.BITWISE_OR_ASSIGNMENT
        lexer = Test.get_lexer('^=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.BITWISE_XOR_ASSIGNMENT
        lexer = Test.get_lexer('~=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.BITWISE_NOT_ASSIGNMENT
        lexer = Test.get_lexer('<<=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SHIFT_LEFT_OR_EQUAL
        lexer = Test.get_lexer('>>=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_SIGN
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.GREATER_THAN_OR_EQUAL

    def test_dots_operators_success(self):
        lexer = Test.get_lexer('.')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DOT
        lexer = Test.get_lexer('..')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.RANGE
        lexer = Test.get_lexer('...')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ELLIPSES
        lexer = Test.get_lexer('. .')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DOT
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.WS
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DOT
        lexer = Test.get_lexer('.. ..')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.RANGE
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.WS
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.RANGE
        lexer = Test.get_lexer('... ...')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ELLIPSES
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.WS
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ELLIPSES

    def test_plus_success(self):
        lexer = Test.get_lexer('+')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.PLUS_SIGN
        lexer = Test.get_lexer('++')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.INCREMENT
        lexer = Test.get_lexer('+=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ADD_ASSIGNMENT

    def test_hyphens_success(self):
        lexer = Test.get_lexer('-')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.HYPHEN_MINUS
        lexer = Test.get_lexer('--')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DECREMENT
        lexer = Test.get_lexer('-=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.SUB_ASSIGNMENT
        lexer = Test.get_lexer('->')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.ARROW

    def test_equal_success(self):
        lexer = Test.get_lexer('=')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.EQUALS_SIGN
        lexer = Test.get_lexer('==')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.EQUAL
        lexer = Test.get_lexer('=>')
        lexer.next_lexeme()
        assert lexer.token.kind == TokenKind.DOUBLE_ARROW


if __name__ == '__main__':
    """
    """
    unittest.main()
