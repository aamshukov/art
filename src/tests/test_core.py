#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest

from art.framework.core.domain_helper import DomainHelper
from art.framework.core.flags import Flags
from art.framework.core.logger import Logger
from art.framework.core.text import Text


class Test(unittest.TestCase):
    def test_logger_success(self):
        path = r'd:\tmp'
        logger = Logger(path=path)
        logger.debug('kuku')
        assert os.path.exists(os.path.join(path, f'{Logger.LOGGER_NAME}.log'))

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

    def test_modify_flags_success(self):
        flags = Flags.DIRTY | Flags.PROCESSED | Flags.VISITED | Flags.LEAF | Flags.INVALID
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.PROCESSED == Flags.PROCESSED
        assert flags & Flags.VISITED == Flags.VISITED
        assert flags & Flags.LEAF == Flags.LEAF
        assert flags & Flags.INVALID == Flags.INVALID
        flags = Flags.modify_flags(flags,
                                   Flags.GENUINE | Flags.SYNTHETIC, Flags.PROCESSED | Flags.VISITED | Flags.INVALID)
        assert flags & Flags.DIRTY == Flags.DIRTY
        assert flags & Flags.GENUINE == Flags.GENUINE
        assert flags & Flags.SYNTHETIC == Flags.SYNTHETIC

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

    def test_epsilon_success(self):
        assert DomainHelper.real_numbers_equal(0.0, 0.0)
        assert DomainHelper.real_numbers_equal(DomainHelper.epsilon(), DomainHelper.epsilon())
        assert DomainHelper.real_numbers_equal(0.1, 0.1)
        assert not DomainHelper.real_numbers_equal(0.0000001, 0.00010001)
        assert DomainHelper.real_numbers_equal(47264780.00027800001, 47264780.00027800001)
        assert DomainHelper.real_numbers_equal(47264780E+27, 47264780E+27)
        assert DomainHelper.real_numbers_equal(47264780E-28, 47264780E-27)


if __name__ == '__main__':
    """
    """
    unittest.main()
