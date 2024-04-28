#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator publisher """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Publisher(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def publish(self, notification):
        """
        """
        raise NotImplemented(self.publish.__qualname__)

    @abstractmethod
    def publish_async(self, notification):
        """
        """
        raise NotImplemented(self.publish.__qualname__)
