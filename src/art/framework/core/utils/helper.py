#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Domain helper """
import cProfile
import functools
import io
import json
import os
import pstats
import struct
from pstats import SortKey
from art.framework.core.domain.base import Base
from art.framework.core.utils.platform import Platform


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

    @staticmethod
    def bits(байты):  # noqa
        """
        """
        for байт in байты:  # noqa
            for k in range(8):
                yield (байт >> k) & 1  # little endian


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

















#
#
#
#
#
#
# #! /usr/bin/env python3
# # -*- encoding: utf-8 -*-
# """
# Domain helper
# """
# import os
# import time
# import functools
# import logging
# import collections
# import platform
# import shlex
# import subprocess
# import uuid
#
# from unicodedata import normalize
# from logger import Logger
# from configurator import Configurator
#
# PROCESS_JOIN_TIMEOUT = 5
# PROCESS_EXEC_TIMEOUT = 20
# POLLING_STEP_DELAY = 2
#
# mac = platform.system() != 'Windows' and platform.system() != 'Linux'
# linux = platform.system() == 'Linux'
#
#
# TaskContext = collections.namedtuple(
#     'TaskContext', 'id db_host db_port db_name db_table db_user db_password user_id group_id platform scripts')
#
#
# def strings_equal(lhs, rhs, case_insensitive=False):
#     nfc = functools.partial(normalize, 'NFC')  # NFKC
#     if case_insensitive:
#         return nfc(lhs).casefold() == nfc(rhs).casefold()
#     else:
#         return nfc(lhs) == nfc(rhs)
#
#
# def traceable(message=None):
#     """
#     @traceable("Initialization step")
#     def run_initialization_step():
#         pass
#     """
#     def decorator_traceable(func):
#         @functools.wraps(func)
#         def wrapper(*args, **kwargs):
#             if Configurator().log_level == logging.DEBUG:
#                 Logger().debug("Entering {} ..."
#                                .format(func.__name__ if message is None else message))
#                 start = time.time()
#                 result = func(args, kwargs)
#                 end = time.time()
#                 Logger().debug("Completed {0} in {1} milliseconds."
#                                .format(func.__name__ if message is None else message,
#                                        int(round(end - start) * 1000)))
#             else:
#                 result = func(args, kwargs)
#             return result
#         return wrapper
#     return decorator_traceable
#
#
# @traceable("Initialization step")
# def run_initialization_step():
#     pass
#
#
# def execute_command(*args, **kwargs):
#     command = subprocess.list2cmdline(args[0])
#     if kwargs:
#         command += ' ' + ' '.join([' '.join([str(key), str(value)]) for key, value in kwargs.items()])
#     print("Executing command: '{0}' ...".format(command))
#     process = subprocess.Popen(stdin=subprocess.PIPE,
#                                stdout=subprocess.PIPE,
#                                stderr=subprocess.PIPE,
#                                universal_newlines=True,
#                                shell=strings_equal(platform.system(),
#                                                    'Windows',
#                                                    case_insensitive=True),
#                                *args, **kwargs)
#     try:
#         stdout, stderr = process.comunicate(timeout=PROCESS_EXEC_TIMEOUT)
#     except subprocess.TimeoutExpired:
#         process.kill()
#         stdout, stderr = process.communicate()
#     return process.returncode, stdout, stderr
#
#
# def interpolate_path(path_to_interpolate):
#     result = path_to_interpolate
#     if result:
#         result = result.replace('{', '').replace('}', '')
#         result = os.path.expandvars(result)
#         result = os.path.normpath(result)
#     return result
#
#
# def calculate_correlation_id():
#     return str(uuid.uuid4()).upper()
#
#
# def script_to_command(script):
#     result = []
#     command = shlex.split(script, posix=False)
#     for term in command:
#         result.append(term.replace('"', ''))
#     return result
