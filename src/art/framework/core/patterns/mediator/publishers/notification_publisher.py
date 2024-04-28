#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification publisher interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class NotificationPublisher(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def publish(self,
                handlers,  # notification handlers
                notification):
        """
        """
        raise NotImplemented(self.publish.__qualname__)
