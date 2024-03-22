#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Burrows–Wheeler transform (BWT). """
from art.framework.core.algorithm.suffix_array import SuffixArray
from art.framework.core.domain.base import Base


class Bwt(Base):
    """
    """
    @staticmethod
    def encode(data):
        """
        """
        suffixes = SuffixArray.build_suffix_array(data)
        result = ['$'] * (len(data) + 1)  # 0 acts as $
        for k, suffix in enumerate(suffixes):
            if suffix > 0:
                result[k] = data[suffix - 1]
        return result

    @staticmethod
    def decode(data):
        """
        https://www.student.cs.uwaterloo.ca/~cs240/f18/modules/module10.pdf
        BWT-decoding(C[0..n − 1])
         C: string of characters over alphabet Σc
         A <- array of size n
         for i = 0 to n − 1
             A[i] <- (C[i], i)
         Stably sort A by first entry
         S <- empty string
         for j = 0 to n
             if C[j] = $ break
         repeat
             j <- second entry of A[j]
             append C[j] to S
         until C[j] = $
         return S
        """
        c = data
        n = len(c)
        a = [('$', -1)] * n
        for k in range(n):
            a[k] = (c[k], k)
        a.sort(key=lambda e: str(e[0]))
        s = ''
        k = 0
        for k in range(n):
            if c[k] == '$':
                break
        while True:
            k = a[k][1]
            if c[k] == '$':
                break
            s += c[k]
        return s
