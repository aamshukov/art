#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.frontend.content.content import Content
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.token.tokenizer import Tokenizer


class Test(unittest.TestCase):
    class TestTokenizer(Tokenizer):
        def __init__(self, id, content, version='1.0'):
            super().__init__(id, content, version=version)
            self._k = 0

        def next_lexeme_impl(self):
            self._token = Token(TokenKind.IDENTIFIER)

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_next_codepoint_empty_success(self):
        dp = StringDataProvider('')
        data = dp.load()
        assert len(data) == 0
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == Text.eos_codepoint()
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_next_codepoint_a_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == 'A'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_next_codepoint_ab_success(self):
        dp = StringDataProvider('AB')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == 'A'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'B'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_next_codepoint_snake_success(self):
        dp = StringDataProvider('🐍')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_next_codepoint_smile_snake_success(self):
        dp = StringDataProvider('😁🐍')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '😁'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escape_u_success(self):
        dp = StringDataProvider(r'\uD83D\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()
        dp = StringDataProvider(r'\uuD83D\uuuuDC0D')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escape_u_slashes_success(self):
        dp = StringDataProvider(r'\\\uD83D\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()
        dp = StringDataProvider(r'\uD83D\\\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '�'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escape_u_broken_success(self):
        dp = StringDataProvider(r'\uD83DA\\')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uD83DA\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uD8\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uD\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\u\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'u'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'D'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'C'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '0'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'D'
        dp = StringDataProvider(r'\uDC0D')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uDC0')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uDC')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\uD')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\u')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        dp = StringDataProvider(r'\\')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escape_U_success(self):
        dp = StringDataProvider(r'\\\U0001F40D')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '\\'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()
        dp = StringDataProvider(r'\U0001F40')
        data = dp.load()
        content = Content(0, data, '')
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == '�'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escape_U_full_success(self):
        dp = StringDataProvider(r'abc\U0001F40Dသန彡xyz你叫什么名字Я')
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == 'a'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'b'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'c'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '🐍'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'သ'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'န'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '彡'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'x'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'y'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'z'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '你'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '叫'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '什'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '么'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '名'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == '字'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == 'Я'
        codepoint = tokenizer.next_codepoint()
        assert codepoint == Text.eos_codepoint()

    def test_unicode_escaped_U_success(self):
        string = 'a🐍ba🐍bcline (ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥ အသုံးပြုနိုㄒㄖㄒ卄乇1F40Dသန彡xyz你叫什么名字 ' \
                 'детства хотел завести 🐍Я'
        escaped_data = r'a🐍b\u0061\uD83D\uDC0D\u0062\u0063\u006C\u0069\u006E\u0065\u0020\u0028\u30CE\u0CA0\u76CA' \
                       r'\u0CA0\u0029\u30CE\u5F61\u0020\u0279\u006F\u0287\u0131\u0070\u018E\u0020\u0287\u0078' \
                       r'\u01DD\u22A5\u0020\u1021\u101E\u102F\u1036\u1038\u1015\u103C\u102F\u1014\u102D\u102F' \
                       r'\u3112\u3116\u3112\u5344\u4E47\u0031\u0046\u0034\u0030\u0044\u101E\u1014\u5F61\u0078' \
                       r'\u0079\u007A\u4F60\u53EB\u4EC0\u4E48\u540D\u5B57\u0020\u0434\u0435\u0442\u0441\u0442' \
                       r'\u0432\u0430\u0020\u0445\u043E\u0442\u0435\u043B\u0020\u0437\u0430\u0432\u0435\u0441' \
                       r'\u0442\u0438\u0020\uD83D\uDC0D\u042F'
        dp = StringDataProvider(escaped_data)
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        tokenizer = Test.TestTokenizer(0, content)
        codepoint = tokenizer.codepoint
        assert codepoint == string[0]
        for k in range(1, len(string)):
            codepoint = tokenizer.next_codepoint()
            print(k)
            assert codepoint == string[k]


if __name__ == '__main__':
    """
    """
    unittest.main()
