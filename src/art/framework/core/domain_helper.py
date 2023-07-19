#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
import functools
import os
import sys
import struct
import cProfile, pstats, io
from pstats import SortKey
from art.framework.core.base import Base


class DomainHelper(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def collect_slots(obj):
        """
        """
        result = set()
        for klass in obj.__class__.__mro__:
            result.update(getattr(klass, '__slots__', []))
        return result

    @staticmethod
    def collect_dicts(obj):
        """
        """
        result = set()
        for klass in obj.__class__.__mro__:
            result.update(getattr(klass, '__dict__', []))
        return result

    @staticmethod
    def print_matrix(matrix):
        """
        """
        print(matrix)
        print('')

    @staticmethod
    def get_max_int():
        """
        """
        return sys.maxsize

    @staticmethod
    def get_int_size():
        """
        """
        return (sys.maxsize + 1).bit_length()

    @staticmethod
    def generate_random_bytes(length):
        """
        """
        return bytearray(os.urandom(length))

    @staticmethod
    def serialize_string(string):
        """
        """
        string = bytes(string, 'utf-8')
        result = struct.pack("I", len(string)) + string
        return result

    @staticmethod
    def deserialize_string(data, template='I'):
        """
        """
        size = struct.calcsize(template)
        result = struct.unpack(template, data[:size]), data[size:]
        return result[1].decode('utf-8')

    @staticmethod
    def pad_string(string, size, filler=' '):
        """
        """
        return string.rjust(size, filler)

    @staticmethod
    def epsilon():
        """
        """
        return sys.float_info.epsilon

    @staticmethod
    def real_numbers_equal(real1, real2):
        """
        """
        return abs(real1 - real2) <= DomainHelper.epsilon()


def profile(message=None):
    """
    @profile("Profiling foo()...")
    def foo():
        pass
    """
    def decorator_profile(func):
        @functools.wraps(func)
        def wrapped_function(*args, **kwargs):
            if message:
                print(message)
            pr = cProfile.Profile()
            pr.enable()
            result = func(*args, **kwargs)
            pr.disable()
            s = io.StringIO()
            sort_by = SortKey.CUMULATIVE
            ps = pstats.Stats(pr, stream=s).sort_stats(sort_by)
            ps.print_stats()
            print(s.getvalue())
            return result
        return wrapped_function
    return decorator_profile
