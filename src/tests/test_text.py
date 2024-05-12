#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text.text import Text


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

    def test_make_codepoint_success(self):
        assert Text.make_codepoint(0xD83D, 0xDE01) == 0x0001F601
        assert chr(Text.make_codepoint(0xD83D, 0xDE01)) == '😁'
        assert Text.make_codepoint(0xD83D, 0xDC0D) == 0x0001F40D
        assert chr(Text.make_codepoint(0xD83D, 0xDC0D)) == '🐍'
        ''

    def test_high_surrogate_success(self):
        assert Text.high_surrogate(0xD83D)

    def test_low_surrogate_success(self):
        assert Text.low_surrogate(0xDE01)
        assert Text.low_surrogate(0xDC0D)

    def test_letter_success(self):
        assert Text.letter(ord('A'))
        assert Text.letter(ord('Я'))
        assert Text.letter(ord('彡'))
        assert Text.letter(ord('ಠ'))
        assert Text.letter(ord('益'))
        assert Text.letter(ord('什'))

    def test_letter_number_success(self):
        assert Text.letter_number(ord('ᛯ'))
        assert Text.letter_number(ord('ⅶ'))
        assert Text.letter_number(ord('ↇ'))
        assert Text.letter_number(ord('ⅿ'))

    def test_decimal_digit_success(self):
        assert Text.decimal_digit(ord('0'))
        assert Text.decimal_digit(ord('1'))
        assert Text.decimal_digit(ord('5'))
        assert Text.decimal_digit(ord('४'))
        assert Text.decimal_digit(ord('३'))
        assert Text.decimal_digit(ord('௫'))
        assert Text.decimal_digit(ord('៥'))

    def test_hexadecimal_digit_number_success(self):
        assert Text.hexadecimal_digit(ord('0'))
        assert Text.hexadecimal_digit(ord('1'))
        assert Text.hexadecimal_digit(ord('5'))
        assert Text.hexadecimal_digit(ord('a'))
        assert Text.hexadecimal_digit(ord('b'))
        assert Text.hexadecimal_digit(ord('c'))
        assert Text.hexadecimal_digit(ord('d'))
        assert Text.hexadecimal_digit(ord('e'))
        assert Text.hexadecimal_digit(ord('f'))
        assert Text.hexadecimal_digit(ord('A'))
        assert Text.hexadecimal_digit(ord('B'))
        assert Text.hexadecimal_digit(ord('C'))
        assert Text.hexadecimal_digit(ord('D'))
        assert Text.hexadecimal_digit(ord('E'))
        assert Text.hexadecimal_digit(ord('F'))
        assert Text.hexadecimal_digit(ord('४'))
        assert Text.hexadecimal_digit(ord('३'))
        assert Text.hexadecimal_digit(ord('௫'))
        assert Text.hexadecimal_digit(ord('៥'))

    def test_spacing_mark_success(self):
        assert Text.spacing_mark(ord('ৌ'))
        assert Text.spacing_mark(ord('ૌ'))
        assert Text.spacing_mark(ord('ೊ'))
        assert Text.spacing_mark(ord('ോ'))

    def test_non_spacing_mark_success(self):
        assert Text.non_spacing_mark(ord('̚'))
        assert Text.non_spacing_mark(ord('̳'))
        assert Text.non_spacing_mark(ord('͢'))
        assert Text.non_spacing_mark(ord('ؒ'))

    def test_whitespace_success(self):
        assert Text.whitespace(ord(' '))
        assert Text.whitespace(ord('\t'))
        assert Text.whitespace(ord('\f'))
        assert Text.whitespace(0x00A0)
        assert Text.whitespace(0x205F)
        assert Text.whitespace(0x2009)
        assert Text.whitespace(0x0000200F)
        assert Text.whitespace(0x0000001A)

    def test_eol_success(self):
        assert Text.eol(ord('\n'))
        assert Text.eol(ord('\r'))
        assert Text.eol(0x0085)
        assert Text.eol(0x2028)
        assert Text.eol(0x2029)

    def test_eos_success(self):
        assert Text.eos(0x0004)
        assert Text.eos(0x2404)

    def test_underscore_success(self):
        assert Text.underscore(ord('_'))
        assert Text.underscore(ord('﹎'))
        assert Text.underscore(ord('﹏'))

    def test_connector_punctuation_success(self):
        assert Text.underscore(ord('_'))
        assert Text.underscore(ord('﹎'))
        assert Text.underscore(ord('﹏'))

    def test_dollar_sign_success(self):
        assert Text.dollar_sign(ord('$'))

    def test_currency_sign_success(self):
        assert Text.currency_sign(ord('؋'))
        assert Text.currency_sign(ord('௹'))
        assert Text.currency_sign(ord('₽'))

    def test_left_parenthesis_success(self):
        assert Text.left_parenthesis(ord('('))
        assert Text.left_parenthesis(ord('⁽'))
        assert Text.left_parenthesis(ord('₍'))
        assert Text.left_parenthesis(ord('﹙'))
        assert Text.left_parenthesis(ord('（'))
        assert Text.left_parenthesis(ord('︵'))

    def test_right_parenthesis_success(self):
        assert Text.right_parenthesis(ord(')'))
        assert Text.right_parenthesis(ord('⁾'))
        assert Text.right_parenthesis(ord('₎'))
        assert Text.right_parenthesis(ord('﹚'))
        assert Text.right_parenthesis(ord('）'))
        assert Text.right_parenthesis(ord('︶'))

    def test_left_square_bracket_success(self):
        assert Text.left_square_bracket(ord('['))
        assert Text.left_square_bracket(ord('［'))
        assert Text.left_square_bracket(ord('﹇'))

    def test_right_square_bracket_success(self):
        assert Text.right_square_bracket(ord(']'))
        assert Text.right_square_bracket(ord('］'))
        assert Text.right_square_bracket(ord('﹈'))

    def test_left_curly_bracket_success(self):
        assert Text.left_curly_bracket(ord('{'))
        assert Text.left_curly_bracket(ord('｛'))
        assert Text.left_curly_bracket(ord('﹛'))
        assert Text.left_curly_bracket(ord('︷'))

    def test_right_curly_bracket_success(self):
        assert Text.right_curly_bracket(ord('}'))
        assert Text.right_curly_bracket(ord('｝'))
        assert Text.right_curly_bracket(ord('﹜'))
        assert Text.right_curly_bracket(ord('︸'))

    def test_plus_sign_success(self):
        assert Text.plus_sign(ord('+'))
        assert Text.plus_sign(ord('＋'))
        assert Text.plus_sign(ord('﹢'))
        assert Text.plus_sign(ord('﬩'))
        assert Text.plus_sign(ord('₊'))
        assert Text.plus_sign(ord('⁺'))

    def test_hyphen_minus_success(self):
        assert Text.hyphen_minus(ord('-'))
        assert Text.hyphen_minus(ord('－'))
        assert Text.hyphen_minus(ord('﹣'))

    def test_asterisk_success(self):
        assert Text.asterisk(ord('*'))
        assert Text.asterisk(ord('＊'))
        assert Text.asterisk(ord('﹡'))

    def test_forward_slash_success(self):
        assert Text.forward_slash(ord('/'))
        assert Text.forward_slash(ord('／'))

    def test_back_slash_success(self):
        assert Text.back_slash(ord('\\'))
        assert Text.back_slash(ord('＼'))
        assert Text.back_slash(ord('﹨'))

    def test_equals_sign_success(self):
        assert Text.equals_sign(ord('='))
        assert Text.equals_sign(ord('＝'))
        assert Text.equals_sign(ord('﹦'))
        assert Text.equals_sign(ord('₌'))
        assert Text.equals_sign(ord('⁼'))

    def test_less_than_sign_success(self):
        assert Text.less_than_sign(ord('<'))
        assert Text.less_than_sign(ord('＜'))
        assert Text.less_than_sign(ord('﹤'))

    def test_greater_than_sign_success(self):
        assert Text.greater_than_sign(ord('>'))
        assert Text.greater_than_sign(ord('＞'))
        assert Text.greater_than_sign(ord('﹥'))

    def test_dot_success(self):
        assert Text.dot(ord('.'))
        assert Text.dot(ord('．'))
        assert Text.dot(ord('﹒'))

    def test_colon_success(self):
        assert Text.colon(ord(':'))
        assert Text.colon(ord('：'))
        assert Text.colon(ord('﹕'))
        assert Text.colon(ord('︓'))

    def test_comma_success(self):
        assert Text.comma(ord(','))
        assert Text.comma(ord('，'))
        assert Text.comma(ord('﹐'))
        assert Text.comma(ord('︐'))

    def test_semicolon_success(self):
        assert Text.semicolon(ord(';'))
        assert Text.semicolon(ord('；'))
        assert Text.semicolon(ord('﹔'))
        assert Text.semicolon(ord('︔'))

    def test_vertical_line_success(self):
        assert Text.vertical_line(ord('|'))
        assert Text.vertical_line(ord('｜'))

    def test_grave_accent_success(self):
        assert Text.grave_accent(ord('`'))
        assert Text.grave_accent(ord('｀'))

    def test_tilde_success(self):
        assert Text.tilde(ord('~'))
        assert Text.tilde(ord('～'))

    def test_apostrophe_success(self):
        assert Text.apostrophe(ord('\''))
        assert Text.apostrophe(ord('＇'))

    def test_exclamation_mark_success(self):
        assert Text.exclamation_mark(ord('!'))
        assert Text.exclamation_mark(ord('！'))
        assert Text.exclamation_mark(ord('︕'))
        assert Text.exclamation_mark(ord('﹗'))

    def test_question_mark_success(self):
        assert Text.question_mark(ord('?'))
        assert Text.question_mark(ord('？'))
        assert Text.question_mark(ord('︖'))
        assert Text.question_mark(ord('﹖'))

    def test_quotation_mark_success(self):
        assert Text.quotation_mark(ord('"'))
        assert Text.quotation_mark(ord('＂'))

    def test_commercial_at_success(self):
        assert Text.commercial_at(ord('@'))
        assert Text.commercial_at(ord('＠'))
        assert Text.commercial_at(ord('﹫'))

    def test_number_sign_success(self):
        assert Text.number_sign(ord('#'))
        assert Text.number_sign(ord('＃'))
        assert Text.number_sign(ord('﹟'))

    def test_percent_sign_success(self):
        assert Text.percent_sign(ord('%'))
        assert Text.percent_sign(ord('％'))
        assert Text.percent_sign(ord('﹪'))

    def test_circumflex_accent_success(self):
        assert Text.circumflex_accent(ord('^'))
        assert Text.circumflex_accent(ord('＾'))

    def test_ampersand_success(self):
        assert Text.ampersand(ord('&'))
        assert Text.ampersand(ord('＆'))
        assert Text.ampersand(ord('﹠'))

    def test_epsilon_success(self):
        assert Text.epsilon('ε')
        assert Text.epsilon('λ')

    def test_emoji_success(self):
        assert Text.emoji(ord('⌛'))
        assert Text.emoji(ord('⛳'))
        assert not Text.emoji(0x0001F1FB)
        assert Text.emoji(0x0001F52F)
        assert Text.emoji(0x0001F389)
        assert Text.emoji(0x0000274E)
        assert not Text.emoji(9220)

    def test_find_block_success(self):
        assert Text.find_block(0x00000000) == 0
        assert Text.find_block(0x00000005) == 0
        assert Text.find_block(0x00000080) == 1
        assert Text.find_block(0x00000091) == 1
        assert Text.find_block(0x00000600) == 12
        assert Text.find_block(0x00000626) == 12
        assert Text.find_block(0x00000C00) == 28
        assert Text.find_block(0x00000C56) == 28
        assert Text.find_block(0x00002C80) == 98
        assert Text.find_block(0x00002CF1) == 98
        assert Text.find_block(0x00002D00) == 99
        assert Text.find_block(0x00010200) == 171
        assert Text.find_block(0x00010201) == 171
        assert Text.find_block(0x00030000 - 2) == 368
        assert Text.find_block(0x00030000 - 1) == 368
        assert Text.find_block(0x00030000) == 369
        assert Text.find_block(0x00030000 + 1) == 369
        assert Text.find_block(0x00030000 + 2) == 369
        assert Text.find_block(0x00031350 - 1) == 369
        assert Text.find_block(0x00031350) == 370
        assert Text.find_block(0x000E0100) == 374
        assert Text.find_block(0x000E01AA) == 374
        assert Text.find_block(0x000F0000) == 376
        assert Text.find_block(0x000F0ABF) == 376
        assert Text.find_block(0x00100000) == 377

    def test_get_block_range_success(self):
        assert Text.get_block_range(0x00000000) == (0x00000000, 0x00000080 - 1)
        assert Text.get_block_range(0x00000005) == (0x00000000, 0x00000080 - 1)
        assert Text.get_block_range(0x00000080) == (0x00000080, 0x00000100 - 1)
        assert Text.get_block_range(0x00000091) == (0x00000080, 0x00000100 - 1)
        assert Text.get_block_range(0x00000600) == (0x00000600, 0x00000700 - 1)
        assert Text.get_block_range(0x00000626) == (0x00000600, 0x00000700 - 1)
        assert Text.get_block_range(0x00000C00) == (0x00000C00, 0x00000C80 - 1)
        assert Text.get_block_range(0x00000C56) == (0x00000C00, 0x00000C80 - 1)
        assert Text.get_block_range(0x00002C80) == (0x00002C80, 0x00002D00 - 1)
        assert Text.get_block_range(0x00002CF1) == (0x00002C80, 0x00002D00 - 1)
        assert Text.get_block_range(0x00002D00) == (0x00002D00, 0x00002D30 - 1)
        assert Text.get_block_range(0x00010200) == (0x00010200, 0x00010280 - 1)
        assert Text.get_block_range(0x00010201) == (0x00010200, 0x00010280 - 1)
        assert Text.get_block_range(0x00030000 - 2) == (0x0002FA20, 0x00030000 - 1)
        assert Text.get_block_range(0x00030000 - 1) == (0x0002FA20, 0x00030000 - 1)
        assert Text.get_block_range(0x00030000) == (0x00030000, 0x00031350 - 1)
        assert Text.get_block_range(0x00030000 + 1) == (0x00030000, 0x00031350 - 1)
        assert Text.get_block_range(0x00030000 + 2) == (0x00030000, 0x00031350 - 1)
        assert Text.get_block_range(0x00031350 - 1) == (0x00030000, 0x00031350 - 1)
        assert Text.get_block_range(0x00031350) == (0x00031350, 0x000323B0 - 1)
        assert Text.get_block_range(0x000E0100) == (0x000E0100, 0x000E01F0 - 1)
        assert Text.get_block_range(0x000E01AA) == (0x000E0100, 0x000E01F0 - 1)
        assert Text.get_block_range(0x000F0000) == (0x000F0000, 0x00100000 - 1)
        assert Text.get_block_range(0x000F0ABF) == (0x000F0000, 0x00100000 - 1)
        assert Text.get_block_range(0x00100000) == (0x00100000, Text.MAX_CODE_POINT)

    def test_pictographs_success(self):
        assert Text.pictographs(ord('🐍'))
        assert not Text.pictographs(ord('⛵'))
        assert not Text.pictographs(ord('⭕'))
        assert not Text.pictographs(ord('✅'))

    def test_miscellaneous_symbols_success(self):
        assert not Text.miscellaneous_symbols(ord('🐍'))
        assert Text.miscellaneous_symbols(ord('⛵'))
        assert not Text.miscellaneous_symbols(ord('⭕'))
        assert not Text.miscellaneous_symbols(ord('✅'))

    def test_dingbats_success(self):
        assert not Text.dingbats(ord('🐍'))
        assert not Text.dingbats(ord('⛵'))
        assert not Text.dingbats(ord('⭕'))
        assert Text.dingbats(ord('✅'))


if __name__ == '__main__':
    """
    """
    unittest.main()
