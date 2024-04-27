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
    def send_request(self, request, *args, **kwargs):
        """
        """
        raise NotImplemented(self.send_request.__qualname__)

    @abstractmethod
    def send_command(self, command, *args, **kwargs):
        """
        """
        raise NotImplemented(self.send_command.__qualname__)

    @abstractmethod
    def send_query(self, query, *args, **kwargs):
        """
        """
        raise NotImplemented(self.send_query.__qualname__)
