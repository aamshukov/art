#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator """
from art.framework.core.patterns.mediator.context.context import Context
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper
from art.framework.core.patterns.mediator.messages.command import Command
from art.framework.core.patterns.mediator.messages.notification import Notification
from art.framework.core.patterns.mediator.messages.query import Query
from art.framework.core.patterns.mediator.messages.request import Request
from art.framework.core.patterns.mediator.publisher import Publisher
from art.framework.core.patterns.mediator.sender import Sender
from art.framework.core.utils.helper import traceable


class Mediator(Sender, Publisher):
    """
    """
    def __init__(self,
                 configuration,
                 logger,
                 commands_registry=None,
                 notifications_registry=None,
                 queries_registry=None,
                 requests_registry=None,
                 notification_publisher=None):
        """
        """
        super().__init__()
        self.configuration = configuration
        self.logger = logger
        self.commands_registry = commands_registry
        self.notifications_registry = notifications_registry
        self.queries_registry = queries_registry
        self.requests_registry = requests_registry
        self.notification_publisher = notification_publisher

    @traceable("Mediator: send command")
    def send_command(self, command):
        """
        """
        assert type(command) is Command, f"Invalid argument type {command}, Command is expected."
        bindings = self.commands_registry.get_bindings(command)
        assert any(bindings), f"Middleware for {command} is not found."
        context = Context(request=command, configuration=self.configuration, logger=self.logger)
        return MediatorDomainHelper.send(context, bindings)

    @traceable("Mediator: send command")
    async def send_command_async(self, command):  # noqa
        """
        """
        assert type(command) is Command, f"Invalid argument type {command}, Command is expected."
        bindings = self.commands_registry.get_bindings(command)
        assert any(bindings), f"Middleware for {command} is not found."
        context = Context(request=command, configuration=self.configuration, logger=self.logger)
        return await MediatorDomainHelper.send_async(context, bindings)

    @traceable("Mediator: send query")
    def send_query(self, query):  # noqa
        """
        """
        assert type(query) is Query, f"Invalid argument type {query}, Query is expected."
        bindings = self.queries_registry.get_bindings(query)
        assert any(bindings), f"Middleware for {query} is not found."
        context = Context(request=query, configuration=self.configuration, logger=self.logger)
        return MediatorDomainHelper.send(context, bindings)

    @traceable("Mediator: send query")
    async def send_query_async(self, query):  # noqa
        """
        """
        assert type(query) is Query, f"Invalid argument type {query}, Query is expected."
        bindings = self.queries_registry.get_bindings(query)
        assert any(bindings), f"Middleware for {query} is not found."
        context = Context(request=query, configuration=self.configuration, logger=self.logger)
        return await MediatorDomainHelper.send_async(context, bindings)

    @traceable("Mediator: send request")
    def send_request(self, request):  # noqa
        """
        """
        assert type(request) is Request, f"Invalid argument type {request}, Request is expected."
        bindings = self.requests_registry.get_bindings(request)
        assert any(bindings), f"Middleware for {request} is not found."
        context = Context(request=request, configuration=self.configuration, logger=self.logger)
        return MediatorDomainHelper.send(context, bindings)

    @traceable("Mediator: send request")
    async def send_request_async(self, request):  # noqa
        """
        """
        assert type(request) is Request, f"Invalid argument type {request}, Request is expected."
        bindings = self.requests_registry.get_bindings(request)
        assert any(bindings), f"Middleware for {request} is not found."
        context = Context(request=request, configuration=self.configuration, logger=self.logger)
        return await MediatorDomainHelper.send_async(context, bindings)

    @traceable("Mediator: publish notification")
    def publish(self, notification):  # noqa
        """
        """
        assert self.notification_publisher, "Notification publisher is not provided."
        assert type(notification) is Notification, f"Invalid argument type {notification}, Request is expected."
        bindings = self.notifications_registry.get_bindings(notification)
        assert any(bindings), f"Middleware for {notification} is not found."
        context = Context(request=notification, configuration=self.configuration, logger=self.logger)
        return self.notification_publisher.publish(context, bindings)

    async def publish_async(self, notification):  # noqa
        """
        """
        assert self.notification_publisher, "Notification publisher is not provided."
        assert type(notification) is Notification, f"Invalid argument type {notification}, Request is expected."
        bindings = self.notifications_registry.get_bindings(notification)
        assert any(bindings), f"Middleware for {notification} is not found."
        context = Context(request=notification, configuration=self.configuration, logger=self.logger)
        return await self.notification_publisher.publish_async(context, bindings)
