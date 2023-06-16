#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Data provider interface """
from abc import abstractmethod
from art.framework.core.base import Base


class DataProvider(Base):
    """
    """
    @abstractmethod
    def load(self, to_codepoints=False):
        """
        """
        raise NotImplemented(self.load.__qualname__)
