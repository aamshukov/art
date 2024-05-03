#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator bindings pipeline """
from art.framework.core.domain.base import Base
from art.framework.core.patterns.mediator.messages.command import Command
from art.framework.core.patterns.mediator.messages.notification import Notification
from art.framework.core.patterns.mediator.messages.query import Query
from art.framework.core.patterns.mediator.messages.request import Request
from art.framework.core.patterns.mediator.middleware.middleware_binding import MiddlewareBinding


class MiddlewarePipeline(Base):
    """
    Acts as virtual pipeline.
    """
    def __init__(self, pipeline=None):
        """
        """
        super().__init__()
        self.pipeline = pipeline if pipeline is not None else list()  # set of bindings

    def get_bindings(self, message):
        """
        """
        bindings = list()
        for binding in self.pipeline:
            if binding.message is type(message):
                bindings.append(binding)
        return bindings

    def register_command(self, command, middleware):
        """
        """
        assert issubclass(command, Command), f"Invalid argument type {command}, Command is expected."
        self.register_binding(MiddlewareBinding(command, middleware))

    def register_notification(self, notification, middleware):
        """
        """
        assert issubclass(notification, Notification),\
            f"Invalid argument type {notification}, Notification is expected."
        self.pipeline.append(MiddlewareBinding(notification, middleware))

    def register_query(self, query, middleware):
        """
        """
        assert issubclass(query, Query), f"Invalid argument type {query}, Query is expected."
        self.register_binding(MiddlewareBinding(query, middleware))

    def register_request(self, request, middleware):
        """
        """
        assert issubclass(request, Request), f"Invalid argument type {request}, Request is expected."
        self.register_binding(MiddlewareBinding(request, middleware))

    def register_binding(self, new_binding):
        """
        """
        self.pipeline.append(new_binding)
        # for binding in self.pipeline:
        #     if binding.message is new_binding.message:
        #         break
        # else:
        #     self.pipeline.append(new_binding)
