#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator command interceptor interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Interceptor(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def intercept(self, context):
        """
        """
        raise NotImplemented(self.intercept.__qualname__)
