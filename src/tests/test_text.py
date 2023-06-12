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

    def test_number_success(self):
        assert Text.number('0')
        assert Text.number('1')
        assert Text.number('5')
        assert Text.number('४')
        assert Text.number('३')
        assert Text.number('௫')
        assert Text.number('៥')

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

    def test_eol_success(self):
        assert Text.eol('\n')
        assert Text.eol('\r')

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


if __name__ == '__main__':
    """
    """
    unittest.main()
