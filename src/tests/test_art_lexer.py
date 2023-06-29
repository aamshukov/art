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
    def evaluate(program, tokens):
        literals = list()
        lexer = Test.get_lexer(program)
        for k, token in enumerate(tokens):
            lexer.next_lexeme()
            assert lexer.token.kind == TokenKind(token)
            literals.append(lexer.token.literal)
        return literals

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
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_empty_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '""'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_1_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '" "'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_2_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = '" a "'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = r'"\"prefix \" 😁🐍 ⏩⏰⌚⏳☔♈ \uD83D\uDC0D ♿ \U0001F40Dသန彡xyz你叫什么名字Я ⚓⚡⚪⚽⛄⛎⛔⛪⛲⛵⛺⛽✅✊✨❌❎❓❗➕➰➿⬛⭐⭕🀄🃏🆎🆑🈁🈚🈯🈲🈸🉐🌀\""'  # noqa
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_single_quote_success(self):
        tokens = [TokenKind.STRING,
                  TokenKind.EOS]
        program = r"'\'prefix \' 😁🐍 ⏩⏰⌚⏳☔♈ \uD83D\uDC0D ♿ \U0001F40Dသန彡xyz你叫什么名字Я ⚓⚡⚪⚽⛄⛎⛔⛪⛲⛵⛺⛽✅✊✨❌❎❓❗➕➰➿⬛⭐⭕🀄🃏🆎🆑🈁🈚🈯🈲🈸🉐🌀\''"  # noqa
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_eos_success(self):
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = r'"abc'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program

    def test_string_eol_success(self):
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOL,
                  TokenKind.INDENT,
                  TokenKind.EOS]
        program = """'a
        """
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == "'a"

    def test_single_line_number_sign_comments_success(self):
        tokens = [TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '# 123'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '   # 123'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '   '
        assert literals[1] == '# 123'

    def test_single_line_comments_success(self):
        tokens = [TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '// 123'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.WS,
                  TokenKind.SINGLE_LINE_COMMENT,
                  TokenKind.EOS]
        program = '   // 123'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '   '
        assert literals[1] == '// 123'

    def test_multi_line_comments_success(self):
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/**/'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* */'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* 123 */'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.WS,
                  TokenKind.MULTI_LINE_COMMENT,
                  TokenKind.EOS]
        program = '/* /**/ /* /* /* */ */ */ */ /* */'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == '/* /**/ /* /* /* */ */ */ */'
        assert literals[1] == ' '
        assert literals[2] == '/* */'
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/**'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/*'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program
        tokens = [TokenKind.UNKNOWN,
                  TokenKind.EOS]
        program = '/* /*/ /* /* /* */ */ */ */ /* */'
        literals = Test.evaluate(program, tokens)
        assert len(literals) == len(tokens)
        assert literals[0] == program


if __name__ == '__main__':
    """
    """
    unittest.main()
