#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator command handler interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.handlers.handler import Handler


class CommandHandler(Handler):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def handle(self, context):
        """
        """
        raise NotImplemented(self.handle.__qualname__)

    @abstractmethod
    async def handle_async(self, context):
        """
        """  # noqa
        raise NotImplemented(self.handle_async.__qualname__)
