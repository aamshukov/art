#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator middleware """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Middleware(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def handle(self, message, next_handler):
        """
        """
        raise NotImplemented(self.handle.__qualname__)
