#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String extensions """
import sys
import ctypes
import functools
import random
import string
import unicodedata
from art.framework.core.base import Base


class Text(Base):
    """
    """
    CATEGORY_UPPERCASE_LETTER = 1            # Lu
    CATEGORY_LOWERCASE_LETTER = 2            # Ll
    CATEGORY_TITLECASE_LETTER = 3            # Lt
    CATEGORY_MODIFIER_LETTER = 4             # Lm
    CATEGORY_OTHER_LETTER = 5                # Lo

    CATEGORY_NON_SPACING_MARK = 6            # Mn
    CATEGORY_ENCLOSING_MARK = 7              # Me
    CATEGORY_COMBINING_SPACING_MARK = 8      # Mc

    CATEGORY_DECIMAL_DIGIT_NUMBER = 9        # Nd
    CATEGORY_LETTER_NUMBER = 10              # Nl
    CATEGORY_OTHER_NUMBER = 11               # No

    CATEGORY_CONNECTOR_PUNCTUATION = 12      # Pc
    CATEGORY_DASH_PUNCTUATION = 13           # Pd
    CATEGORY_START_PUNCTUATION = 14          # Ps
    CATEGORY_END_PUNCTUATION = 15            # Pe
    CATEGORY_INITIAL_QUOTE_PUNCTUATION = 16  # Pi
    CATEGORY_FINAL_QUOTE_PUNCTUATION = 17    # Pf
    CATEGORY_OTHER_PUNCTUATION = 18          # Po

    CATEGORY_MATH_SYMBOL = 19                # Sm
    CATEGORY_CURRENCY_SYMBOL = 20            # Sc
    CATEGORY_MODIFIER_SYMBOL = 21            # Sk
    CATEGORY_OTHER_SYMBOL = 22               # So

    CATEGORY_SPACE_SEPARATOR = 23            # Zs
    CATEGORY_LINE_SEPARATOR = 24             # Zl
    CATEGORY_PARAGRAPH_SEPARATOR = 25        # Zp

    CATEGORY_CONTROL = 26                    # Cc
    CATEGORY_FORMAT = 27                     # Cf
    CATEGORY_PRIVATE_USE = 28                # Co
    CATEGORY_SURROGATE = 29                  # Cs
    CATEGORY_UNASSIGNED = 30                 # Cn

    MIN_CODE_POINT = 0x00000000
    MAX_CODE_POINT = 0x0010FFFF

    UNICODE_BLOCK_STARTS = [
        0x00000000,  # 0000 - 007F     Basic Latin
        0x00000080,  # 0080 - 00FF     Latin-1 Supplement
        0x00000100,  # 0100 - 017F     Latin Extended-A
        0x00000180,  # 0180 - 024F     Latin Extended-B
        0x00000250,  # 0250 - 02AF     IPA Extensions
        0x000002B0,  # 02B0 - 02FF     Spacing Modifier Letters
        0x00000300,  # 0300 - 036F     Combining Diacritical Marks
        0x00000370,  # 0370 - 03FF     Greek and Coptic
        0x00000400,  # 0400 - 04FF     Cyrillic
        0x00000500,  # 0500 - 052F     Cyrillic Supplement
        0x00000530,  # 0530 - 058F     Armenian
        0x00000590,  # 0590 - 05FF     Hebrew
        0x00000600,  # 0600 - 06FF     Arabic
        0x00000700,  # 0700 - 074F     Syriac
        0x00000750,  # 0750 - 077F     Arabic Supplement
        0x00000780,  # 0780 - 07BF     Thaana
        0x000007C0,  # 07C0 - 07FF     NKo
        0x00000800,  # 0800 - 083F     Samaritan
        0x00000840,  # 0840 - 085F     Mandaic
        0x00000860,  # 0860 - 086F     Syriac Supplement
        0x00000870,  # 0870 - 089F     Arabic Extended-B
        0x000008A0,  # 08A0 - 08FF     Arabic Extended-A
        0x00000900,  # 0900 - 097F     Devanagari
        0x00000980,  # 0980 - 09FF     Bengali
        0x00000A00,  # 0A00 - 0A7F     Gurmukhi
        0x00000A80,  # 0A80 - 0AFF     Gujarati
        0x00000B00,  # 0B00 - 0B7F     Oriya
        0x00000B80,  # 0B80 - 0BFF     Tamil
        0x00000C00,  # 0C00 - 0C7F     Telugu
        0x00000C80,  # 0C80 - 0CFF     Kannada
        0x00000D00,  # 0D00 - 0D7F     Malayalam
        0x00000D80,  # 0D80 - 0DFF     Sinhala
        0x00000E00,  # 0E00 - 0E7F     Thai
        0x00000E80,  # 0E80 - 0EFF     Lao
        0x00000F00,  # 0F00 - 0FFF     Tibetan
        0x00001000,  # 1000 - 109F     Myanmar
        0x000010A0,  # 10A0 - 10FF     Georgian
        0x00001100,  # 1100 - 11FF     Hangul Jamo
        0x00001200,  # 1200 - 137F     Ethiopic
        0x00001380,  # 1380 - 139F     Ethiopic Supplement
        0x000013A0,  # 13A0 - 13FF     Cherokee
        0x00001400,  # 1400 - 167F     Unified Canadian Aboriginal Syllabics
        0x00001680,  # 1680 - 169F     Ogham
        0x000016A0,  # 16A0 - 16FF     Runic
        0x00001700,  # 1700 - 171F     Tagalog
        0x00001720,  # 1720 - 173F     Hanunoo
        0x00001740,  # 1740 - 175F     Buhid
        0x00001760,  # 1760 - 177F     Tagbanwa
        0x00001780,  # 1780 - 17FF     Khmer
        0x00001800,  # 1800 - 18AF     Mongolian
        0x000018B0,  # 18B0 - 18FF     Unified Canadian Aboriginal Syllabics Extended
        0x00001900,  # 1900 - 194F     Limbu
        0x00001950,  # 1950 - 197F     Tai Le
        0x00001980,  # 1980 - 19DF     New Tai Lue
        0x000019E0,  # 19E0 - 19FF     Khmer Symbols
        0x00001A00,  # 1A00 - 1A1F     Buginese
        0x00001A20,  # 1A20 - 1AAF     Tai Tham
        0x00001AB0,  # 1AB0 - 1AFF     Combining Diacritical Marks Extended
        0x00001B00,  # 1B00 - 1B7F     Balinese
        0x00001B80,  # 1B80 - 1BBF     Sundanese
        0x00001BC0,  # 1BC0 - 1BFF     Batak
        0x00001C00,  # 1C00 - 1C4F     Lepcha
        0x00001C50,  # 1C50 - 1C7F     Ol Chiki
        0x00001C80,  # 1C80 - 1C8F     Cyrillic Extended-C
        0x00001C90,  # 1C90 - 1CBF     Georgian Extended
        0x00001CC0,  # 1CC0 - 1CCF     Sundanese Supplement
        0x00001CD0,  # 1CD0 - 1CFF     Vedic Extensions
        0x00001D00,  # 1D00 - 1D7F     Phonetic Extensions
        0x00001D80,  # 1D80 - 1DBF     Phonetic Extensions Supplement
        0x00001DC0,  # 1DC0 - 1DFF     Combining Diacritical Marks Supplement
        0x00001E00,  # 1E00 - 1EFF     Latin Extended Additional
        0x00001F00,  # 1F00 - 1FFF     Greek Extended
        0x00002000,  # 2000 - 206F     General Punctuation
        0x00002070,  # 2070 - 209F     Superscripts and Subscripts
        0x000020A0,  # 20A0 - 20CF     Currency Symbols
        0x000020D0,  # 20D0 - 20FF     Combining Diacritical Marks for Symbols
        0x00002100,  # 2100 - 214F     Letterlike Symbols
        0x00002150,  # 2150 - 218F     Number Forms
        0x00002190,  # 2190 - 21FF     Arrows
        0x00002200,  # 2200 - 22FF     Mathematical Operators
        0x00002300,  # 2300 - 23FF     Miscellaneous Technical
        0x00002400,  # 2400 - 243F     Control Pictures
        0x00002440,  # 2440 - 245F     Optical Character Recognition
        0x00002460,  # 2460 - 24FF     Enclosed Alphanumerics
        0x00002500,  # 2500 - 257F     Box Drawing
        0x00002580,  # 2580 - 259F     Block Elements
        0x000025A0,  # 25A0 - 25FF     Geometric Shapes
        0x00002600,  # 2600 - 26FF     Miscellaneous Symbols
        0x00002700,  # 2700 - 27BF     Dingbats
        0x000027C0,  # 27C0 - 27EF     Miscellaneous Mathematical Symbols-A
        0x000027F0,  # 27F0 - 27FF     Supplemental Arrows-A
        0x00002800,  # 2800 - 28FF     Braille Patterns
        0x00002900,  # 2900 - 297F     Supplemental Arrows-B
        0x00002980,  # 2980 - 29FF     Miscellaneous Mathematical Symbols-B
        0x00002A00,  # 2A00 - 2AFF     Supplemental Mathematical Operators
        0x00002B00,  # 2B00 - 2BFF     Miscellaneous Symbols and Arrows
        0x00002C00,  # 2C00 - 2C5F     Glagolitic
        0x00002C60,  # 2C60 - 2C7F     Latin Extended-C
        0x00002C80,  # 2C80 - 2CFF     Coptic
        0x00002D00,  # 2D00 - 2D2F     Georgian Supplement
        0x00002D30,  # 2D30 - 2D7F     Tifinagh
        0x00002D80,  # 2D80 - 2DDF     Ethiopic Extended
        0x00002DE0,  # 2DE0 - 2DFF     Cyrillic Extended-A
        0x00002E00,  # 2E00 - 2E7F     Supplemental Punctuation
        0x00002E80,  # 2E80 - 2EFF     CJK Radicals Supplement
        0x00002F00,  # 2F00 - 2FDF     Kangxi Radicals
        0x00002FE0,  # UNASSIGNED
        0x00002FF0,  # 2FF0 - 2FFF     Ideographic Description Characters
        0x00003000,  # 3000 - 303F     CJK Symbols and Punctuation
        0x00003040,  # 3040 - 309F     Hiragana
        0x000030A0,  # 30A0 - 30FF     Katakana
        0x00003100,  # 3100 - 312F     Bopomofo
        0x00003130,  # 3130 - 318F     Hangul Compatibility Jamo
        0x00003190,  # 3190 - 319F     Kanbun
        0x000031A0,  # 31A0 - 31BF     Bopomofo Extended
        0x000031C0,  # 31C0 - 31EF     CJK Strokes
        0x000031F0,  # 31F0 - 31FF     Katakana Phonetic Extensions
        0x00003200,  # 3200 - 32FF     Enclosed CJK Letters and Months
        0x00003300,  # 3300 - 33FF     CJK Compatibility
        0x00003400,  # 3400 - 4DBF     CJK Unified Ideographs Extension A
        0x00004DC0,  # 4DC0 - 4DFF     Yijing Hexagram Symbols
        0x00004E00,  # 4E00 - 9FFF     CJK Unified Ideographs
        0x0000A000,  # A000 - A48F     Yi Syllables
        0x0000A490,  # A490 - A4CF     Yi Radicals
        0x0000A4D0,  # A4D0 - A4FF     Lisu
        0x0000A500,  # A500 - A63F     Vai
        0x0000A640,  # A640 - A69F     Cyrillic Extended-B
        0x0000A6A0,  # A6A0 - A6FF     Bamum
        0x0000A700,  # A700 - A71F     Modifier Tone Letters
        0x0000A720,  # A720 - A7FF     Latin Extended-D
        0x0000A800,  # A800 - A82F     Syloti Nagri
        0x0000A830,  # A830 - A83F     Common Indic Number Forms
        0x0000A840,  # A840 - A87F     Phags-pa
        0x0000A880,  # A880 - A8DF     Saurashtra
        0x0000A8E0,  # A8E0 - A8FF     Devanagari Extended
        0x0000A900,  # A900 - A92F     Kayah Li
        0x0000A930,  # A930 - A95F     Rejang
        0x0000A960,  # A960 - A97F     Hangul Jamo Extended-A
        0x0000A980,  # A980 - A9DF     Javanese
        0x0000A9E0,  # A9E0 - A9FF     Myanmar Extended-B
        0x0000AA00,  # AA00 - AA5F     Cham
        0x0000AA60,  # AA60 - AA7F     Myanmar Extended-A
        0x0000AA80,  # AA80 - AADF     Tai Viet
        0x0000AAE0,  # AAE0 - AAFF     Meetei Mayek Extensions
        0x0000AB00,  # AB00 - AB2F     Ethiopic Extended-A
        0x0000AB30,  # AB30 - AB6F     Latin Extended-E
        0x0000AB70,  # AB70 - ABBF     Cherokee Supplement
        0x0000ABC0,  # ABC0 - ABFF     Meetei Mayek
        0x0000AC00,  # AC00 - D7AF     Hangul Syllables
        0x0000D7B0,  # D7B0 - D7FF     Hangul Jamo Extended-B
        0x0000D800,  # D800 - DB7F     High Surrogates
        0x0000DB80,  # DB80 - DBFF     High Private Use Surrogates
        0x0000DC00,  # DC00 - DFFF     Low Surrogates
        0x0000E000,  # E000 - F8FF     Private Use Area
        0x0000F900,  # F900 - FAFF     CJK Compatibility Ideographs
        0x0000FB00,  # FB00 - FB4F     Alphabetic Presentation Forms
        0x0000FB50,  # FB50 - FDFF     Arabic Presentation Forms-A
        0x0000FE00,  # FE00 - FE0F     Variation Selectors
        0x0000FE10,  # FE10 - FE1F     Vertical Forms
        0x0000FE20,  # FE20 - FE2F     Combining Half Marks
        0x0000FE30,  # FE30 - FE4F     CJK Compatibility Forms
        0x0000FE50,  # FE50 - FE6F     Small Form Variants
        0x0000FE70,  # FE70 - FEFF     Arabic Presentation Forms-B
        0x0000FF00,  # FF00 - FFEF     Halfwidth and Fullwidth Forms
        0x0000FFF0,  # FFF0 - FFFF     Specials
        0x00010000,  # 10000 - 1007F    Linear B Syllabary
        0x00010080,  # 10080 - 100FF    Linear B Ideograms
        0x00010100,  # 10100 - 1013F    Aegean Numbers
        0x00010140,  # 10140 - 1018F    Ancient Greek Numbers
        0x00010190,  # 10190 - 101CF    Ancient Symbols
        0x000101D0,  # 101D0 - 101FF    Phaistos Disc
        0x00010200,  # UNASSIGNED
        0x00010280,  # 10280 - 1029F    Lycian
        0x000102A0,  # 102A0 - 102DF    Carian
        0x000102E0,  # 102E0 - 102FF    Coptic Epact Numbers
        0x00010300,  # 10300 - 1032F    Old Italic
        0x00010330,  # 10330 - 1034F    Gothic
        0x00010350,  # 10350 - 1037F    Old Permic
        0x00010380,  # 10380 - 1039F    Ugaritic
        0x000103A0,  # 103A0 - 103DF    Old Persian
        0x000103E0,  # UNASSIGNED
        0x00010400,  # 10400 - 1044F    Deseret
        0x00010450,  # 10450 - 1047F    Shavian
        0x00010480,  # 10480 - 104AF    Osmanya
        0x000104B0,  # 104B0 - 104FF    Osage
        0x00010500,  # 10500 - 1052F    Elbasan
        0x00010530,  # 10530 - 1056F    Caucasian Albanian
        0x00010570,  # 10570 - 105BF    Vithkuqi
        0x000105C0,  # UNASSIGNED
        0x00010600,  # 10600 - 1077F    Linear A
        0x00010780,  # 10780 - 107BF    Latin Extended-F
        0x000107C0,  # UNASSIGNED
        0x00010800,  # 10800 - 1083F    Cypriot Syllabary
        0x00010840,  # 10840 - 1085F    Imperial Aramaic
        0x00010860,  # 10860 - 1087F    Palmyrene
        0x00010880,  # 10880 - 108AF    Nabataean
        0x000108B0,  # UNASSIGNED
        0x000108E0,  # 108E0 - 108FF    Hatran
        0x00010900,  # 10900 - 1091F    Phoenician
        0x00010920,  # 10920 - 1093F    Lydian
        0x00010940,  # UNASSIGNED
        0x00010980,  # 10980 - 1099F    Meroitic Hieroglyphs
        0x000109A0,  # 109A0 - 109FF    Meroitic Cursive
        0x00010A00,  # 10A00 - 10A5F    Kharoshthi
        0x00010A60,  # 10A60 - 10A7F    Old South Arabian
        0x00010A80,  # 10A80 - 10A9F    Old North Arabian
        0x00010AA0,  # UNASSIGNED
        0x00010AC0,  # 10AC0 - 10AFF    Manichaean
        0x00010B00,  # 10B00 - 10B3F    Avestan
        0x00010B40,  # 10B40 - 10B5F    Inscriptional Parthian
        0x00010B60,  # 10B60 - 10B7F    Inscriptional Pahlavi
        0x00010B80,  # 10B80 - 10BAF    Psalter Pahlavi
        0x00010BB0,  # UNASSIGNED
        0x00010C00,  # 10C00 - 10C4F    Old Turkic
        0x00010C50,  # UNASSIGNED
        0x00010C80,  # 10C80 - 10CFF    Old Hungarian
        0x00010D00,  # 10D00 - 10D3F    Hanifi Rohingya
        0x00010D40,  # UNASSIGNED
        0x00010E60,  # 10E60 - 10E7F    Rumi Numeral Symbols
        0x00010E80,  # 10E80 - 10EBF    Yezidi
        0x00010EC0,  # 10EC0 - 10EFF    Arabic Extended-C
        0x00010F00,  # 10F00 - 10F2F    Old Sogdian
        0x00010F30,  # 10F30 - 10F6F    Sogdian
        0x00010F70,  # 10F70 - 10FAF    Old Uyghur
        0x00010FB0,  # 10FB0 - 10FDF    Chorasmian
        0x00010FE0,  # 10FE0 - 10FFF    Elymaic
        0x00011000,  # 11000 - 1107F    Brahmi
        0x00011080,  # 11080 - 110CF    Kaithi
        0x000110D0,  # 110D0 - 110FF    Sora Sompeng
        0x00011100,  # 11100 - 1114F    Chakma
        0x00011150,  # 11150 - 1117F    Mahajani
        0x00011180,  # 11180 - 111DF    Sharada
        0x000111E0,  # 111E0 - 111FF    Sinhala Archaic Numbers
        0x00011200,  # 11200 - 1124F    Khojki
        0x00011250,  # UNASSIGNED
        0x00011280,  # 11280 - 112AF    Multani
        0x000112B0,  # 112B0 - 112FF    Khudawadi
        0x00011300,  # 11300 - 1137F    Grantha
        0x00011380,  # UNASSIGNED
        0x00011400,  # 11400 - 1147F    Newa
        0x00011480,  # 11480 - 114DF    Tirhuta
        0x000114E0,  # UNASSIGNED
        0x00011580,  # 11580 - 115FF    Siddham
        0x00011600,  # 11600 - 1165F    Modi
        0x00011660,  # 11660 - 1167F    Mongolian Supplement
        0x00011680,  # 11680 - 116CF    Takri
        0x000116D0,  # UNASSIGNED
        0x00011700,  # 11700 - 1174F    Ahom
        0x00011750,  # UNASSIGNED
        0x00011800,  # 11800 - 1184F    Dogra
        0x00011850,  # UNASSIGNED
        0x000118A0,  # 118A0 - 118FF    Warang Citi
        0x00011900,  # 11900 - 1195F    Dives Akuru
        0x00011960,  # UNASSIGNED
        0x000119A0,  # 119A0 - 119FF    Nandinagari
        0x00011A00,  # 11A00 - 11A4F    Zanabazar Square
        0x00011A50,  # 11A50 - 11AAF    Soyombo
        0x00011AB0,  # 11AB0 - 11ABF    Unified Canadian Aboriginal Syllabics Extended-A
        0x00011AC0,  # 11AC0 - 11AFF    Pau Cin Hau
        0x00011B00,  # 11B00 - 11B5F    Devanagari Extended-A
        0x00011B60,  # UNASSIGNED
        0x00011C00,  # 11C00 - 11C6F    Bhaiksuki
        0x00011C70,  # 11C70 - 11CBF    Marchen
        0x00011CC0,  # UNASSIGNED
        0x00011D00,  # 11D00 - 11D5F    Masaram Gondi
        0x00011D60,  # 11D60 - 11DAF    Gunjala Gondi
        0x00011DB0,  # UNASSIGNED
        0x00011EE0,  # 11EE0 - 11EFF    Makasar
        0x00011F00,  # 11F00 - 11F5F    Kawi
        0x00011F60,  # UNASSIGNED
        0x00011FB0,  # 11FB0 - 11FBF    Lisu Supplement
        0x00011FC0,  # 11FC0 - 11FFF    Tamil Supplement
        0x00012000,  # 12000 - 123FF    Cuneiform
        0x00012400,  # 12400 - 1247F    Cuneiform Numbers and Punctuation
        0x00012480,  # 12480 - 1254F    Early Dynastic Cuneiform
        0x00012550,  # UNASSIGNED
        0x00012F90,  # 12F90 - 12FFF    Cypro-Minoan
        0x00013000,  # 13000 - 1342F    Egyptian Hieroglyphs
        0x00013430,  # 13430 - 1345F    Egyptian Hieroglyph Format Controls
        0x00013460,  # UNASSIGNED
        0x00014400,  # 14400 - 1467F    Anatolian Hieroglyphs
        0x00014680,  # UNASSIGNED
        0x00016800,  # 16800 - 16A3F    Bamum Supplement
        0x00016A40,  # 16A40 - 16A6F    Mro
        0x00016A70,  # 16A70 - 16ACF    Tangsa
        0x00016AD0,  # 16AD0 - 16AFF    Bassa Vah
        0x00016B00,  # 16B00 - 16B8F    Pahawh Hmong
        0x00016B90,  # UNASSIGNED
        0x00016E40,  # 16E40 - 16E9F    Medefaidrin
        0x00016EA0,  # UNASSIGNED
        0x00016F00,  # 16F00 - 16F9F    Miao
        0x00016FA0,  # UNASSIGNED
        0x00016FE0,  # 16FE0 - 16FFF    Ideographic Symbols and Punctuation
        0x00017000,  # 17000 - 187FF    Tangut
        0x00018800,  # 18800 - 18AFF    Tangut Components
        0x00018B00,  # 18B00 - 18CFF    Khitan Small Script
        0x00018D00,  # 18D00 - 18D7F    Tangut Supplement
        0x00018D80,  # UNASSIGNED
        0x0001AFF0,  # 1AFF0 - 1AFFF    Kana Extended-B
        0x0001B000,  # 1B000 - 1B0FF    Kana Supplement
        0x0001B100,  # 1B100 - 1B12F    Kana Extended-A
        0x0001B130,  # 1B130 - 1B16F    Small Kana Extension
        0x0001B170,  # 1B170 - 1B2FF    Nushu
        0x0001B300,  # UNASSIGNED
        0x0001BC00,  # 1BC00 - 1BC9F    Duployan
        0x0001BCA0,  # 1BCA0 - 1BCAF    Shorthand Format Controls
        0x0001BCB0,  # UNASSIGNED
        0x0001CF00,  # 1CF00 - 1CFCF    Znamenny Musical Notation
        0x0001CFD0,  # UNASSIGNED
        0x0001D000,  # 1D000 - 1D0FF    Byzantine Musical Symbols
        0x0001D100,  # 1D100 - 1D1FF    Musical Symbols
        0x0001D200,  # 1D200 - 1D24F    Ancient Greek Musical Notation
        0x0001D250,  # UNASSIGNED
        0x0001D2C0,  # 1D2C0 - 1D2DF    Kaktovik Numerals
        0x0001D2E0,  # 1D2E0 - 1D2FF    Mayan Numerals
        0x0001D300,  # 1D300 - 1D35F    Tai Xuan Jing Symbols
        0x0001D360,  # 1D360 - 1D37F    Counting Rod Numerals
        0x0001D380,  # UNASSIGNED
        0x0001D400,  # 1D400 - 1D7FF    Mathematical Alphanumeric Symbols
        0x0001D800,  # 1D800 - 1DAAF    Sutton SignWriting
        0x0001DAB0,  # UNASSIGNED
        0x0001DF00,  # 1DF00 - 1DFFF    Latin Extended-G
        0x0001E000,  # 1E000 - 1E02F    Glagolitic Supplement
        0x0001E030,  # 1E030 - 1E08F    Cyrillic Extended-D
        0x0001E090,  # UNASSIGNED
        0x0001E100,  # 1E100 - 1E14F    Nyiakeng Puachue Hmong
        0x0001E150,  # UNASSIGNED
        0x0001E290,  # 1E290 - 1E2BF    Toto
        0x0001E2C0,  # 1E2C0 - 1E2FF    Wancho
        0x0001E300,  # UNASSIGNED
        0x0001E4D0,  # 1E4D0 - 1E4FF    Nag Mundari
        0x0001E500,  # UNASSIGNED
        0x0001E7E0,  # 1E7E0 - 1E7FF    Ethiopic Extended-B
        0x0001E800,  # 1E800 - 1E8DF    Mende Kikakui
        0x0001E8E0,  # UNASSIGNED
        0x0001E900,  # 1E900 - 1E95F    Adlam
        0x0001E960,  # UNASSIGNED
        0x0001EC70,  # 1EC70 - 1ECBF    Indic Siyaq Numbers
        0x0001ECC0,  # UNASSIGNED
        0x0001ED00,  # 1ED00 - 1ED4F    Ottoman Siyaq Numbers
        0x0001ED50,  # UNASSIGNED
        0x0001EE00,  # 1EE00 - 1EEFF    Arabic Mathematical Alphabetic Symbols
        0x0001EF00,  # UNASSIGNED
        0x0001F000,  # 1F000 - 1F02F    Mahjong Tiles
        0x0001F030,  # 1F030 - 1F09F    Domino Tiles
        0x0001F0A0,  # 1F0A0 - 1F0FF    Playing Cards
        0x0001F100,  # 1F100 - 1F1FF    Enclosed Alphanumeric Supplement
        0x0001F200,  # 1F200 - 1F2FF    Enclosed Ideographic Supplement
        0x0001F300,  # 1F300 - 1F5FF    Miscellaneous Symbols and Pictographs
        0x0001F600,  # 1F600 - 1F64F    Emoticons
        0x0001F650,  # 1F650 - 1F67F    Ornamental Dingbats
        0x0001F680,  # 1F680 - 1F6FF    Transport and Map Symbols
        0x0001F700,  # 1F700 - 1F77F    Alchemical Symbols
        0x0001F780,  # 1F780 - 1F7FF    Geometric Shapes Extended
        0x0001F800,  # 1F800 - 1F8FF    Supplemental Arrows-C
        0x0001F900,  # 1F900 - 1F9FF    Supplemental Symbols and Pictographs
        0x0001FA00,  # 1FA00 - 1FA6F    Chess Symbols
        0x0001FA70,  # 1FA70 - 1FAFF    Symbols and Pictographs Extended-A
        0x0001FB00,  # 1FB00 - 1FBFF    Symbols for Legacy Computing
        0x0001FC00,  # UNASSIGNED
        0x00020000,  # 20000 - 2A6DF    CJK Unified Ideographs Extension B
        0x0002A6E0,  # UNASSIGNED
        0x0002A700,  # 2A700 - 2B73F    CJK Unified Ideographs Extension C
        0x0002B740,  # 2B740 - 2B81F    CJK Unified Ideographs Extension D
        0x0002B820,  # 2B820 - 2CEAF    CJK Unified Ideographs Extension E
        0x0002CEB0,  # 2CEB0 - 2EBEF    CJK Unified Ideographs Extension F
        0x0002EBF0,  # UNASSIGNED
        0x0002F800,  # 2F800 - 2FA1F    CJK Compatibility Ideographs Supplement
        0x0002FA20,  # UNASSIGNED
        0x00030000,  # 30000 - 3134F    CJK Unified Ideographs Extension G
        0x00031350,  # 31350 - 323AF    CJK Unified Ideographs Extension H
        0x000323B0,  # UNASSIGNED
        0x000E0000,  # E0000 - E007F    Tags
        0x000E0080,  # UNASSIGNED
        0x000E0100,  # E0100 - E01EF    Variation Selectors Supplement
        0x000E01F0,  # UNASSIGNED
        0x000F0000,  # F0000 - FFFFF    Supplementary Private Use Area-A
        0x00100000   # 100000 - 10FFFF Supplementary Private Use Area-B
    ]

    #
    BAD_CODEPOINT = 0x0000FFFD
    ERRONEOUS_CODEPOINT = 0xFFFFFFFF

    # http://www.unicode.org/glossary/#high_surrogate_code_unit
    HIGH_SURROGATE_MIN = 0x0000D800
    HIGH_SURROGATE_MAX = 0x0000DBFF

    # http://www.unicode.org/glossary/#low_surrogate_code_unit
    LOW_SURROGATE_MIN = 0x0000DC00
    LOW_SURROGATE_MAX = 0x0000DFFF

    # http://www.unicode.org/glossary/#supplementary_code_point
    SUPPLEMENTARY_CODE_POINT_MIN = 0x00010000
    SUPPLEMENTARY_CODE_POINT_MAX = 0x0010FFFF

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def equal(lhs, rhs, case_insensitive=False, normalization_form='NFKC'):
        """
        """
        assert lhs is not None, 'Invalid LHS.'
        assert rhs is not None, 'Invalid RHS.'
        nfc = functools.partial(unicodedata.normalize, normalization_form)
        if case_insensitive:
            return nfc(lhs).casefold() == nfc(rhs).casefold()
        else:
            return nfc(lhs) == nfc(rhs)

    @staticmethod
    def compare(lhs, rhs, case_insensitive=False, normalization_form='NFKC'):
        """
        """
        assert lhs is not None, 'Invalid LHS.'
        assert rhs is not None, 'Invalid RHS.'
        nfc = functools.partial(unicodedata.normalize, normalization_form)
        if case_insensitive:
            lhs, rhs = nfc(lhs).casefold(), nfc(rhs).casefold()
        result = 0
        if nfc(lhs) < nfc(rhs):
            result = -1
        elif nfc(lhs) > nfc(rhs):
            result = 1
        return result

    class PyUnicodeObject(ctypes.Structure):
        """
        """
        PyUnicode_WCHAR_KIND = 0
        PyUnicode_1BYTE_KIND = 1
        PyUnicode_2BYTE_KIND = 2
        PyUnicode_4BYTE_KIND = 4
        _fields_ = (('kind', ctypes.c_uint, 3), )

    @staticmethod
    def get_string_kind(text):
        """
        """
        return Text.PyUnicodeObject.from_address(id(text)).kind

    @staticmethod
    def list_category(category, filepath=r"D:\Tmp\UnicodeData.txt"):
        """
        """
        with open(filepath) as stream:
            baskets = []
            index = -1
            curr_num = -1
            for _, line in enumerate(stream):
                num, _, cat, _ = line.split(';', 3)
                if cat == category:
                    num = int(num, 16)
                    if num - curr_num != 1:
                        baskets.append([])
                        index += 1
                    baskets[index].append(num)
                    curr_num = num
            result = baskets
        return result

    @staticmethod
    def collect_by_category(category):
        """
        """
        # collect_by_category('Cf')
        print(f"Listing  {category}  category  - .")
        ranges = Text.list_category(category)
        # print(ranges)
        result = "    return\n"
        for r in ranges:
            def convert(num):
                res = "{0:#0{1}x}".format(num, 6)
                res = list(res)
                prefix = res[0:2]
                suffix = res[2:]
                suffix = [ch.upper() for ch in suffix]
                res = ''.join(prefix) + ''.join(suffix)
                return res
            start = convert(r[0])
            end = convert(r[len(r)-1])
            # print("{}, {}".format(start, end))
            result += "           in_range(codepoint, {}, {}) ||\n".format(start, end)
        result += ";"
        print(result)

    @staticmethod
    def concatenate_strings_with_sentinels(strings):
        """
        """
        result = ""
        for k, text in enumerate(strings):
            result += text + chr(k)
        return result

    @staticmethod
    def generate_random_string(length):
        """
        """
        data = string.printable
        return ''.join(random.choice(data) for i in range(length))

    @staticmethod
    def find_all_substrings(text, pattern):
        """
        """
        result = list()
        index = 0
        while True:
            index = text.find(pattern, index)
            if index < 0:
                break
            result.append(index)
            index += len(pattern)
        return result

    @staticmethod
    def convert_to_character(codepoint):
        """
        """
        return chr(codepoint)

    @staticmethod
    def assemble_codepoint_le(b0, b1, b2, b3):
        """
        """
        v  = (b0 << 0)  & 0x000000FF  # noqa
        v |= (b1 << 8)  & 0x0000FF00  # noqa
        v |= (b2 << 16) & 0x00FF0000  # noqa
        v |= (b3 << 24) & 0xFF000000  # noqa
        return v

    @staticmethod
    def assemble_codepoint_be(b0, b1, b2, b3):
        """
        """
        v  = (b0 << 24) & 0xFF000000  # noqa
        v |= (b1 << 16) & 0x00FF0000  # noqa
        v |= (b2 << 8)  & 0x0000FF00  # noqa
        v |= (b3 << 0)  & 0x000000FF  # noqa
        return v

    @staticmethod
    def string_to_codepoints(text):
        """
        """
        suffix = 'le' if sys.byteorder == "little" else 'be'
        data = text.encode(f'UTF-32{suffix}')
        assert len(data) % 4 == 0, "Invalid unicode data"
        assembler = Text.assemble_codepoint_le if suffix == 'le' else Text.assemble_codepoint_be
        codepoints = [0] * (len(data) // 4)
        i = 0
        for k in range(0, len(data), 4):
            codepoints[i] = assembler(data[k + 0],
                                      data[k + 1],
                                      data[k + 2],
                                      data[k + 3])
            i += 1
        return codepoints

    @staticmethod
    def make_codepoint(high_surrogate_code_unit, low_surrogate_code_unit):
        """
        https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-encoding-introduction
        """
        return (Text.SUPPLEMENTARY_CODE_POINT_MIN +
                ((high_surrogate_code_unit - Text.HIGH_SURROGATE_MIN) * 0x00000400 +
                 (low_surrogate_code_unit - Text.LOW_SURROGATE_MIN)))

    @staticmethod
    def high_surrogate(code_unit):
        """
        """
        return Text.HIGH_SURROGATE_MIN <= code_unit <= Text.HIGH_SURROGATE_MAX

    @staticmethod
    def low_surrogate(code_unit):
        """
        """
        return Text.LOW_SURROGATE_MIN <= code_unit <= Text.LOW_SURROGATE_MAX

    @staticmethod
    def non_character(codepoint):
        """
        """
        return ((codepoint & 0x0000FFFE) == 0x0000FFFE or
                (0x0000FDD0 <= codepoint <= 0x0000FDEF))

    @staticmethod
    def valid_codepoint(codepoint):
        """
        """
        return Text.MIN_CODE_POINT <= codepoint <= Text.MAX_CODE_POINT

    @staticmethod
    def letter(codepoint):
        """
        """
        result = ((0x00000041 <= codepoint <= 0x0000005A) or
                  (0x00000061 <= codepoint <= 0x0000007A))
        if not result:
            ch = Text.convert_to_character(codepoint)
            category = unicodedata.category(ch)
            match category:
                case 'Lu' | 'Ll' | 'Lt' | 'Lm' | 'Lo':
                    result = True
                case _:
                    result = False
        return result

    @staticmethod
    def letter_number(codepoint):
        """
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'Nl'

    @staticmethod
    def other_symbol(codepoint):
        """
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'So'

    @staticmethod
    def binary_digit(codepoint):
        """
        Only considering ASCII table and 0xFF10 - 0xFF11
        when use octal numbers during lexical analyze.
        """
        result = ((0x00000030 <= codepoint <= 0x00000031) or
                  (0x0000FF10 <= codepoint <= 0x0000FF11))
        return result

    @staticmethod
    def ascii_binary_digit(codepoint):
        """
        Only considering ASCII table.
        """
        return 0x00000030 <= codepoint <= 0x00000031

    @staticmethod
    def octal_digit(codepoint):
        """
        Only considering ASCII table and 0xFF10 - 0xFF17
        when use octal numbers during lexical analyze.
        """
        result = ((0x00000030 <= codepoint <= 0x00000037) or
                  (0x0000FF10 <= codepoint <= 0x0000FF17))
        return result

    @staticmethod
    def ascii_octal_digit(codepoint):
        """
        Only considering ASCII table.
        """
        return 0x00000030 <= codepoint <= 0x00000037

    @staticmethod
    def decimal_digit(codepoint):
        """
        """
        result = ((0x00000030 <= codepoint <= 0x00000039) or
                  (0x0000FF10 <= codepoint <= 0x0000FF19))
        if not result:
            ch = Text.convert_to_character(codepoint)
            result = unicodedata.category(ch) == 'Nd'
        return result

    @staticmethod
    def ascii_decimal_digit(codepoint):
        """
        Only considering ASCII table.
        """
        return 0x00000030 <= codepoint <= 0x00000039

    @staticmethod
    def hexadecimal_digit(codepoint):
        """
        """
        result = ((0x00000030 <= codepoint <= 0x00000039) or
                  (0x00000041 <= codepoint <= 0x00000046) or
                  (0x00000061 <= codepoint <= 0x00000066) or
                  (0x0000FF10 <= codepoint <= 0x0000FF19) or
                  (0x0000FF21 <= codepoint <= 0x0000FF26) or
                  (0x0000FF41 <= codepoint <= 0x0000FF46))
        if not result:
            ch = Text.convert_to_character(codepoint)
            result = unicodedata.category(ch) == 'Nd'
        return result

    @staticmethod
    def ascii_hexadecimal_digit(codepoint):
        """
        """
        return ((0x00000030 <= codepoint <= 0x00000039) or
                (0x00000041 <= codepoint <= 0x00000046) or
                (0x00000061 <= codepoint <= 0x00000066))

    @staticmethod
    def zero_digit(codepoint):
        """
        """
        return 0x00000030 == codepoint or codepoint == 0x0000FF10

    @staticmethod
    def ascii_zero_digit(codepoint):
        """
        """
        return 0x00000030 == codepoint

    ASCII_NUMBERS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
                     0, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0]

    @staticmethod
    def ascii_digit(digit):
        """
        """
        return Text.ASCII_NUMBERS[digit]

    @staticmethod
    def ascii(codepoint):
        """
        """
        return codepoint <= 0x0000007F

    @staticmethod
    def spacing_mark(codepoint):
        """
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'Mc'

    @staticmethod
    def non_spacing_mark(codepoint):
        """
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'Mn'

    @staticmethod
    def whitespace(codepoint):
        """
        """
        match codepoint:
            case (0x00000020 |  # ' '
                  0x00000009 |  # '\t'
                  0x0000000B |  # '\v'
                  0x0000000C |  # '\f'
                  0x000000A0 |  # NO-BREAK SPACE
                  0x0000FEFF |  # ZERO WIDTH NO-BREAK SPACE
                  0x0000001A):  # Substitute, SUB
                return True
            case _:
                ch = Text.convert_to_character(codepoint)
                return unicodedata.category(ch) == 'Zs'

    @staticmethod
    def eol(codepoint):
        """
        """
        return (codepoint == 0x0000000A or  # '\n' Line feed character
                codepoint == 0x0000000D or  # '\r' Carriage return character
                codepoint == 0x00000085 or  # Next line character
                codepoint == 0x00002028 or  # Line separator character
                codepoint == 0x00002029)    # Paragraph separator character

    @staticmethod
    def eos(codepoint):
        """
        End Of Transmission
        """
        return codepoint == 0x00000004 or codepoint == 0x00002404

    @staticmethod
    def eos_codepoint():
        """
        Return End Of Transmission (EOT) codepoint.
        """
        return 0x00002404

    @staticmethod
    def underscore(codepoint):
        """
        Low Line (Underscore) _
        """
        match codepoint:
            case '_':
                return True
            case _:
                ch = Text.convert_to_character(codepoint)
                return unicodedata.category(ch) == 'Pc'

    @staticmethod
    def connector_punctuation(codepoint):
        """
        Connector Punctuation
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'Pc'

    @staticmethod
    def dollar_sign(codepoint):
        """
        Dollar Sign $
        """
        return (codepoint == 0x00000024 or  # '$'
                codepoint == 0x0000FF04 or  # '＄'
                codepoint == 0x0000FE69)    # '﹩'

    @staticmethod
    def currency_sign(codepoint):
        """
        Currency Sign
        """
        ch = Text.convert_to_character(codepoint)
        return unicodedata.category(ch) == 'Sc'

    @staticmethod
    def left_parenthesis(codepoint):
        """
        Left Parenthesis (
        """
        return (codepoint == 0x00000028 or  # '('
                codepoint == 0x0000FF08 or  # '（'
                codepoint == 0x0000FE59 or  # '﹙'
                codepoint == 0x0000208D or  # '₍'
                codepoint == 0x0000207D or  # '⁽'
                codepoint == 0x0000FE35)    # '︵'

    @staticmethod
    def right_parenthesis(codepoint):
        """
        Right Parenthesis )
        """
        return (codepoint == 0x00000029 or  # ')'
                codepoint == 0x0000FF09 or  # '）'
                codepoint == 0x0000FE5A or  # '﹚'
                codepoint == 0x0000208E or  # '₎'
                codepoint == 0x0000207E or  # '⁾'
                codepoint == 0x0000FE36)    # '︶'

    @staticmethod
    def left_square_bracket(codepoint):
        """
        Left Square Bracket [
        """
        return (codepoint == 0x0000005B or  # '['
                codepoint == 0x0000FF3B or  # '［'
                codepoint == 0x0000FE47)    # '﹇'

    @staticmethod
    def right_square_bracket(codepoint):
        """
        Right Square Bracket ]
        """
        return (codepoint == 0x0000005D or  # ']'
                codepoint == 0x0000FF3D or  # '］'
                codepoint == 0x0000FE48)    # '﹈'

    @staticmethod
    def left_curly_bracket(codepoint):
        """
        Left Curly Bracket {
        """
        return (codepoint == 0x0000007B or  # '{'
                codepoint == 0x0000FF5B or  # '｛'
                codepoint == 0x0000FE5B or  # '﹛'
                codepoint == 0x0000FE37)    # '︷'

    @staticmethod
    def right_curly_bracket(codepoint):
        """
        Right Curly Bracket }
        """
        return (codepoint == 0x0000007D or  # '}'
                codepoint == 0x0000FF5D or  # '｝'
                codepoint == 0x0000FE5C or  # '﹜'
                codepoint == 0x0000FE38)    # '︸'

    @staticmethod
    def plus_sign(codepoint):
        """
        Plus Sign +
        """
        return (codepoint == 0x0000002B or  # '+'
                codepoint == 0x0000FF0B or  # '＋'
                codepoint == 0x0000FE62 or  # '﹢'
                codepoint == 0x0000FB29 or  # '﬩'
                codepoint == 0x0000208A or  # '₊'
                codepoint == 0x0000207A)    # '⁺'

    @staticmethod
    def hyphen_minus(codepoint):
        """
        Hyphen-Minus -
        """
        return (codepoint == 0x0000002D or  # '-'
                codepoint == 0x0000FF0D or  # '－'
                codepoint == 0x0000FE63)    # '﹣'

    @staticmethod
    def asterisk(codepoint):
        """
        Asterisk (Mul) *
        """
        return (codepoint == 0x0000002A or  # '*'
                codepoint == 0x0000FF0A or  # '＊'
                codepoint == 0x0000FE61)    # '﹡'

    @staticmethod
    def forward_slash(codepoint):
        """
        Solidus (Div) (Forward slash) /
        """
        return (codepoint == 0x0000002F or  # '/'
                codepoint == 0x0000FF0F)    # '／'

    @staticmethod
    def back_slash(codepoint):
        """
        Reverse Solidus (Back slash) \
        """
        return (codepoint == 0x0000005C or  # '\\'
                codepoint == 0x0000FF3C or  # '＼'
                codepoint == 0x0000FE68)    # '﹨'

    @staticmethod
    def equals_sign(codepoint):
        """
        Equals Sign =
        """
        return (codepoint == 0x0000003D or  # '='
                codepoint == 0x0000FF1D or  # '＝'
                codepoint == 0x0000FE66 or  # '﹦'
                codepoint == 0x0000208C or  # '₌'
                codepoint == 0x0000207C)    # '⁼'

    @staticmethod
    def less_than_sign(codepoint):
        """
        Less-Than Sign <
        """
        return (codepoint == 0x0000003C or  # '<'
                codepoint == 0x0000FF1C or  # '＜'
                codepoint == 0x0000FE64)    # '﹤'

    @staticmethod
    def greater_than_sign(codepoint):
        """
        Greater-Than Sign >
        """
        return (codepoint == 0x0000003E or  # '>'
                codepoint == 0x0000FF1E or  # '＞'
                codepoint == 0x0000FE65)    # '﹥'

    @staticmethod
    def dot(codepoint):
        """
        Full Stop (Dot) .
        """
        return (codepoint == 0x0000002E or  # '.'
                codepoint == 0x0000FF0E or  # '．'
                codepoint == 0x0000FE52)    # '﹒'

    @staticmethod
    def colon(codepoint):
        """
        Colon :
        """
        return (codepoint == 0x0000003A or  # ':'
                codepoint == 0x0000FF1A or  # '：'
                codepoint == 0x0000FE55 or  # '﹕'
                codepoint == 0x0000FE13)    # '︓'

    @staticmethod
    def comma(codepoint):
        """
        Comma ,
        """
        return (codepoint == 0x0000002C or  # ','
                codepoint == 0x0000FF0C or  # '，'
                codepoint == 0x0000FE50 or  # '﹐'
                codepoint == 0x0000FE10)    # '︐'

    @staticmethod
    def semicolon(codepoint):
        """
        Semicolon ;
        """
        return (codepoint == 0x0000003B or  # ';'
                codepoint == 0x0000FF1B or  # '；'
                codepoint == 0x0000FE54 or  # '﹔'
                codepoint == 0x0000FE14)    # '︔'

    @staticmethod
    def vertical_line(codepoint):
        """
        Vertical Line (Bar) |
        """
        return (codepoint == 0x0000007C or  # '|'
                codepoint == 0x0000FF5C)    # '｜'

    @staticmethod
    def grave_accent(codepoint):
        """
        Grave Accent `
        """
        return (codepoint == 0x00000060 or  # '`'
                codepoint == 0x0000FF40)    # '｀'

    @staticmethod
    def tilde(codepoint):
        """
        Tilde ~
        """
        return (codepoint == 0x0000007E or  # '~'
                codepoint == 0x0000FF5E)    # '～'

    @staticmethod
    def exclamation_mark(codepoint):
        """
        Exclamation Mark !
        """
        return (codepoint == 0x00000021 or  # '!'
                codepoint == 0x0000FF01 or  # '！'
                codepoint == 0x0000FE15 or  # '︕'
                codepoint == 0x0000FE57)    # '﹗'

    @staticmethod
    def question_mark(codepoint):
        """
        Question Mark ?
        """
        return (codepoint == 0x0000003F or  # '?'
                codepoint == 0x0000FF1F or  # '？'
                codepoint == 0x0000FE16 or  # '︖'
                codepoint == 0x0000FE56)    # '﹖'

    @staticmethod
    def apostrophe(codepoint):
        """
        Single Quotation Mark (Apostrophe) '
        """
        return (codepoint == 0x00000027 or  # '\''
                codepoint == 0x0000FF07)    # '＇'

    @staticmethod
    def quotation_mark(codepoint):
        """
        Double Quotation Mark "
        """
        return (codepoint == 0x00000022 or  # '"'
                codepoint == 0x0000FF02)    # '＂'

    @staticmethod
    def commercial_at(codepoint):
        """
        Commercial At @
        """
        return (codepoint == 0x00000040 or  # '@'
                codepoint == 0x0000FF20 or  # '＠'
                codepoint == 0x0000FE6B)    # '﹫'

    @staticmethod
    def number_sign(codepoint):
        """
        Number Sign #
        """
        return (codepoint == 0x00000023 or  # '#'
                codepoint == 0x0000FF03 or  # '＃'
                codepoint == 0x0000FE5F)    # '﹟'

    @staticmethod
    def percent_sign(codepoint):
        """
        Percent Sign %
        """
        return (codepoint == 0x00000025 or  # '%'
                codepoint == 0x0000FF05 or  # '％'
                codepoint == 0x0000FE6A)    # '﹪'

    @staticmethod
    def circumflex_accent(codepoint):
        """
        Circumflex Accent (Xor) ^
        """
        return (codepoint == 0x0000005E or  # '^'
                codepoint == 0x0000FF3E)    # '＾'

    @staticmethod
    def ampersand(codepoint):
        """
        Ampersand &.
        """
        return (codepoint == 0x00000026 or  # '&'
                codepoint == 0x0000FF06 or  # '＆'
                codepoint == 0x0000FE60)    # '﹠'

    @staticmethod
    def epsilon(ch):
        """
        """
        return (ch == 'ε' or  # 0x000003B5
                ch == 'λ')    # 0x000003BB

    @staticmethod
    def emoji(codepoint):
        """
        """
        return (0x0000231A <= codepoint <= 0x0000231B or
                0x000023E9 <= codepoint <= 0x000023EC or
                codepoint == 0x000023F0 or
                codepoint == 0x000023F3 or
                0x000025FD <= codepoint <= 0x000025FE or
                0x00002614 <= codepoint <= 0x00002615 or
                0x00002648 <= codepoint <= 0x00002653 or
                codepoint == 0x0000267F or
                codepoint == 0x00002693 or
                codepoint == 0x000026A1 or
                0x000026AA <= codepoint <= 0x000026AB or
                0x000026BD <= codepoint <= 0x000026BE or
                0x000026C4 <= codepoint <= 0x000026C5 or
                codepoint == 0x000026CE or
                codepoint == 0x000026D4 or
                codepoint == 0x000026EA or
                0x000026F2 <= codepoint <= 0x000026F3 or
                codepoint == 0x000026F5 or
                codepoint == 0x000026FA or
                codepoint == 0x000026FD or
                codepoint == 0x00002705 or
                0x0000270A <= codepoint <= 0x0000270B or
                codepoint == 0x00002728 or
                codepoint == 0x0000274C or
                codepoint == 0x0000274E or
                0x00002753 <= codepoint <= 0x00002755 or
                codepoint == 0x00002757 or
                0x00002795 <= codepoint <= 0x00002797 or
                codepoint == 0x000027B0 or
                codepoint == 0x000027BF or
                0x00002B1B <= codepoint <= 0x00002B1C or
                codepoint == 0x00002B50 or
                codepoint == 0x00002B55 or
                codepoint == 0x0001F004 or
                codepoint == 0x0001F0CF or
                codepoint == 0x0001F18E or
                0x0001F191 <= codepoint <= 0x0001F19A or
                codepoint == 0x0001F201 or
                codepoint == 0x0001F21A or
                codepoint == 0x0001F22F or
                0x0001F232 <= codepoint <= 0x0001F236 or
                0x0001F238 <= codepoint <= 0x0001F23A or
                0x0001F250 <= codepoint <= 0x0001F251 or
                0x0001F300 <= codepoint <= 0x0001F30C or
                0x0001F30D <= codepoint <= 0x0001F30E or
                codepoint == 0x0001F30F or
                codepoint == 0x0001F310 or
                codepoint == 0x0001F311 or
                codepoint == 0x0001F312 or
                0x0001F313 <= codepoint <= 0x0001F315 or
                0x0001F316 <= codepoint <= 0x0001F318 or
                codepoint == 0x0001F319 or
                codepoint == 0x0001F31A or
                codepoint == 0x0001F31B or
                codepoint == 0x0001F31C or
                0x0001F31D <= codepoint <= 0x0001F31E or
                0x0001F31F <= codepoint <= 0x0001F320 or
                0x0001F32D <= codepoint <= 0x0001F32F or
                0x0001F330 <= codepoint <= 0x0001F331 or
                0x0001F332 <= codepoint <= 0x0001F333 or
                0x0001F334 <= codepoint <= 0x0001F335 or
                0x0001F337 <= codepoint <= 0x0001F34A or
                codepoint == 0x0001F34B or
                0x0001F34C <= codepoint <= 0x0001F34F or
                codepoint == 0x0001F350 or
                0x0001F351 <= codepoint <= 0x0001F37B or
                codepoint == 0x0001F37C or
                0x0001F37E <= codepoint <= 0x0001F37F or
                0x0001F380 <= codepoint <= 0x0001F393 or
                0x0001F3A0 <= codepoint <= 0x0001F3C4 or
                codepoint == 0x0001F3C5 or
                codepoint == 0x0001F3C6 or
                codepoint == 0x0001F3C7 or
                codepoint == 0x0001F3C8 or
                codepoint == 0x0001F3C9 or
                codepoint == 0x0001F3CA or
                0x0001F3CF <= codepoint <= 0x0001F3D3 or
                0x0001F3E0 <= codepoint <= 0x0001F3E3 or
                codepoint == 0x0001F3E4 or
                0x0001F3E5 <= codepoint <= 0x0001F3F0 or
                codepoint == 0x0001F3F4 or
                0x0001F3F8 <= codepoint <= 0x0001F407 or
                codepoint == 0x0001F408 or
                0x0001F409 <= codepoint <= 0x0001F40B or
                0x0001F40C <= codepoint <= 0x0001F40E or
                0x0001F40F <= codepoint <= 0x0001F410 or
                0x0001F411 <= codepoint <= 0x0001F412 or
                codepoint == 0x0001F413 or
                codepoint == 0x0001F414 or
                codepoint == 0x0001F415 or
                codepoint == 0x0001F416 or
                0x0001F417 <= codepoint <= 0x0001F429 or
                codepoint == 0x0001F42A or
                0x0001F42B <= codepoint <= 0x0001F43E or
                codepoint == 0x0001F440 or
                0x0001F442 <= codepoint <= 0x0001F464 or
                codepoint == 0x0001F465 or
                0x0001F466 <= codepoint <= 0x0001F46B or
                0x0001F46C <= codepoint <= 0x0001F46D or
                0x0001F46E <= codepoint <= 0x0001F4AC or
                codepoint == 0x0001F4AD or
                0x0001F4AE <= codepoint <= 0x0001F4B5 or
                0x0001F4B6 <= codepoint <= 0x0001F4B7 or
                0x0001F4B8 <= codepoint <= 0x0001F4EB or
                0x0001F4EC <= codepoint <= 0x0001F4ED or
                codepoint == 0x0001F4EE or
                codepoint == 0x0001F4EF or
                0x0001F4F0 <= codepoint <= 0x0001F4F4 or
                codepoint == 0x0001F4F5 or
                0x0001F4F6 <= codepoint <= 0x0001F4F7 or
                codepoint == 0x0001F4F8 or
                0x0001F4F9 <= codepoint <= 0x0001F4FC or
                0x0001F4FF <= codepoint <= 0x0001F502 or
                codepoint == 0x0001F503 or
                0x0001F504 <= codepoint <= 0x0001F507 or
                codepoint == 0x0001F508 or
                codepoint == 0x0001F509 or
                0x0001F50A <= codepoint <= 0x0001F514 or
                codepoint == 0x0001F515 or
                0x0001F516 <= codepoint <= 0x0001F52B or
                0x0001F52C <= codepoint <= 0x0001F52D or
                0x0001F52E <= codepoint <= 0x0001F53D or
                0x0001F54B <= codepoint <= 0x0001F54E or
                0x0001F550 <= codepoint <= 0x0001F55B or
                0x0001F55C <= codepoint <= 0x0001F567 or
                codepoint == 0x0001F57A or
                0x0001F595 <= codepoint <= 0x0001F596 or
                codepoint == 0x0001F5A4 or
                0x0001F5FB <= codepoint <= 0x0001F5FF or
                codepoint == 0x0001F600 or
                0x0001F601 <= codepoint <= 0x0001F606 or
                0x0001F607 <= codepoint <= 0x0001F608 or
                0x0001F609 <= codepoint <= 0x0001F60D or
                codepoint == 0x0001F60E or
                codepoint == 0x0001F60F or
                codepoint == 0x0001F610 or
                codepoint == 0x0001F611 or
                0x0001F612 <= codepoint <= 0x0001F614 or
                codepoint == 0x0001F615 or
                codepoint == 0x0001F616 or
                codepoint == 0x0001F617 or
                codepoint == 0x0001F618 or
                codepoint == 0x0001F619 or
                codepoint == 0x0001F61A or
                codepoint == 0x0001F61B or
                0x0001F61C <= codepoint <= 0x0001F61E or
                codepoint == 0x0001F61F or
                0x0001F620 <= codepoint <= 0x0001F625 or
                0x0001F626 <= codepoint <= 0x0001F627 or
                0x0001F628 <= codepoint <= 0x0001F62B or
                codepoint == 0x0001F62C or
                codepoint == 0x0001F62D or
                0x0001F62E <= codepoint <= 0x0001F62F or
                0x0001F630 <= codepoint <= 0x0001F633 or
                codepoint == 0x0001F634 or
                codepoint == 0x0001F635 or
                codepoint == 0x0001F636 or
                0x0001F637 <= codepoint <= 0x0001F640 or
                0x0001F641 <= codepoint <= 0x0001F644 or
                0x0001F645 <= codepoint <= 0x0001F64F or
                codepoint == 0x0001F680 or
                0x0001F681 <= codepoint <= 0x0001F682 or
                0x0001F683 <= codepoint <= 0x0001F685 or
                codepoint == 0x0001F686 or
                codepoint == 0x0001F687 or
                codepoint == 0x0001F688 or
                codepoint == 0x0001F689 or
                0x0001F68A <= codepoint <= 0x0001F68B or
                codepoint == 0x0001F68C or
                codepoint == 0x0001F68D or
                codepoint == 0x0001F68E or
                codepoint == 0x0001F68F or
                codepoint == 0x0001F690 or
                0x0001F691 <= codepoint <= 0x0001F693 or
                codepoint == 0x0001F694 or
                codepoint == 0x0001F695 or
                codepoint == 0x0001F696 or
                codepoint == 0x0001F697 or
                codepoint == 0x0001F698 or
                0x0001F699 <= codepoint <= 0x0001F69A or
                0x0001F69B <= codepoint <= 0x0001F6A1 or
                codepoint == 0x0001F6A2 or
                codepoint == 0x0001F6A3 or
                0x0001F6A4 <= codepoint <= 0x0001F6A5 or
                codepoint == 0x0001F6A6 or
                0x0001F6A7 <= codepoint <= 0x0001F6AD or
                0x0001F6AE <= codepoint <= 0x0001F6B1 or
                codepoint == 0x0001F6B2 or
                0x0001F6B3 <= codepoint <= 0x0001F6B5 or
                codepoint == 0x0001F6B6 or
                0x0001F6B7 <= codepoint <= 0x0001F6B8 or
                0x0001F6B9 <= codepoint <= 0x0001F6BE or
                codepoint == 0x0001F6BF or
                codepoint == 0x0001F6C0 or
                0x0001F6C1 <= codepoint <= 0x0001F6C5 or
                codepoint == 0x0001F6CC or
                codepoint == 0x0001F6D0 or
                0x0001F6D1 <= codepoint <= 0x0001F6D2 or
                codepoint == 0x0001F6D5 or
                0x0001F6D6 <= codepoint <= 0x0001F6D7 or
                codepoint == 0x0001F6DC or
                0x0001F6DD <= codepoint <= 0x0001F6DF or
                0x0001F6EB <= codepoint <= 0x0001F6EC or
                0x0001F6F4 <= codepoint <= 0x0001F6F6 or
                0x0001F6F7 <= codepoint <= 0x0001F6F8 or
                codepoint == 0x0001F6F9 or
                codepoint == 0x0001F6FA or
                0x0001F6FB <= codepoint <= 0x0001F6FC or
                0x0001F7E0 <= codepoint <= 0x0001F7EB or
                codepoint == 0x0001F7F0 or
                codepoint == 0x0001F90C or
                0x0001F90D <= codepoint <= 0x0001F90F or
                0x0001F910 <= codepoint <= 0x0001F918 or
                0x0001F919 <= codepoint <= 0x0001F91E or
                codepoint == 0x0001F91F or
                0x0001F920 <= codepoint <= 0x0001F927 or
                0x0001F928 <= codepoint <= 0x0001F92F or
                codepoint == 0x0001F930 or
                0x0001F931 <= codepoint <= 0x0001F932 or
                0x0001F933 <= codepoint <= 0x0001F93A or
                0x0001F93C <= codepoint <= 0x0001F93E or
                codepoint == 0x0001F93F or
                0x0001F940 <= codepoint <= 0x0001F945 or
                0x0001F947 <= codepoint <= 0x0001F94B or
                codepoint == 0x0001F94C or
                0x0001F94D <= codepoint <= 0x0001F94F or
                0x0001F950 <= codepoint <= 0x0001F95E or
                0x0001F95F <= codepoint <= 0x0001F96B or
                0x0001F96C <= codepoint <= 0x0001F970 or
                codepoint == 0x0001F971 or
                codepoint == 0x0001F972 or
                0x0001F973 <= codepoint <= 0x0001F976 or
                0x0001F977 <= codepoint <= 0x0001F978 or
                codepoint == 0x0001F979 or
                codepoint == 0x0001F97A or
                codepoint == 0x0001F97B or
                0x0001F97C <= codepoint <= 0x0001F97F or
                0x0001F980 <= codepoint <= 0x0001F984 or
                0x0001F985 <= codepoint <= 0x0001F991 or
                0x0001F992 <= codepoint <= 0x0001F997 or
                0x0001F998 <= codepoint <= 0x0001F9A2 or
                0x0001F9A3 <= codepoint <= 0x0001F9A4 or
                0x0001F9A5 <= codepoint <= 0x0001F9AA or
                0x0001F9AB <= codepoint <= 0x0001F9AD or
                0x0001F9AE <= codepoint <= 0x0001F9AF or
                0x0001F9B0 <= codepoint <= 0x0001F9B9 or
                0x0001F9BA <= codepoint <= 0x0001F9BF or
                codepoint == 0x0001F9C0 or
                0x0001F9C1 <= codepoint <= 0x0001F9C2 or
                0x0001F9C3 <= codepoint <= 0x0001F9CA or
                codepoint == 0x0001F9CB or
                codepoint == 0x0001F9CC or
                0x0001F9CD <= codepoint <= 0x0001F9CF or
                0x0001F9D0 <= codepoint <= 0x0001F9E6 or
                0x0001F9E7 <= codepoint <= 0x0001F9FF or
                0x0001FA70 <= codepoint <= 0x0001FA73 or
                codepoint == 0x0001FA74 or
                0x0001FA75 <= codepoint <= 0x0001FA77 or
                0x0001FA78 <= codepoint <= 0x0001FA7A or
                0x0001FA7B <= codepoint <= 0x0001FA7C or
                0x0001FA80 <= codepoint <= 0x0001FA82 or
                0x0001FA83 <= codepoint <= 0x0001FA86 or
                0x0001FA87 <= codepoint <= 0x0001FA88 or
                0x0001FA90 <= codepoint <= 0x0001FA95 or
                0x0001FA96 <= codepoint <= 0x0001FAA8 or
                0x0001FAA9 <= codepoint <= 0x0001FAAC or
                0x0001FAAD <= codepoint <= 0x0001FAAF or
                0x0001FAB0 <= codepoint <= 0x0001FAB6 or
                0x0001FAB7 <= codepoint <= 0x0001FABA or
                0x0001FABB <= codepoint <= 0x0001FABD or
                codepoint == 0x0001FABF or
                0x0001FAC0 <= codepoint <= 0x0001FAC2 or
                0x0001FAC3 <= codepoint <= 0x0001FAC5 or
                0x0001FACE <= codepoint <= 0x0001FACF or
                0x0001FAD0 <= codepoint <= 0x0001FAD6 or
                0x0001FAD7 <= codepoint <= 0x0001FAD9 or
                0x0001FADA <= codepoint <= 0x0001FADB or
                0x0001FAE0 <= codepoint <= 0x0001FAE7 or
                codepoint == 0x0001FAE8 or
                0x0001FAF0 <= codepoint <= 0x0001FAF6 or
                0x0001FAF7 <= codepoint <= 0x0001FAF8)

    @staticmethod
    def find_block(codepoint):
        """
        """
        assert Text.valid_codepoint(codepoint)
        lo = 0
        hi = len(Text.UNICODE_BLOCK_STARTS) - 1
        while lo <= hi:
            mid = (hi + lo) // 2
            if codepoint > Text.UNICODE_BLOCK_STARTS[mid]:
                lo = mid + 1
            elif codepoint < Text.UNICODE_BLOCK_STARTS[mid]:
                hi = mid - 1
            else:
                return mid
        return min(lo, hi)  # always consider top of the interval

    @staticmethod
    def get_block_range(codepoint):
        """
        """
        assert Text.valid_codepoint(codepoint)
        start_block = Text.find_block(codepoint)
        start = Text.UNICODE_BLOCK_STARTS[start_block]
        if start_block < len(Text.UNICODE_BLOCK_STARTS) - 1:
            end_block = start_block + 1
            end = Text.UNICODE_BLOCK_STARTS[end_block] - 1
        else:
            end = Text.MAX_CODE_POINT
        return start, end

    @staticmethod
    def pictographs(codepoint):
        """
        1F300 - 1F5FF Miscellaneous Symbols and Pictographs.
        """
        start, end = Text.get_block_range(codepoint)
        return start == 0x0001F300 and end == 0x0001F600 - 1

    @staticmethod
    def miscellaneous_symbols(codepoint):
        """
        2600 - 26FF Miscellaneous Symbols.
        """
        start, end = Text.get_block_range(codepoint)
        return start == 0x00002600 and end == 0x00002700 - 1

    @staticmethod
    def dingbats(codepoint):
        """
        2700 - 27BF Dingbats.
        """
        start, end = Text.get_block_range(codepoint)
        return start == 0x00002700 and end == 0x000027C0 - 1
