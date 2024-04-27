#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Result status code values """
from enum import Flag


class Code(Flag):
    """
    """
    SUCCESS_MASK     = 0x0000_0000_0000_0000  # noqa
    INFORMATION_MASK = 0x0001_0000_0000_0000  # noqa
    WARNING_MASK     = 0x0010_0000_0000_0000  # noqa
    ERROR_MASK       = 0x0100_0000_0000_0000  # noqa
    FATAL_ERROR_MASK = 0x1000_0000_0000_0000  # noqa

    Unknown     = 0                     # noqa  unknown state/value
    Ok          = 1 | SUCCESS_MASK      # noqa
    Success     = 1 | SUCCESS_MASK      # noqa
    Information = 2 | INFORMATION_MASK  # noqa
    Warning     = 3 | WARNING_MASK      # noqa
    Error       = 0 | ERROR_MASK        # noqa  failure, recoverable error
    FatalError  = 0 | FATAL_ERROR_MASK  # noqa  failure, non-recoverable error

    INVALID_LITERAL         = 128 | ERROR_MASK      # noqa
    INVALID_INT_LITERAL     = 129 | ERROR_MASK      # noqa
    INVALID_REAL_LITERAL    = 130 | ERROR_MASK      # noqa
    STATUS_DEPRECATED       = 131 | WARNING_MASK    # noqa
    INVALID_UNICODE_ESCAPE  = 132 | ERROR_MASK      # noqa
    INVALID_ESCAPE          = 133 | ERROR_MASK      # noqa
    INVALID_CHARACTER       = 134 | ERROR_MASK      # noqa
    INVALID_STRING_LITERAL  = 135 | ERROR_MASK      # noqa
    INVALID_TOKEN           = 136 | ERROR_MASK      # noqa
    INVALID_CLOSING_PAREN   = 137 | ERROR_MASK      # noqa
    INVALID_ARRAY_ELEMENTS  = 138 | ERROR_MASK      # noqa
    UNEXPEXTED_EOS          = 139 | ERROR_MASK      # noqa
