#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Value type """
from abc import abstractmethod
from art.framework.core.text import Text
from art.framework.core.equatable import Equatable


class Value(Equatable):
    """
    """
    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self._version = version.strip()

    @abstractmethod
    def __hash__(self):
        """
        """
        return hash(self._version)

    @abstractmethod
    def __eq__(self, other):
        """
        """
        return Text.equal(self._version, other.version)

    @abstractmethod
    def __lt__(self, other):
        """
        """
        return Text.compare(self._version, other.version) < 0

    @abstractmethod
    def __le__(self, other):
        """
        """
        return Text.compare(self._version, other.version) <= 0

    @property
    def version(self):
        """
        """
        return self._version

    @abstractmethod
    def validate(self):
        """
        """
        return True
