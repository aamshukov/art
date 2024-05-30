#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Value type """
from abc import abstractmethod
from art.framework.core.domain.equatable import Equatable
from art.framework.core.domain.versional import Versional
from art.framework.core.text.text import Text


class Value(Equatable, Versional):
    """
    """
    def __init__(self, value=None, version='1.0'):
        """
        """
        super().__init__(version=version)
        self.value = value

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
        if other.__class__ is self.__class__:
            result = (self.value < other.value and
                      Text.compare(self.version, other.version) < 0)
        else:
            result = NotImplemented
        return result

    @abstractmethod
    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (self.value <= other.value and
                      Text.compare(self.version, other.version) <= 0)
        else:
            result = NotImplemented
        return result

    @abstractmethod
    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.value}:{self.version}"
