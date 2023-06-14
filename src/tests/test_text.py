#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.core.text import Text


class Test(unittest.TestCase):
    def test_strings_equality_success(self):
        assert Text.equal('', '')
        assert Text.equal('Rit\u0113', 'Rite\u0304')
        assert not Text.equal('', ' ')
        assert Text.equal('(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥')
        assert Text.equal('သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                          'offline အသုံးပြုနိုင်တဲ့ converter တစ်',
                          'သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                          'offline အသုံးပြုနိုင်တဲ့ converter တစ်')
        assert Text.equal('Я с детства хотел завести собаку', 'Я с детства хотел завести собаку')
        assert not Text.equal('Я c детства хотел завести собаку', 'Я с детства хотел завести собаку')
        assert Text.equal('english text', 'english text')
        assert Text.equal('山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇',
                          '山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇')
        assert Text.equal('enGlisH texT', 'EngLish TeXt', case_insensitive=True)
        assert Text.equal('Я с дЕТства хоТЕЛ зАВестИ Собаку', 'я с деТСтвА ХотЕЛ ЗАВЕСТИ СОБАКУ', case_insensitive=True)

    def test_strings_compare_success(self):
        assert Text.compare('', '') == 0
        assert Text.compare('Rit\u0113', 'Rite\u0304') == 0
        assert Text.compare('', ' ') == -1
        assert Text.compare('(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥') == 0
        assert Text.compare('သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                            'offline အသုံးပြုနိုင်တဲ့ converter တစ်',
                            'သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း '
                            'offline အသုံးပြုနိုင်တဲ့ converter တစ်') == 0
        assert Text.compare('Я с детства хотел завести собаку', 'Я с детства хотел завести собаку') == 0
        assert Text.compare('Я c детства хотел завести собаку', 'Я с детства хотел завести собаку') == -1
        assert Text.compare('english text', 'english text') == 0
        assert Text.compare('山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇',
                            '山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇') == 0
        assert Text.compare('enGlisH texT', 'EngLish TeXt', case_insensitive=True) == 0
        assert Text.compare('Я с дЕТства хоТЕЛ зАВестИ Собаку',
                            'я с деТСтвА ХотЕЛ ЗАВЕСТИ СОБАКУ',
                            case_insensitive=True) == 0
        assert Text.compare('habit', 'hat') == -1
        assert Text.compare('bat', 'bail') == 1
        assert Text.compare('HELLO', 'Hello') == -1
        assert Text.compare('HELLO', 'Hello', case_insensitive=True) == 0

    def test_collect_by_category(self):
        Text.collect_by_category('Cf')

    def test_string_kind_success(self):
        kind = Text.get_string_kind('a')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('Я')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('爪')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('🐍')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND
        kind = Text.get_string_kind('သည်')
        print(kind)
        # assert kind == Text.PyUnicodeObject.PyUnicode_2BYTE_KIND

    def test_concatenate_strings_with_sentinels_success(self):
        s = Text.concatenate_strings_with_sentinels(['one', 'two', 'three'])
        assert s == 'one\x00two\x01three\x02'

    def test_generate_random_string_success(self):
        assert len(Text.generate_random_string(100)) == 100

    def test_find_all_substrings_success(self):
        assert (Text.find_all_substrings('Я с детства хотел завести собакуЯ с детства хотел завести собаку', 'о') ==
                [13, 27, 45, 59])

    def test_epsilon_codepoint_success(self):
        assert Text.epsilon_codepoint(ord('ε'))

    def test_epsilon_success(self):
        assert Text.epsilon('ε')

    def test_identifier_start_success(self):
        assert Text.identifier_start('a')
        assert Text.identifier_start('_')
        assert Text.identifier_start('$')
        assert Text.identifier_start('﹍')
        assert Text.identifier_start('Я')
        assert Text.identifier_start('彡')
        assert Text.identifier_start('ಠ')
        assert Text.identifier_start('益')
        assert Text.identifier_start('什')
        assert Text.identifier_start('သ')

    def test_identifier_part_success(self):
        assert Text.identifier_part('a')
        assert Text.identifier_part('_')
        assert Text.identifier_part('$')
        assert Text.identifier_part('﹍')
        assert Text.identifier_part('Я')
        assert Text.identifier_part('彡')
        assert Text.identifier_part('ಠ')
        assert Text.identifier_part('益')
        assert Text.identifier_part('什')
        assert Text.identifier_part('်')

    def test_letter_success(self):
        assert Text.letter('A')
        assert Text.letter('Я')
        assert Text.letter('彡')
        assert Text.letter('ಠ')
        assert Text.letter('益')
        assert Text.letter('什')

    def test_decimal_digit_number_success(self):
        assert Text.decimal_digit_number('0')
        assert Text.decimal_digit_number('1')
        assert Text.decimal_digit_number('5')
        assert Text.decimal_digit_number('४')
        assert Text.decimal_digit_number('३')
        assert Text.decimal_digit_number('௫')
        assert Text.decimal_digit_number('៥')

    def test_hexadecimal_digit_number_success(self):
        assert Text.hexadecimal_digit('0')
        assert Text.hexadecimal_digit('1')
        assert Text.hexadecimal_digit('5')
        assert Text.hexadecimal_digit('a')
        assert Text.hexadecimal_digit('b')
        assert Text.hexadecimal_digit('c')
        assert Text.hexadecimal_digit('d')
        assert Text.hexadecimal_digit('e')
        assert Text.hexadecimal_digit('f')
        assert Text.hexadecimal_digit('A')
        assert Text.hexadecimal_digit('B')
        assert Text.hexadecimal_digit('C')
        assert Text.hexadecimal_digit('D')
        assert Text.hexadecimal_digit('E')
        assert Text.hexadecimal_digit('F')
        assert Text.hexadecimal_digit('४')
        assert Text.hexadecimal_digit('३')
        assert Text.hexadecimal_digit('௫')
        assert Text.hexadecimal_digit('៥')

    def test_letter_number_success(self):
        assert Text.letter_number('ᛯ')
        assert Text.letter_number('ⅶ')
        assert Text.letter_number('ↇ')
        assert Text.letter_number('ⅿ')

    def test_spacing_mark_success(self):
        assert Text.spacing_mark('ৌ')
        assert Text.spacing_mark('ૌ')
        assert Text.spacing_mark('ೊ')
        assert Text.spacing_mark('ോ')

    def test_non_spacing_mark_success(self):
        assert Text.non_spacing_mark('̚')
        assert Text.non_spacing_mark('̳')
        assert Text.non_spacing_mark('͢')
        assert Text.non_spacing_mark('ؒ')

    def test_whitespace_success(self):
        assert Text.whitespace(' ')
        assert Text.whitespace('\t')
        assert Text.whitespace('\f')
        assert Text.whitespace(chr(0x00A0))
        assert Text.whitespace(chr(0x205F))
        assert Text.whitespace(chr(0x2009))

    def test_eol_success(self):
        assert Text.eol('\n')
        assert Text.eol('\r')
        assert Text.eol(chr(0x0085))
        assert Text.eol(chr(0x2028))
        assert Text.eol(chr(0x2029))

    def test_eos_success(self):
        assert Text.eos(chr(0x0004))
        assert Text.eos(chr(0x2404))

    def test_underscore_success(self):
        assert Text.underscore('_')
        assert Text.underscore('﹎')
        assert Text.underscore('﹏')

    def test_connector_punctuation_success(self):
        assert Text.underscore('_')
        assert Text.underscore('﹎')
        assert Text.underscore('﹏')

    def test_dollar_sign_success(self):
        assert Text.dollar_sign('$')

    def test_currency_sign_success(self):
        assert Text.currency_sign('؋')
        assert Text.currency_sign('௹')
        assert Text.currency_sign('₽')

    def test_left_parenthesis_success(self):
        assert Text.left_parenthesis('(')
        assert Text.left_parenthesis('⁽')
        assert Text.left_parenthesis('₍')
        assert Text.left_parenthesis('﹙')
        assert Text.left_parenthesis('（')
        assert Text.left_parenthesis('︵')

    def test_right_parenthesis_success(self):
        assert Text.right_parenthesis(')')
        assert Text.right_parenthesis('⁾')
        assert Text.right_parenthesis('₎')
        assert Text.right_parenthesis('﹚')
        assert Text.right_parenthesis('）')
        assert Text.right_parenthesis('︶')

    def test_left_square_bracket_success(self):
        assert Text.left_square_bracket('[')
        assert Text.left_square_bracket('［')
        assert Text.left_square_bracket('﹇')

    def test_right_square_bracket_success(self):
        assert Text.right_square_bracket(']')
        assert Text.right_square_bracket('］')
        assert Text.right_square_bracket('﹈')

    def test_left_curly_bracket_success(self):
        assert Text.left_curly_bracket('{')
        assert Text.left_curly_bracket('｛')
        assert Text.left_curly_bracket('﹛')
        assert Text.left_curly_bracket('︷')

    def test_right_curly_bracket_success(self):
        assert Text.right_curly_bracket('}')
        assert Text.right_curly_bracket('｝')
        assert Text.right_curly_bracket('﹜')
        assert Text.right_curly_bracket('︸')

    def test_plus_sign_success(self):
        assert Text.plus_sign('+')
        assert Text.plus_sign('＋')
        assert Text.plus_sign('﹢')
        assert Text.plus_sign('﬩')
        assert Text.plus_sign('₊')
        assert Text.plus_sign('⁺')

    def test_hyphen_minus_success(self):
        assert Text.hyphen_minus('-')
        assert Text.hyphen_minus('－')
        assert Text.hyphen_minus('﹣')

    def test_asterisk_success(self):
        assert Text.asterisk('*')
        assert Text.asterisk('＊')
        assert Text.asterisk('﹡')

    def test_forward_slash_success(self):
        assert Text.forward_slash('/')
        assert Text.forward_slash('／')

    def test_back_slash_success(self):
        assert Text.back_slash('\\')
        assert Text.back_slash('＼')
        assert Text.back_slash('﹨')

    def test_equals_sign_success(self):
        assert Text.equals_sign('=')
        assert Text.equals_sign('＝')
        assert Text.equals_sign('﹦')
        assert Text.equals_sign('₌')
        assert Text.equals_sign('⁼')

    def test_less_than_sign_success(self):
        assert Text.less_than_sign('<')
        assert Text.less_than_sign('＜')
        assert Text.less_than_sign('﹤')

    def test_greater_than_sign_success(self):
        assert Text.greater_than_sign('>')
        assert Text.greater_than_sign('＞')
        assert Text.greater_than_sign('﹥')

    def test_dot_success(self):
        assert Text.dot('.')
        assert Text.dot('．')
        assert Text.dot('﹒')

    def test_colon_success(self):
        assert Text.colon(':')
        assert Text.colon('：')
        assert Text.colon('﹕')
        assert Text.colon('︓')

    def test_comma_success(self):
        assert Text.comma(',')
        assert Text.comma('，')
        assert Text.comma('﹐')
        assert Text.comma('︐')

    def test_semicolon_success(self):
        assert Text.semicolon(';')
        assert Text.semicolon('；')
        assert Text.semicolon('﹔')
        assert Text.semicolon('︔')

    def test_vertical_line_success(self):
        assert Text.vertical_line('|')
        assert Text.vertical_line('｜')

    def test_grave_accent_success(self):
        assert Text.grave_accent('`')
        assert Text.grave_accent('｀')
        assert Text.grave_accent('`')

    def test_tilde_success(self):
        assert Text.tilde('~')
        assert Text.tilde('～')

    def test_apostrophe_success(self):
        assert Text.apostrophe('\'')
        assert Text.apostrophe('＇')

    def test_exclamation_mark_success(self):
        assert Text.exclamation_mark('!')
        assert Text.exclamation_mark('！')
        assert Text.exclamation_mark('︕')
        assert Text.exclamation_mark('﹗')

    def test_question_mark_success(self):
        assert Text.question_mark('?')
        assert Text.question_mark('？')
        assert Text.question_mark('︖')
        assert Text.question_mark('﹖')

    def test_quotation_mark_success(self):
        assert Text.quotation_mark('"')
        assert Text.quotation_mark('＂')

    def test_commercial_at_success(self):
        assert Text.commercial_at('@')
        assert Text.commercial_at('＠')
        assert Text.commercial_at('﹫')

    def test_number_sign_success(self):
        assert Text.number_sign('#')
        assert Text.number_sign('＃')
        assert Text.number_sign('﹟')

    def test_percent_sign_success(self):
        assert Text.percent_sign('%')
        assert Text.percent_sign('％')
        assert Text.percent_sign('﹪')

    def test_circumflex_accent_success(self):
        assert Text.circumflex_accent('^')
        assert Text.circumflex_accent('＾')

    def test_ampersand_success(self):
        assert Text.ampersand('&')
        assert Text.ampersand('＆')
        assert Text.ampersand('﹠')

    def test_make_codepoint_success(self):
        assert Text.make_codepoint(0xD83D, 0xDE01) == 0x0001F601
        assert chr(Text.make_codepoint(0xD83D, 0xDE01)) == '😁'
        assert Text.make_codepoint(0xD83D, 0xDC0D) == 0x0001F40D
        assert chr(Text.make_codepoint(0xD83D, 0xDC0D)) == '🐍'

    def test_high_surrogate_success(self):
        assert Text.high_surrogate(0xD83D)

    def test_low_surrogate_success(self):
        assert Text.low_surrogate(0xDE01)
        assert Text.low_surrogate(0xDC0D)


if __name__ == '__main__':
    """
    """
    unittest.main()
