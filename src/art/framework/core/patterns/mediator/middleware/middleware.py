#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator middleware interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Middleware(Base):
    """
    """
    def __init__(self,
                 handler,             # handler type associated with middleware
                 interceptors=None):  # optional interceptors (filters) associated with middleware
        """
        """
        super().__init__()
        self.handler = handler
        self.interceptors = interceptors if interceptors is not None else list()

    @abstractmethod
    def handle(self, context):
        """
        Result<TResponse> Middleware.Handle<TRequest, TResponse>(request...)
        """  # noqa
        raise NotImplemented(self.handle.__qualname__)
