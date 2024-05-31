#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art declarations """
from enum import Flag


class ArtDeclKind(Flag):
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

    UNKNOWN_DECL             = 0                    # noqa

    INTEGER_DECL             =  1 | BUILTIN_MASK    # noqa  int, integer
    REAL_DECL                =  2 | BUILTIN_MASK    # noqa  real, float, double
    STRING_DECL              =  3 | BUILTIN_MASK    # noqa  ' "" ', " '' "
    BOOLEAN_DECL             =  4 | BUILTIN_MASK    # noqa  true, false

    STRUCT_DECL              =  5 | COMPOSITE_MASK  # noqa  structure
    RECORD_DECL              =  6 | COMPOSITE_MASK  # noqa  record
    TUPLE_DECL               =  7 | COMPOSITE_MASK  # noqa  record
    ENUM_DECL                =  8 | COMPOSITE_MASK  # noqa  enumeration

    SUB_DECL                 =  9 | SUBTYPE_MASK    # noqa  subtype: byte = 0-255, ascii7 = 0-127
    SLICE_DECL               = 10 | SUBTYPE_MASK    # noqa  slice: [1:5:1]
    SPAN_DECL                = 11 | SUBTYPE_MASK    # noqa  span: 1-5
    RANGE_DECL               = 12 | SUBTYPE_MASK    # noqa  range: [1-5], (1-5], [1-5), (1-5), closed, half-open, open

    FUNCTION_DECL            = 13 | CALLABLE_MASK   # noqa  fn
    ANONYMOUS_FUNCTION_DECL  = 14 | CALLABLE_MASK   # noqa  anonymous function
    PROCEDURE_DECL           = 15 | CALLABLE_MASK   # noqa  proc
    ANONYMOUS_PROCEDURE_DECL = 16 | CALLABLE_MASK   # noqa  anonymous procedure
    LAMBDA_DECL              = 17 | CALLABLE_MASK   # noqa  lambda
    CLOSURE_DECL             = 18 | CALLABLE_MASK   # noqa  closure

    TYPE_PARAMETER           = 19 | GENERIC_MASK    # noqa
    TYPE_ARGUMENT            = 20 | GENERIC_MASK    # noqa
