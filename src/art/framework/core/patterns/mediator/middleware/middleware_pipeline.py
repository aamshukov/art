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
        message_type = type(message)
        for binding in self.pipeline:
            if type(binding.message) is message_type:
                bindings.append(binding)
        return bindings

    def register_command(self, binding):
        """
        """
        assert type(binding.message) is Command, f"Invalid argument type {binding.message}, Command is expected."
        self.register_binding(binding)

    def register_notification(self, binding):
        """
        """
        assert type(binding.message) is Notification,\
            f"Invalid argument type {binding.message}, Notification is expected."
        self.pipeline.append(binding)

    def register_query(self, binding):
        """
        """
        assert type(binding.message) is Query, f"Invalid argument type {binding.message}, Query is expected."
        self.register_binding(binding)

    def register_request(self, binding):
        """
        """
        assert type(binding.message) is Request, f"Invalid argument type {binding.message}, Request is expected."
        self.register_binding(binding)

    def register_binding(self, new_binding):
        """
        """
        message_type = type(new_binding.message)
        for binding in self.pipeline:
            if type(binding.message) is message_type:
                break
        else:
            self.pipeline.append(new_binding)
