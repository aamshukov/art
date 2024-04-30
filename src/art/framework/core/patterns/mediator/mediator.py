#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator interface """
from art.framework.core.logging.logger import Logger
from art.framework.core.patterns.mediator.context.context import Context
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper
from art.framework.core.patterns.mediator.publisher import Publisher
from art.framework.core.patterns.mediator.sender import Sender
from art.framework.core.utils.helper import traceable
from art.framework.core.patterns.mediator.messages import command as msg_command
from art.framework.core.patterns.mediator.messages import query as msg_query
from art.framework.core.patterns.mediator.messages import request as msg_request
from art.framework.core.patterns.mediator.messages import notification as msg_notification


class Mediator(Sender, Publisher):
    """
    """
    def __init__(self,
                 commands_registry=None,
                 notifications_registry=None,
                 queries_registry=None,
                 requests_registry=None,
                 notification_publisher=None,
                 logger=None):
        """
        """
        super().__init__()
        self.commands_registry = commands_registry
        self.notifications_registry = notifications_registry
        self.queries_registry = queries_registry
        self.requests_registry = requests_registry
        self.notification_publisher = notification_publisher
        self.logger = logger if logger is not None else Logger()

    @traceable("Mediator: send command")
    def send_command(self, command):
        """
        """
        assert type(command) is msg_command, f"Invalid argument type {command}, Command is expected."
        bindings = self.commands_registry.get_bindings(command)
        assert any(bindings), f"Middleware for {command} is not found."
        context = Context(request=command)
        return MediatorDomainHelper.send(context, bindings)

    def send_command_async(self, command):  # noqa
        """
        """
        pass

    @traceable("Mediator: send query")
    def send_query(self, query):  # noqa
        """
        """
        assert type(query) is msg_query, f"Invalid argument type {query}, Query is expected."
        bindings = self.queries_registry.get_bindings(query)
        assert any(bindings), f"Middleware for {query} is not found."
        context = Context(request=query)
        return MediatorDomainHelper.send(context, bindings)

    def send_query_async(self, query):  # noqa
        """
        """
        pass

    @traceable("Mediator: send request")
    def send_request(self, request):  # noqa
        """
        """
        assert type(request) is msg_request, f"Invalid argument type {request}, Request is expected."
        bindings = self.requests_registry.get_bindings(request)
        assert any(bindings), f"Middleware for {request} is not found."
        context = Context(request=request)
        return MediatorDomainHelper.send(context, bindings)

    def send_request_async(self, request):  # noqa
        """
        """
        pass

    @traceable("Mediator: publish notification")
    def publish(self, notification):  # noqa
        """
        """
        assert type(notification) is msg_notification, f"Invalid argument type {notification}, Request is expected."
        bindings = self.notifications_registry.get_bindings(notification)
        assert any(bindings), f"Middleware for {notification} is not found."
        context = Context(request=notification)
        return MediatorDomainHelper.send(context, bindings)

    def publish_async(self, notification):  # noqa
        """
        """
        pass
