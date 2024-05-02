#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator binding """
from art.framework.core.domain.base import Base


class MiddlewareBinding(Base):
    """
    """
    def __init__(self,
                 message,      # message type (Command, Notification, Query, Request, etc.)
                 middleware):  # middleware with handler and interceptors types
        """
        """
        super().__init__()
        self.message = message
        self.middleware = middleware
