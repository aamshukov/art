#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Value type """
from abc import abstractmethod
from art.framework.core.utils.text import Text
from art.framework.core.domain.equatable import Equatable


class Value(Equatable):
    """
    """
    def __init__(self, value=None, version='1.0'):
        """
        """
        super().__init__()
        self.value = value
        self.version = version.strip()

    @abstractmethod
    def __hash__(self):
        """
        """
        return hash((self.__class__, self.value, self.version))

    @abstractmethod
    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (self.value == other.value and
                      Text.equal(self.version, other.version))
        else:
            result = NotImplemented
        return result

    @abstractmethod
    def __lt__(self, other):
        """
        """
        return (self.value < other.value and
                Text.compare(self.version, other.version) < 0)

    @abstractmethod
    def __le__(self, other):
        """
        """
        return (self.value <= other.value and
                Text.compare(self.version, other.version) <= 0)

    @abstractmethod
    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)
