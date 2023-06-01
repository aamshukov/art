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
        result = super().__hash__() ^ hash(self._version)
        return result

    @abstractmethod
    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  Text.equal(self._version, other.version))
        return result

    @abstractmethod
    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._version < other.version)
        return result

    @abstractmethod
    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._version <= other.version)
        return result

    @property
    def version(self):
        """
        """
        return self._version

    @abstractmethod
    def validate(self):
        """
        """
        pass
