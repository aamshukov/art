#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator query handler interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.handlers.handler import Handler


class QueryHandler(Handler):
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
