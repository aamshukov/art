#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.core.source import Source
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.data_provider.file_data_provider import FileDataProvider
from art.framework.frontend.content.content import Content


class Test(unittest.TestCase):
    def test_content_string_data_provider_0_success(self):
        dp = StringDataProvider('')
        data = dp.load()
        assert len(data) == 0
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_1_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Я')
        data = dp.load()
        assert len(data) == 1
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('乇')
        data = dp.load()
        assert len(data) == 1
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('သ')
        data = dp.load()
        assert len(data) == 1
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_2_success(self):
        dp = StringDataProvider('AB')
        data = dp.load()
        assert len(data) == 2
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Яд')
        data = dp.load()
        assert len(data) == 2
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ಠ益')
        data = dp.load()
        assert len(data) == 2
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('်ဂ')
        data = dp.load()
        assert len(data) == 2
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_string_data_provider_3_success(self):
        dp = StringDataProvider('AcB')
        data = dp.load()
        assert len(data) == 3
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('Яхд')
        data = dp.load()
        assert len(data) == 3
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ಠノ彡')
        data = dp.load()
        assert len(data) == 3
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        dp = StringDataProvider('ို့')
        data = dp.load()
        assert len(data) == 3
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        bs = str.encode(data, 'utf-8')
        dp = StringDataProvider(bs, raw_bytes=True)
        data0 = dp.load()
        assert len(data) == 3
        assert Text.equal(data, data0)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_0_success(self):
        dp = FileDataProvider(Source(0, r'data/ascii-0.txt'))
        data = dp.load()
        assert len(data) == 0
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_1_success(self):
        dp = FileDataProvider(Source(0, r'data/ascii-1.txt'))
        data = dp.load()
        assert len(data) == 1
        assert Text.equal(data, 'A')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_ascii_2_success(self):
        dp = FileDataProvider(Source(0, r'data/ascii-2.txt'))
        data = dp.load()
        assert len(data) == 2
        assert Text.equal(data, 'AB')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_0_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-0.txt'))
        data = dp.load()
        assert len(data) == 0
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_1_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-1.txt'))
        data = dp.load()
        assert len(data) == 1
        assert Text.equal(data, '彡')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_2_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-2.txt'))
        data = dp.load()
        assert len(data) == 2
        assert Text.equal(data, '်ဂ')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_3_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-3.txt'))
        data = dp.load()
        assert len(data) == 3
        assert Text.equal(data, 'дЕA')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf8_4_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-4.txt'))
        data = dp.load()
        assert len(data) == 4
        assert Text.equal(data, '你叫什么')
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    TEXT = "Rit Rite ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥', '(ノಠ益ಠ)ノ彡 ɹoʇıpƎ ʇxǝ⊥ 你叫什么名字သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် \r\n" \
           "တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင်  多少钱 အင်တာနက်မရှိချိန်တွင်လည်း offline အသုံးပြုနိုင်တဲ့ converter တစ် \r\n" \
           "သည် ဇော်ဂျီ နှင့် မြန်မာ ယူနီကုတ် တို့ကို အပြန်အလှန် ပြောင်းပေးနိုင်သည့်အပြင် အင်တာနက်မရှိချိန်တွင်လည်း  offline\r\n" \
           " အသုံးပြုနိုင်တဲ့ converter တစ် Я с детства хотел завести собаку', 'Я с детства хотел завести собакуЯ \r\n" \
           "c детства хотел завести собаку', 'Я с детства хотел завести собаку  english text  \r\n" \
           "山乇ㄥ匚ㄖ爪乇　ㄒㄖ　ㄒ卄乇　爪ㄖ丂ㄒ　匚ㄖ爪卩ㄥ乇ㄒ乇　ﾌ卂卩卂几乇丂乇你想去哪里xyz"

    def test_content_file_data_provider_utf8_success(self):
        dp = FileDataProvider(Source(0, r'data/utf8-text.txt'))
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf16_BE_success(self):
        dp = FileDataProvider(Source(0, r'data/utf16-BE-text.txt'))
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf16_LE_success(self):
        dp = FileDataProvider(Source(0, r'data/utf16-LE-text.txt'))
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf32_BE_success(self):
        dp = FileDataProvider(Source(0, r'data/utf32-BE-text.txt'))
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)

    def test_content_file_data_provider_utf32_LE_success(self):
        dp = FileDataProvider(Source(0, r'data/utf32-LE-text.txt'))
        data = dp.load()
        assert len(data) == len(Test.TEXT)
        assert Text.equal(data, Test.TEXT)
        content = Content(data, Source(0, ''))
        assert len(data) == content.count
        assert Text.equal(data, content.data)


if __name__ == '__main__':
    """
    """
    unittest.main()
