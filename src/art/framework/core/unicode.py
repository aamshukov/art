#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Unicode related content """
from enum import IntEnum


class Unicode:
    """
    """

    class Encoding(IntEnum):
        """
        """
        UNKNOWN_ENCODING = 0    # UNKNOWN, UTF-8
        UTF8_ENCODING = 1       # UTF-8
        UTF16_LE_ENCODING = 2   # UTF-16-LE
        UTF16_BE_ENCODING = 3   # UTF-16-BE
        UTF32_LE_ENCODING = 4   # UTF-32-LE
        UTF32_BE_ENCODING = 5   # UTF-32-BE
        UTF7_ENCODING = 6       # UTF-7
        UTF1_ENCODING = 7       # UTF-1
        UTF_EBCDIC_ENCODING = 8 # UTF-EBCDIC
        SDSU_ENCODING = 9       # SDSU
        BOCU1_ENCODING = 10     # BOCU-1
        GB18030_ENCODING = 11   # GB-18030
        DEFAULT_ENCODING = 12   # DEFAULT

    INVALID_UNICODE_CODEPOINT = 0xFFFFFFFF
