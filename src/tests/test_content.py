#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.data_provider.file_data_provider import FileDataProvider
from art.framework.frontend.content.content import Content


class Test(unittest.TestCase):
    def test_content_string_data_provider_0_success(self):
        dp = StringDataProvider('')
        data = dp.load()
        assert len(data) == 0
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_1_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Я')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('乇')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('သ')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_2_success(self):
        dp = StringDataProvider('AB')
        data = dp.load()
        assert len(data) == 2
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Яд')
        data = dp.load()
        assert len(data) == 2
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ಠ益')
        data = dp.load()
        assert len(data) == 2
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('်ဂ')
        data = dp.load()
        assert len(data) == 2
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_3_success(self):
        dp = StringDataProvider('AcB')
        data = dp.load()
        assert len(data) == 3
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Яхд')
        data = dp.load()
        assert len(data) == 3
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ಠノ彡')
        data = dp.load()
        assert len(data) == 3
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ို့')
        data = dp.load()
        assert len(data) == 3
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        bs = str.encode(data, 'utf-8')
        dp = StringDataProvider(bs, raw_bytes=True)
        data0 = dp.load()
        assert len(data) == 3
        assert Text.equal(data, data0)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_0_success(self):
        dp = FileDataProvider(r'data/ascii-0.txt')
        data = dp.load()
        assert len(data) == 0
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_1_success(self):
        dp = FileDataProvider(r'data/ascii-1.txt')
        data = dp.load()
        assert len(data) == 1
        assert Text.equal(data, 'A')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_2_success(self):
        dp = FileDataProvider(r'data/ascii-2.txt')
        data = dp.load()
        assert len(data) == 2
        assert Text.equal(data, 'AB')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_0_success(self):
        dp = FileDataProvider(r'data/utf8-0.txt')
        data = dp.load()
        assert len(data) == 0
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_1_success(self):
        dp = FileDataProvider(r'data/utf8-1.txt')
        data = dp.load()
        assert len(data) == 1
        assert Text.equal(data, '彡')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_2_success(self):
        dp = FileDataProvider(r'data/utf8-2.txt')
        data = dp.load()
        assert len(data) == 2
        assert Text.equal(data, '်ဂ')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_3_success(self):
        dp = FileDataProvider(r'data/utf8-3.txt')
        data = dp.load()
        assert len(data) == 3
        assert Text.equal(data, 'дЕA')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_4_success(self):
        dp = FileDataProvider(r'data/utf8-4.txt')
        data = dp.load()
        assert len(data) == 4
        assert Text.equal(data, '你叫什么')
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    TEXT = "Rit Rite ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥ 你叫什么名字သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် \r\n" \
           "တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင်  多少钱 အင်တာနက်မရှိချိန်တွင်လည်း offline အသုံးပြုနိုင်တဲ့ converter တစ် \r\n" \
           "သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း  offline\r\n" \
           " အသုံးပြုနိုင်တဲ့ converter တစ် Я с детства хотел завести собаку', 'Я с детства хотел завести собакуЯ \r\n" \
           "c детства хотел завести собаку', 'Я с детства хотел завести собаку  english text  \r\n" \
           "山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇你想去哪里xyz"

    TABBED_TEXT = "Rit\t\tRite ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥ (ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥ 你叫什么名字သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် Z\r\n" \
           "တို့ကို\t\t အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင်  多少钱 အင်တာနက်မရှိချိန်တွင်လည်း offline အသုံးပြုနိုင်တဲ့ converter တစ် \r\n" \
           "သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း  offline\r\n" \
           " အသုံးပြုနိုင်တဲ့ converter တစ် Я с детства хотел завести собаку', 'Я с детства хотел завести собакуЯ \r\n" \
           "c дет\tства хотел завести собаку', 'Я с детства хотел завести собаку  english text  \r\n" \
           "山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇你想去哪里\txyz"

    def test_content_file_data_provider_utf8_success(self):
        dp = FileDataProvider(r'data/utf8-text.txt')
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf16_BE_success(self):
        dp = FileDataProvider(r'data/utf16-BE-text.txt')
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf16_LE_success(self):
        dp = FileDataProvider(r'data/utf16-LE-text.txt')
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf32_BE_success(self):
        dp = FileDataProvider(r'data/utf32-BE-text.txt')
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf32_LE_success(self):
        dp = FileDataProvider(r'data/utf32-LE-text.txt')
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_build_line_map_success(self):
        dp = StringDataProvider('')  # line map has no entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1')  # line map has 1 entry
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1\n')  # line map has 1 entry
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1\n\n\n')  # line map has 3 entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1\nLine 2\nLine 3')  # line map has 3 entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1\nLine 2\nLine 3\n')  # line map has 3 entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Line 1\n\nLine 3\n\nLine5')  # line map has 5 entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider(Test.TEXT)
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        dp = StringDataProvider('Lin\te 1\n\nLi\t\t\tne 3\n\nLin\t\t\t\te5')  # line map has 5 entries
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()

    def test_content_location_success(self):
        dp = StringDataProvider(Test.TABBED_TEXT)
        data = dp.load()
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        assert(content.get_line(0) == Content.FIRST_LINE)
        assert(content.get_column(0) == Content.FIRST_COLUMN)
        assert(content.get_line(1) == Content.FIRST_LINE)
        assert(content.get_column(1) == 1)
        assert(content.get_line(3) == Content.FIRST_LINE)
        assert(content.get_column(3) == 3)
        assert(content.get_column(4) == 4)
        assert(content.get_column(5) == 8)
        assert(content.get_column(6) == 9)
        assert(content.get_column(7) == 10)
        assert(content.get_column(8) == 11)
        assert(content.get_line(91) == 0)
        assert(content.get_line(92) == 0)
        assert(content.get_line(93) == 0)
        assert(content.get_line(94) == 1)

    def test_content_location_no_tabs_success(self):
        dp = StringDataProvider(Test.TABBED_TEXT)
        data = dp.load()
        content = Content(0, data, '', tab_size=0)
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        content.build_line_map()
        assert(content.get_line(0) == Content.FIRST_LINE)
        assert(content.get_column(0) == Content.FIRST_COLUMN)
        assert(content.get_line(1) == Content.FIRST_LINE)
        assert(content.get_column(1) == 1)
        assert(content.get_line(3) == Content.FIRST_LINE)
        assert(content.get_column(3) == 3)
        assert(content.get_column(4) == 4)
        assert(content.get_column(5) == 5)
        assert(content.get_column(6) == 6)
        assert(content.get_column(7) == 7)
        assert(content.get_column(8) == 8)
        assert(content.get_line(91) == 0)
        assert(content.get_line(92) == 0)
        assert(content.get_line(93) == 0)
        assert(content.get_line(94) == 1)


if __name__ == '__main__':
    """
    """
    unittest.main()
