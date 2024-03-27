#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lempel Ziv Welch (LZW) compression algorithm """
from art.framework.core.domain.base import Base


class LzwCodec(Base):
    """
        Based on Mark Nelson's https://github.com/marknelson/LZW/blob/master/lzw.h
        and on Fundamental Data Compression, Ida Menguy Pu.
        Also see C++ codebase for details.
    """
    def __init__(self, model):
        """
        """
        super().__init__()
        self.model = model

    def encode(self, input_stream, output_stream):
        """
            1: word <-- ''
            2: while not EOF do
            3:      x <-- read_next_character()
            4:      if word + x is in the dictionary then
            5:          word <-- word + x
            6:      else
            7:          output the dictionary index for word
            8:          add word + x to the dictionary
            9:          word <-- x
            10:     end if
            11. end while
            12: output the dictionary index for word
        """
        next_code = 2
        original_size = 0
        encoded_size = 0
        word = ''
        arr = []
        while symbol := input_stream.read(1):
            original_size += 1
            word_code = word + symbol  # word + x
            if word_code in self.model.codes:
                word = word_code
            else:
                output_stream.write(self.model.codes[word].to_bytes(2, 'little'))
                arr.append(self.model.codes[word])  #??
                self.model.codes[word_code] = next_code
                next_code += 1
                encoded_size += 1
                word = symbol
        output_stream.write(self.model.codes[word].to_bytes(2, 'little'))
        arr.append(self.model.codes[word])  # ??
        encoded_size += 1
        output_stream.flush()
        return original_size, encoded_size, self.model.codes, arr

    def decode(self, input_stream, output_stream):
        """
            1:  read a token x from the compressed file
            2:  look up dictionary for element at x
            3:  output element
            4:  word <-- element
            5:  while not E0F do
            6:      read x
            7:      look up dictionary for element at x
            8:      if there is no entry yet for index x then
            9:          element <-- word + firstCharOfWord
            10:     end if
            11:     output element
            12:     add word + firstCharOfElement to the dictionary
            13:     word <-- element
            14: end while
        """
        next_code = 2
        original_size = 0
        encoded_size = 0
        word = ''
        code = input_stream.read(2)
        if code:
            code = int.from_bytes(code, 'little')
            encoded_size += 1
            element = self.model.codes[code]
            output_stream.write(element)
            original_size += len(element)
            word = element
        while code := input_stream.read(2):
            code = int.from_bytes(code, 'little')
            encoded_size += 1
            if code not in self.model.codes:
                element = word + word[0]
            else:
                element = self.model.codes[code]
            output_stream.write(element)
            original_size += len(element)
            self.model.codes[next_code] = word + element[0]
            next_code += 1
            word = element
        return original_size, encoded_size, self.model.codes
