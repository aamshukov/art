#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
import functools
import os
import sys
import struct
import json
import cProfile, pstats, io
from pstats import SortKey
from art.framework.core.base import Base
from art.framework.core.platform import Platform


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
    def real_numbers_equal(real1, real2):
        """
        """
        return abs(real1 - real2) <= Platform.epsilon()

    @staticmethod
    def increase_recursion_limit():
        """
        """
        sys.setrecursionlimit(8192)

    @staticmethod
    def dict_to_string(dictionary, flatten=True):
        """
        """
        assert dictionary is not None, "Invalid argument 'dictionary'."
        result = json.dumps(dictionary, indent=(0 if flatten else 4))
        if flatten:
            result = DomainHelper.flatten_json(result)
        return result

    @staticmethod
    def flatten_json(json_text):
        """
        """
        return json_text.replace('\n', '')


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
