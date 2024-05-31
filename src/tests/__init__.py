#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
VERSION = (1, 0, 0)
__version__ = '.'.join([str(x) for x in VERSION])
__all__ = ['data_equal']


@staticmethod
def data_equal(lhs, rhs):
    assert len(lhs) == len(rhs)
    for left, right in zip(lhs, rhs):
        if left != ord(right):
            return False
    return True
