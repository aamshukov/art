#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Observer design pattern """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Observer(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def on_next(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.on_next.__qualname__)

    @abstractmethod
    def on_error(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.on_error.__qualname__)

    @abstractmethod
    def on_completed(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.on_completed.__qualname__)
