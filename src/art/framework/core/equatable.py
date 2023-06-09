#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Equatable interface """
from abc import abstractmethod
from art.framework.core.base import Base


class Equatable(Base):
    """
    """
    @abstractmethod
    def __hash__(self):
        """
        """
        raise NotImplemented(self.__hash__.__qualname__)

    @abstractmethod
    def __eq__(self, other):
        """
        """
        raise NotImplemented(self.__eq__.__qualname__)

    @abstractmethod
    def __lt__(self, other):
        """
        """
        raise NotImplemented(self.__lt__.__qualname__)

    @abstractmethod
    def __le__(self, other):
        """
        """
        raise NotImplemented(self.__le__.__qualname__)
