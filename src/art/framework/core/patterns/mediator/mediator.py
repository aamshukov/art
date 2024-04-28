#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator interface """
from art.framework.core.logging.logger import Logger
from art.framework.core.patterns.mediator.publisher import Publisher
from art.framework.core.patterns.mediator.publishers.sequential_publisher import SequentialPublisher
from art.framework.core.patterns.mediator.sender import Sender
from art.framework.core.utils.helper import traceable


class Mediator(Sender, Publisher):
    """
    """
    def __init__(self,
                 command_handlers=None,
                 notification_handlers=None,
                 notification_publisher=None,
                 query_handlers=None,
                 request_handlers=None,
                 logger=None):
        """
        """
        super().__init__()
        self.command_handlers = command_handlers if command_handlers is not None else dict()
        self.notification_handlers = notification_handlers if notification_handlers is not None else dict()
        self.notification_publisher = notification_publisher \
            if notification_publisher is not None else SequentialPublisher()
        self.query_handlers = query_handlers if query_handlers is not None else dict()
        self.request_handlers = request_handlers if request_handlers is not None else dict()
        self.logger = logger if logger is not None else Logger()

    @traceable("Mediator: send command")
    def send_command(self, command):
        """
        """
        assert type(command) in self.command_handlers, f"Command's {command} handler not found."
        handler = self.command_handlers[type(command)]
        return handler.handle(command)

    def send_command_async(self, command):
        """
        """
        pass

    @traceable("Mediator: send query")
    def send_query(self, query):
        """
        """
        assert type(query) in self.query_handlers, f"Query's {query} handler not found."
        handler = self.query_handlers[type(query)]
        return handler.handle(query)

    def send_query_async(self, query):
        """
        """
        pass

    @traceable("Mediator: send request")
    def send_request(self, request):
        """
        """
        assert type(request) in self.request_handlers, f"Request's {request} handler not found."
        handler = self.request_handlers[type(request)]
        return handler.handle(request)

    def send_request_async(self, request):
        """
        """
        pass

    @traceable("Mediator: publish notification")
    def publish(self, notification):
        """
        """
        handlers = {k: v for k, v in self.notification_handlers.items() if k == type(notification)}
        return self.notification_publisher.publish(handlers, notification)

    def publish_async(self, notification):
        """
        """
        pass
