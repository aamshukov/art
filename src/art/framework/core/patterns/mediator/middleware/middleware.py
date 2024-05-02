#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator middleware """
from art.framework.core.diagnostics.code import Code
from art.framework.core.domain.base import Base
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper


class Middleware(Base):
    """
    """
    def __init__(self,
                 configuration,
                 logger,
                 handler,             # handler type associated with middleware
                 interceptors=None):  # optional interceptor (filter) types associated with middleware
        """
        """
        super().__init__()
        self.configuration = configuration
        self.logger = logger
        self.handler = handler
        self.interceptors = interceptors if interceptors is not None else list()

    @MediatorDomainHelper.traceable()
    def handle(self, context):
        """
        Result<TResponse> Middleware.Handle<TRequest, TResponse>(request...)
        """  # noqa
        for interceptor in self.interceptors:
            result = interceptor(self.configuration, self.logger).intercept(context)
            context.results.append(result)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            result = self.handler(self.configuration, self.logger).handle(context)
            context.results.append(result)
        return result

    @MediatorDomainHelper.traceable_async()
    async def handle_async(self, context):
        """
        Result<TResponse> Middleware.Handle<TRequest, TResponse>(request...)
        """  # noqa
        for interceptor in self.interceptors:
            result = await interceptor(self.configuration, self.logger).intercept_async(context)
            context.results.append(result)
            if result.status.custom_code == Code.Aborted:
                break
        else:
            result = await self.handler(self.configuration, self.logger).handle_async(context)
            context.results.append(result)
        return result
