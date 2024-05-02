#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator query handler interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.middleware.handlers.handler import Handler


class QueryHandler(Handler):
    """
    """
    def __init__(self, configuration, logger):
        """
        """
        super().__init__(configuration, logger)

    @abstractmethod
    def handle(self, context, next_handler=None):
        """
        """
        raise NotImplemented(self.handle.__qualname__)

    @abstractmethod
    async def handle_async(self, context, next_handler=None):
        """
        """  # noqa
        raise NotImplemented(self.handle_async.__qualname__)
