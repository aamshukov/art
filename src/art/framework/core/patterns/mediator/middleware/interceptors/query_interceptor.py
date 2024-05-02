#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator query interceptor interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.middleware.interceptors.interceptor import Interceptor


class QueryInterceptor(Interceptor):
    """
    """
    def __init__(self, configuration, logger):
        """
        """
        super().__init__(configuration, logger)

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
