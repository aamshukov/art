#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art types """
from enum import Flag


class ArtTypeKind(Flag):
    """
    """
    BUILTIN_MASK   = 0x1000_0000_0000_0000_0000_0000_0000_0000  # noqa
    SCALAR_MASK    = 0x0000_0001_0000_0000_0000_0000_0000_0000  # noqa
    ARRAY_MASK     = 0x0000_0010_0000_0000_0000_0000_0000_0000  # noqa
    COMPOSITE_MASK = 0x0000_0100_0000_0000_0000_0000_0000_0000  # noqa  struct, record, tuple, enum, etc.
    SUBTYPE_MASK   = 0x0000_1000_0000_0000_0000_0000_0000_0000  # noqa  sub-type, slice, span, range, etc.
    CALLABLE_MASK  = 0x0001_0000_0000_0000_0000_0000_0000_0000  # noqa  fn, proc, lambda, slosure,
                                                                # anonymous function/procedure, etc.
    GENERIC_MASK   = 0x0010_0000_0000_0000_0000_0000_0000_0000  # noqa

    UNKNOWN_TYPE             = 0                    # noqa

    INTEGER_TYPE             =  1 | BUILTIN_MASK    # noqa  int, integer
    REAL_TYPE                =  2 | BUILTIN_MASK    # noqa  real, float, double
    STRING_TYPE              =  3 | BUILTIN_MASK    # noqa  ' "" ', " '' "
    BOOLEAN_TYPE             =  4 | BUILTIN_MASK    # noqa  true, false

    STRUCT_TYPE              =  5 | COMPOSITE_MASK  # noqa  structure
    RECORD_TYPE              =  6 | COMPOSITE_MASK  # noqa  record
    TUPLE_TYPE               =  7 | COMPOSITE_MASK  # noqa  record
    ENUM_TYPE                =  8 | COMPOSITE_MASK  # noqa  enumeration

    SUB_TYPE                 =  9 | SUBTYPE_MASK    # noqa  subtype: byte = 0-255, ascii7 = 0-127
    SLICE_TYPE               = 10 | SUBTYPE_MASK    # noqa  slice: [1:5:1]
    SPAN_TYPE                = 11 | SUBTYPE_MASK    # noqa  span: 1-5
    RANGE_TYPE               = 12 | SUBTYPE_MASK    # noqa  range: [1-5], (1-5], [1-5), (1-5), closed, half-open, open

    FUNCTION_TYPE            = 13 | CALLABLE_MASK   # noqa  fn
    ANONYMOUS_FUNCTION_TYPE  = 14 | CALLABLE_MASK   # noqa  anonymous function
    PROCEDURE_TYPE           = 15 | CALLABLE_MASK   # noqa  proc
    ANONYMOUS_PROCEDURE_TYPE = 16 | CALLABLE_MASK   # noqa  anonymous procedure
    LAMBDA_TYPE              = 17 | CALLABLE_MASK   # noqa  lambda
    CLOSURE_TYPE             = 18 | CALLABLE_MASK   # noqa  closure

    TYPE_PARAMETER           = 19 | GENERIC_MASK    # noqa
    TYPE_ARGUMENT            = 20 | GENERIC_MASK    # noqa

    @staticmethod
    def builtin(kind):
        """
        """
        return (kind & ArtTypeKind.BUILTIN_MASK) == ArtTypeKind.BUILTIN_MASK

    @staticmethod
    def integer(kind):
        """
        """
        return (kind & ArtTypeKind.INTEGER_TYPE) == ArtTypeKind.INTEGER_TYPE

    @staticmethod
    def scalar(kind):
        """
        """
        return (kind & ArtTypeKind.SCALAR_MASK) == ArtTypeKind.SCALAR_MASK

    @staticmethod
    def array(kind):
        """
        """
        return (kind & ArtTypeKind.ARRAY_MASK) == ArtTypeKind.ARRAY_MASK

    @staticmethod
    def composite(kind):
        """
        """
        return (kind & ArtTypeKind.COMPOSITE_MASK) == ArtTypeKind.COMPOSITE_MASK

    @staticmethod
    def subtype(kind):
        """
        """
        return (kind & ArtTypeKind.SUBTYPE_MASK) == ArtTypeKind.SUBTYPE_MASK

    @staticmethod
    def callable(kind):
        """
        """
        return (kind & ArtTypeKind.CALLABLE_MASK) == ArtTypeKind.CALLABLE_MASK

    @staticmethod
    def generic(kind):
        """
        """
        return (kind & ArtTypeKind.GENERIC_MASK) == ArtTypeKind.GENERIC_MASK
