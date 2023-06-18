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
    BAD_CODEPOINT = 0x0000FFFD

    # http://www.unicode.org/glossary/#high_surrogate_code_unit
    HIGH_SURROGATE_START = 0x0000D800
    HIGH_SURROGATE_END = 0x0000DBFF

    # http://www.unicode.org/glossary/#low_surrogate_code_unit
    LOW_SURROGATE_START = 0x0000DC00
    LOW_SURROGATE_END = 0x0000DFFF

    # http://www.unicode.org/glossary/#supplementary_code_point
    SUPPLEMENTARY_CODE_POINT_START = 0x00010000
    SUPPLEMENTARY_CODE_POINT_END = 0x0010FFFF

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
        print(f"Listing  {category}  category ...")
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
        return (Text.SUPPLEMENTARY_CODE_POINT_START +
                ((high_surrogate_code_unit - Text.HIGH_SURROGATE_START) * 0x00000400 +
                 (low_surrogate_code_unit - Text.LOW_SURROGATE_START)))

    @staticmethod
    def high_surrogate(code_unit):
        """
        """
        return Text.HIGH_SURROGATE_START <= code_unit <= Text.HIGH_SURROGATE_END

    @staticmethod
    def low_surrogate(code_unit):
        """
        """
        return Text.LOW_SURROGATE_START <= code_unit <= Text.LOW_SURROGATE_END

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
    def octal_digit(codepoint):
        """
        Only considering ASCII table and 0xFF10 - 0xFF17
        when use octal numbers during lexical analyze.
        """
        result = ((0x00000030 <= codepoint <= 0x00000037) or
                  (0x0000FF10 <= codepoint <= 0x0000FF17))
        return result

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

    ASCII_NUMBERS = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
                     0, 0xA, 0xB, 0xC, 0xD, 0xE, 0xF, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0xa, 0xb, 0xc, 0xd, 0xe, 0xf, 0, 0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0]

    @staticmethod
    def ascii_number(digit):
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
                  0x0000000C):  # '\f'
                return True
            case _:
                ch = Text.convert_to_character(codepoint)
                return unicodedata.category(ch) == 'Zs'

    @staticmethod
    def eol(codepoint):
        """
        """
        return (codepoint == 0x0000000A or  # '\n'
                codepoint == 0x0000000D or  # '\r'
                codepoint == 0x00000085 or
                codepoint == 0x00002028 or
                codepoint == 0x00002029)

    @staticmethod
    def eos(codepoint):
        """
        Return true if codepoint is End Of Transmission.
        """
        return codepoint == 0x00000004 or codepoint == 0x00002404

    @staticmethod
    def eos_codepoint():
        """
        Return End Of Transmission (EOT) codepoint.
        """
        return 0x2404

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
    def apostrophe(codepoint):
        """
        Apostrophe '
        """
        return (codepoint == 0x00000027 or  # '\''
                codepoint == 0x0000FF07)    # '＇'

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
    def quotation_mark(codepoint):
        """
        Quotation Mark "
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
        Return true if codepoint is Ampersand &.
        """
        return (codepoint == 0x00000026 or  # '&'
                codepoint == 0x0000FF06 or  # '＆'
                codepoint == 0x0000FE60)    # '﹠'

    @staticmethod
    def epsilon(codepoint):
        """
        """
        return (codepoint == 0x000003B5 or  # 'ε'
                codepoint == 0x0001D6C6)    # '𝛆'
