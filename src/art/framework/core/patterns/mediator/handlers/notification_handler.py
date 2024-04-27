#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification handler interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class NotificationHandler(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def handle(self, notification):
        """
        """
        raise NotImplemented(self.handle.__qualname__)
