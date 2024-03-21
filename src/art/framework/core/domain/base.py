#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Root class """
from abc import ABCMeta, abstractmethod


class Base(metaclass=ABCMeta):
    """
    """
    def __init__(self):
        """
        """
        pass

    def __repr__(self):
        """
        """
        return self.stringify()

    __str__ = __repr__

    def stringify(self):
        """
        """
        return f"{type(self).__name__}"
