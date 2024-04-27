#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification interceptor interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.messages.message import Message


class Notification(Message):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def intercept(self, notification):
        """
        """
        raise NotImplemented(self.intercept.__qualname__)
