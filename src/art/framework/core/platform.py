#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Platform specific """
import sys
from art.framework.core.base import Base


class Platform(Base):
    """
    """
    BYTE_BITS = 8

    def __init__(self):
        """
        """
        super().__init__()

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
    def epsilon():
        """
        """
        return sys.float_info.epsilon
