#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Entity type """
from abc import abstractmethod
from art.framework.core.flags import Flags
from art.framework.core.value import Value


class Entity(Value):
    """
    """
    def __init__(self,
                 id,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(value, version)
        self.id = id
        self.attributes = attributes if attributes else dict()
        self.flags = flags

    @abstractmethod
    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self.id)
        return result

    @abstractmethod
    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self.id == other.id)
        return result

    @abstractmethod
    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self.id < other.id)
        return result

    @abstractmethod
    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self.id <= other.id)
        return result

    @abstractmethod
    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)
