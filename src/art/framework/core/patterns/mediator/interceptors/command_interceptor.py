#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator command interceptor interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.interceptors.interceptor import Interceptor


class CommandInterceptor(Interceptor):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def intercept(self, context):
        """
        """
        raise NotImplemented(self.intercept.__qualname__)

    @abstractmethod
    async def handle_async(self, context):
        """
        """  # noqa
        raise NotImplemented(self.handle_async.__qualname__)
