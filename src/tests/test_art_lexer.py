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
                  TokenKind.INTEGER,
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
        tokens = [TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.IDENTIFIER,
                  TokenKind.WS,
                  TokenKind.INTEGER,
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
        program = """
        def foo()

            a1


                 a2
                     a3
                         a4
                         a5
                 a6
                 a7
        
            a8
        """
        # Test.evaluate(program, tokens)

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


if __name__ == '__main__':
    """
    """
    unittest.main()
