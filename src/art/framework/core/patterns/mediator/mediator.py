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


class Mediator(Sender, Publisher):
    """
    """
    def __init__(self,
                 configuration,
                 logger,
                 command_pipeline=None,
                 notification_pipeline=None,
                 query_pipeline=None,
                 request_pipeline=None,
                 notification_publisher=None):
        """
        """
        super().__init__()
        self.configuration = configuration
        self.logger = logger
        self.command_pipeline = command_pipeline
        self.notification_pipeline = notification_pipeline
        self.query_pipeline = query_pipeline
        self.request_pipeline = request_pipeline
        self.notification_publisher = notification_publisher

    @MediatorDomainHelper.traceable()
    def send_command(self, command):
        """
        """
        assert isinstance(command, Command), f"Invalid argument type {command}, Command is expected."
        bindings = self.command_pipeline.get_bindings(command)
        assert any(bindings), f"Middleware for {command} is not found."
        context = Context(request=command)
        return MediatorDomainHelper.send(context, bindings)

    @MediatorDomainHelper.traceable_async()
    async def send_command_async(self, command):  # noqa
        """
        """
        assert isinstance(command, Command), f"Invalid argument type {command}, Command is expected."
        bindings = self.command_pipeline.get_bindings(command)
        assert any(bindings), f"Middleware for {command} is not found."
        context = Context(request=command)
        return await MediatorDomainHelper.send_async(context, bindings)

    @MediatorDomainHelper.traceable()
    def send_query(self, query):  # noqa
        """
        """
        assert isinstance(query, Query), f"Invalid argument type {query}, Query is expected."
        bindings = self.query_pipeline.get_bindings(query)
        assert any(bindings), f"Middleware for {query} is not found."
        context = Context(request=query)
        return MediatorDomainHelper.send(context, bindings)

    @MediatorDomainHelper.traceable_async()
    async def send_query_async(self, query):  # noqa
        """
        """
        assert isinstance(query, Query), f"Invalid argument type {query}, Query is expected."
        bindings = self.query_pipeline.get_bindings(query)
        assert any(bindings), f"Middleware for {query} is not found."
        context = Context(request=query)
        return await MediatorDomainHelper.send_async(context, bindings)

    @MediatorDomainHelper.traceable()
    def send_request(self, request):  # noqa
        """
        """
        assert isinstance(request, Request), f"Invalid argument type {request}, Request is expected."
        bindings = self.request_pipeline.get_bindings(request)
        assert any(bindings), f"Middleware for {request} is not found."
        context = Context(request=request)
        return MediatorDomainHelper.send_propagated(context, bindings)

    @MediatorDomainHelper.traceable_async()
    async def send_request_async(self, request):  # noqa
        """
        """
        assert isinstance(request, Request), f"Invalid argument type {request}, Request is expected."
        bindings = self.request_pipeline.get_bindings(request)
        assert any(bindings), f"Middleware for {request} is not found."
        context = Context(request=request)
        return await MediatorDomainHelper.send_propagated_async(context, bindings)

    @MediatorDomainHelper.traceable()
    def publish(self, notification):  # noqa
        """
        """
        assert self.notification_publisher, "Notification publisher is not provided."
        assert isinstance(notification, Notification), f"Invalid argument type {notification}, Request is expected."
        bindings = self.notification_pipeline.get_bindings(notification)
        assert any(bindings), f"Middleware for {notification} is not found."
        context = Context(request=notification)
        return self.notification_publisher.publish(context, bindings)

    @MediatorDomainHelper.traceable_async()
    async def publish_async(self, notification):  # noqa
        """
        """
        assert self.notification_publisher, "Notification publisher is not provided."
        assert isinstance(notification, Notification), f"Invalid argument type {notification}, Request is expected."
        bindings = self.notification_pipeline.get_bindings(notification)
        assert any(bindings), f"Middleware for {notification} is not found."
        context = Context(request=notification)
        return await self.notification_publisher.publish_async(context, bindings)
