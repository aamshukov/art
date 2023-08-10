#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" File data provider """
import os
from art.framework.core.text import Text
from art.framework.frontend.data_provider.data_provider import DataProvider


class FileDataProvider(DataProvider):
    """
    """
    def __init__(self, source):
        """
        """
        super().__init__()
        self.source = os.path.abspath(source)

    def load(self, to_codepoints=True):
        """
        https://docs.python.org/3/library/codecs.html#encodings-and-unicode
        """
        encoding = 'UTF-8'
        bom = None
        offset = 0
        with open(self.source, 'rb', buffering=0) as stream:
            bom = stream.read(4)
        if bom is not None:
            if len(bom) >= 3 and bom[0] == 0xEF and bom[1] == 0xBB and bom[2] == 0xBF:
                encoding = 'UTF-8-SIG'
            elif len(bom) >= 4 and ((bom[0] == 0x00 and bom[1] == 0x00 and bom[2] == 0xFE and bom[3] == 0xFF) or
                                    (bom[0] == 0xFF and bom[1] == 0xFE and bom[2] == 0x00 and bom[3] == 0x00)):
                if bom[0] == 0x00 and bom[1] == 0x00 and bom[2] == 0xFE and bom[3] == 0xFF:
                    encoding = 'UTF-32BE'
                else:
                    encoding = 'UTF-32LE'
                offset = 4
            elif len(bom) >= 2 and ((bom[0] == 0xFE and bom[1] == 0xFF) or (bom[0] == 0xFF and bom[1] == 0xFE)):
                if bom[0] == 0xFE and bom[1] == 0xFF:
                    encoding = 'UTF-16BE'
                else:
                    encoding = 'UTF-16LE'
                offset = 2
        text = ''
        with open(self.source, 'rt', encoding=encoding, newline=os.linesep) as stream:
            stream.seek(offset, os.SEEK_SET)
            text = stream.read()
        if to_codepoints:
            result = Text.string_to_codepoints(text)
        else:
            result = text
        return result
