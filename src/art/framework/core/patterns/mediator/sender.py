#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator sender """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Sender(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def send_command(self, command):
        """
        """
        raise NotImplemented(self.send_command.__qualname__)

    @abstractmethod
    async def send_command_async(self, command):
        """
        """
        raise NotImplemented(self.send_command_async.__qualname__)

    @abstractmethod
    def send_query(self, query):
        """
        """
        raise NotImplemented(self.send_query.__qualname__)

    @abstractmethod
    async def send_query_async(self, query):
        """
        """
        raise NotImplemented(self.send_query_async.__qualname__)

    @abstractmethod
    def send_request(self, request):
        """
        """
        raise NotImplemented(self.send_request.__qualname__)

    @abstractmethod
    async def send_request_async(self, request):
        """
        """
        raise NotImplemented(self.send_request_async.__qualname__)
