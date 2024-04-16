#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Observable design pattern """
from art.framework.core.domain.base import Base


class Observable(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.observers = list()

    def register(self, observer):
        """
        """
        self.observers.append(observer)
        return self

    def unregister(self, observer):
        """
        """
        self.observers.remove(observer)
        return self
