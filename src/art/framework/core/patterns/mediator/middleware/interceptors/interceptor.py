#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator interceptor interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Interceptor(Base):
    """
    """
    def __init__(self, configuration, logger):
        """
        """
        super().__init__()
        self.configuration = configuration
        self.logger = logger

    @abstractmethod
    def intercept(self, context):
        """
        """
        raise NotImplemented(self.intercept.__qualname__)

    @abstractmethod
    async def intercept_async(self, context):
        """
        """  # noqa
        raise NotImplemented(self.intercept_async.__qualname__)
