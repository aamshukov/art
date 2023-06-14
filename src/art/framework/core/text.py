#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String extensions """
import ctypes
import functools
import random
import string
import unicodedata
from art.framework.core.base import Base


class Text(Base):
    """
    """
    # http://www.unicode.org/glossary/#high_surrogate_code_unit
    HIGH_SURROGATE_START = 0x0000D800
    HIGH_SURROGATE_END = 0x0000DBFF

    # http://www.unicode.org/glossary/#low_surrogate_code_unit
    LOW_SURROGATE_START = 0x0000DC00
    LOW_SURROGATE_END = 0x0000DFFF

    # http://www.unicode.org/glossary/#supplementary_code_point
    SUPPLEMENTARY_CODE_POINT_START = 0x010000
    SUPPLEMENTARY_CODE_POINT_END = 0x10FFFF

    @staticmethod
    def equal(lhs, rhs, case_insensitive=False, normalization_form='NFKC'):
        """
        """
        assert lhs is not None
        assert rhs is not None
        nfc = functools.partial(unicodedata.normalize, normalization_form)
        if case_insensitive:
            return nfc(lhs).casefold() == nfc(rhs).casefold()
        else:
            return nfc(lhs) == nfc(rhs)

    @staticmethod
    def compare(lhs, rhs, case_insensitive=False, normalization_form='NFKC'):
        """
        """
        assert lhs is not None
        assert rhs is not None
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
    def make_codepoint(high_surrogate_code_unit, low_surrogate_code_unit):
        """
        https://learn.microsoft.com/en-us/dotnet/standard/base-types/character-encoding-introduction
        """
        return (Text.SUPPLEMENTARY_CODE_POINT_START +
                ((high_surrogate_code_unit - Text.HIGH_SURROGATE_START) * 0x0400 +
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
    def bad_codepoint():
        """
        """
        return 0x0F000002

    @staticmethod
    def eos_codepoint():
        """
        """
        return 0x0000001A

    @staticmethod
    def epsilon_codepoint(codepoint):
        """
        """
        return codepoint == 0x000003B5

    @staticmethod
    def epsilon(ch):
        """
        """
        return ch == 'ε'

    @staticmethod
    def identifier_start(ch):
        """
        """
        return (Text.letter(ch) or
                Text.underscore(ch) or
                Text.dollar_sign(ch) or
                Text.currency_sign(ch) or
                Text.connector_punctuation(ch))

    @staticmethod
    def identifier_part(ch):
        """
        """
        return (Text.letter(ch) or
                Text.decimal_digit_number(ch) or
                Text.underscore(ch) or
                Text.dollar_sign(ch) or
                Text.letter_number(ch) or
                Text.currency_sign(ch) or
                Text.connector_punctuation(ch) or
                Text.spacing_mark(ch) or
                Text.non_spacing_mark(ch))

    @staticmethod
    def letter(ch):
        """
        """
        match ch:
            case ('A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'G' | 'H' | 'I' | 'J' | 'K' | 'L' | 'M' |
                  'N' | 'O' | 'P' | 'Q' | 'R' | 'S' | 'T' | 'U' | 'V' | 'W' | 'X' | 'Y' | 'Z' |
                  'a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h' | 'i' | 'j' | 'k' | 'l' | 'm' |
                  'n' | 'o' | 'p' | 'q' | 'r' | 's' | 't' | 'u' | 'v' | 'w' | 'x' | 'y' | 'z'):
                return True
            case _:
                category = unicodedata.category(ch)
                match category:
                    case 'Lu' | 'Ll' | 'Lt' | 'Lm' | 'Lo':
                        return True
                    case _:
                        return False

    @staticmethod
    def octal_digit(ch):
        """
        Only considering ASCII table when use octal numbers during lexical analyze.
        """
        match ch:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7':
                return True
            case _:
                return False

    @staticmethod
    def decimal_digit_number(ch):
        """
        """
        match ch:
            case '0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
                return True
            case _:
                return unicodedata.category(ch) == 'Nd'

    @staticmethod
    def hexadecimal_digit(ch):
        """
        """
        match ch:
            case ('0' | '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' |
                  'A' | 'B' | 'C' | 'D' | 'E' | 'F' | 'a' | 'b' | 'c' | 'd' | 'e' | 'f'):
                return True
            case _:
                codepoint = ord(ch)
                # if (0x0066 >= codepoint >= 0x0041 and (codepoint <= 0x0046 or codepoint >= 0x0061)) or \
                if 0xFF21 <= codepoint <= 0xFF46 and (codepoint <= 0xFF26 or codepoint >= 0XFF41):
                    return True
                else:
                    return unicodedata.category(ch) == 'Nd'

    @staticmethod
    def letter_number(ch):
        """
        """
        return unicodedata.category(ch) == 'Nl'

    @staticmethod
    def spacing_mark(ch):
        """
        """
        return unicodedata.category(ch) == 'Mc'

    @staticmethod
    def non_spacing_mark(ch):
        """
        """
        return unicodedata.category(ch) == 'Mn'

    @staticmethod
    def whitespace(ch):
        """
        """
        match ch:
            case ' ' | '\t' | '\f':
                return True
            case _:
                return unicodedata.category(ch) == 'Zs'

    @staticmethod
    def eol(ch):
        """
        """
        match ch:
            case '\n' | '\r':
                return True
            case _:
                codepoint = ord(ch)
                return codepoint == 0x0085 or codepoint == 0x2028 or codepoint == 0x2029

    @staticmethod
    def eos(ch):
        """
        """
        codepoint = ord(ch)
        return codepoint == 0x001A or codepoint == 0x0004 or codepoint == 0x2404

    @staticmethod
    def underscore(ch):
        """
        Low Line (Underscore) _
        """
        match ch:
            case '_':
                return True
            case _:
                return unicodedata.category(ch) == 'Pc'

    @staticmethod
    def connector_punctuation(ch):
        """
        Connector Punctuation
        """
        return unicodedata.category(ch) == 'Pc'

    @staticmethod
    def dollar_sign(ch):
        """
        Dollar Sign $
        """
        return ch == '$'

    @staticmethod
    def currency_sign(ch):
        """
        Currency Sign
        """
        return unicodedata.category(ch) == 'Sc'

    @staticmethod
    def left_parenthesis(ch):
        """
        Left Parenthesis (
        """
        return ch == '(' or ch == '（' or ch == '﹙' or ch == '₍' or ch == '⁽' or ch == '︵'

    @staticmethod
    def right_parenthesis(ch):
        """
        Right Parenthesis )
        """
        return ch == ')' or ch == '）' or ch == '﹚' or ch == '₎' or ch == '⁾' or ch == '︶'

    @staticmethod
    def left_square_bracket(ch):
        """
        Left Square Bracket [
        """
        return ch == '[' or ch == '［' or ch == '﹇'

    @staticmethod
    def right_square_bracket(ch):
        """
        Right Square Bracket ]
        """
        return ch == ']' or ch == '］' or ch == '﹈'

    @staticmethod
    def left_curly_bracket(ch):
        """
        Left Curly Bracket {
        """
        return ch == '{' or ch == '｛' or ch == '﹛' or ch == '︷'

    @staticmethod
    def right_curly_bracket(ch):
        """
        Right Curly Bracket }
        """
        return ch == '}' or ch == '｝' or ch == '﹜' or ch == '︸'

    @staticmethod
    def plus_sign(ch):
        """
        Plus Sign +
        """
        return ch == '+' or ch == '＋' or ch == '﹢' or ch == '﬩' or ch == '₊' or ch == '⁺'

    @staticmethod
    def hyphen_minus(ch):
        """
        Hyphen-Minus -
        """
        return ch == '-' or ch == '－' or ch == '﹣'

    @staticmethod
    def asterisk(ch):
        """
        Asterisk (Mul) *
        """
        return ch == '*' or ch == '＊' or ch == '﹡'

    @staticmethod
    def forward_slash(ch):
        """
        Solidus (Div) (Forward slash) /
        """
        return ch == '/' or ch == '／'

    @staticmethod
    def back_slash(ch):
        """
        Reverse Solidus (Back slash) \
        """
        return ch == '\\' or ch == '＼' or ch == '﹨'

    @staticmethod
    def equals_sign(ch):
        """
        Equals Sign =
        """
        return ch == '=' or ch == '＝' or ch == '﹦' or ch == '₌' or ch == '⁼'

    @staticmethod
    def less_than_sign(ch):
        """
        Less-Than Sign <
        """
        return ch == '<' or ch == '＜' or ch == '﹤'

    @staticmethod
    def greater_than_sign(ch):
        """
        Greater-Than Sign >
        """
        return ch == '>' or ch == '＞' or ch == '﹥'

    @staticmethod
    def dot(ch):
        """
        Full Stop (Dot) .
        """
        return ch == '.' or ch == '．' or ch == '﹒'

    @staticmethod
    def colon(ch):
        """
        Colon :
        """
        return ch == ':' or ch == '：' or ch == '﹕' or ch == '︓'

    @staticmethod
    def comma(ch):
        """
        Comma ,
        """
        return ch == ',' or ch == '，' or ch == '﹐' or ch == '︐'

    @staticmethod
    def semicolon(ch):
        """
        Semicolon ;
        """
        return ch == ';' or ch == '；' or ch == '﹔' or ch == '︔'

    @staticmethod
    def vertical_line(ch):
        """
        Vertical Line (Bar) |
        """
        return ch == '|' or ch == '｜'

    @staticmethod
    def grave_accent(ch):
        """
        Grave Accent `
        """
        return ch == '`' or ch == '｀' or ch == '`'

    @staticmethod
    def tilde(ch):
        """
        Tilde ~
        """
        return ch == '~' or ch == '～'

    @staticmethod
    def apostrophe(ch):
        """
        Apostrophe '
        """
        return ch == '\'' or ch == '＇'

    @staticmethod
    def exclamation_mark(ch):
        """
        Exclamation Mark !
        """
        return ch == '!' or ch == '！' or ch == '︕' or ch == '﹗'

    @staticmethod
    def question_mark(ch):
        """
        Question Mark ?
        """
        return ch == '?' or ch == '？' or ch == '︖' or ch == '﹖'

    @staticmethod
    def quotation_mark(ch):
        """
        Quotation Mark "
        """
        return ch == '"' or ch == '＂'

    @staticmethod
    def commercial_at(ch):
        """
        Commercial At @
        """
        return ch == '@' or ch == '＠' or ch == '﹫'

    @staticmethod
    def number_sign(ch):
        """
        Number Sign #
        """
        return ch == '#' or ch == '＃' or ch == '﹟'

    @staticmethod
    def percent_sign(ch):
        """
        Percent Sign %
        """
        return ch == '%' or ch == '％' or ch == '﹪'

    @staticmethod
    def circumflex_accent(ch):
        """
        Circumflex Accent (Xor) ^
        """
        return ch == '^' or ch == '＾'

    @staticmethod
    def ampersand(ch):
        """
        Ampersand &
        """
        return ch == '&' or ch == '＆' or ch == '﹠'
