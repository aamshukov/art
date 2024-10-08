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
    def __init__(self, configuration, logger):
        """
        """
        super().__init__()
        self.configuration = configuration
        self.logger = logger

    @abstractmethod
    def publish(self, context, bindings):
        """
        """
        raise NotImplemented(self.publish.__qualname__)

    @abstractmethod
    async def publish_async (self, context, bindings):
        """
        """
        raise NotImplemented(self.publish_async .__qualname__)
