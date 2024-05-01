#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator middleware """
from art.framework.core.diagnostics.code import Code
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

    def handle(self, context):
        """
        Result<TResponse> Middleware.Handle<TRequest, TResponse>(request...)
        """  # noqa
        for interceptor in self.interceptors:
            result = interceptor.handle(context)
            context.results.append(result)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            result = self.handler.handle(context)
            context.results.append(result)
        return result

    async def handle_async(self, context):
        """
        Result<TResponse> Middleware.Handle<TRequest, TResponse>(request...)
        """  # noqa
        for interceptor in self.interceptors:
            result = await interceptor.handle_async(context)
            context.results.append(result)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            result = await self.handler.handle_async(context)
            context.results.append(result)
        return result
