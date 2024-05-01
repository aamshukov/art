#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest

from art.framework.core.configuration.configuration import Configuration
from art.framework.core.logging.logger import Logger
from art.framework.core.patterns.mediator.mediator import Mediator
from art.framework.core.patterns.mediator.messages.command import Command
from art.framework.core.patterns.mediator.messages.notification import Notification
from art.framework.core.patterns.mediator.messages.query import Query
from art.framework.core.patterns.mediator.messages.request import Request
from art.framework.core.patterns.mediator.middleware.handlers.command_handler import CommandHandler
from art.framework.core.patterns.mediator.middleware.handlers.notification_handler import NotificationHandler
from art.framework.core.patterns.mediator.middleware.handlers.query_handler import QueryHandler
from art.framework.core.patterns.mediator.middleware.handlers.request_handler import RequestHandler
from art.framework.core.patterns.mediator.middleware.interceptors.command_interceptor import CommandInterceptor
from art.framework.core.patterns.mediator.middleware.interceptors.notification_interceptor import \
    NotificationInterceptor
from art.framework.core.patterns.mediator.middleware.interceptors.query_interceptor import QueryInterceptor
from art.framework.core.patterns.mediator.middleware.interceptors.request_interceptor import RequestInterceptor
from art.framework.core.patterns.mediator.middleware.middleware_pipeline import MiddlewarePipeline
from art.framework.core.result.result import Result


class TestCommand(Command):
    def name(self):  # noqa
        return __class__.__qualname__


class TestNotification(Notification):
    def name(self):  # noqa
        return __class__.__qualname__


class TestQuery(Query):
    def name(self):  # noqa
        return __class__.__qualname__


class TestRequest(Request):
    def name(self):  # noqa
        return __class__.__qualname__


class TestCommandHandler(CommandHandler):
    def handle(self, context, next_handler=None):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        if next_handler is not None:
            return next_handler(context)
        return Result(data=context.request.name())

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        if next_handler is not None:
            return await next_handler(context)
        return Result(data=context.request.name())


class TestCommandInterceptor(CommandInterceptor):
    def intercept(self, context):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        return Result(data=context.request.name())


class TestNotificationHandler(NotificationHandler):
    def handle(self, context, next_handler=None):
        assert type(context.request) is Notification, f"Invalid argument type {context.request}, Notification is expected."  # noqa
        if next_handler is not None:
            return next_handler(context)
        return Result(data=context.request.name())

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Notification, f"Invalid argument type {context.request}, Notification is expected."  # noqa
        if next_handler is not None:
            return await next_handler(context)
        return Result(data=context.request.name())


class TestNotificationInterceptor(NotificationInterceptor):
    def intercept(self, context):
        assert type(context.request) is Notification, f"Invalid argument type {context.request}, Notification is expected."  # noqa
        return Result(data=context.request.name())

    async def intercept_async(self, context, next_handler=None):
        assert type(context.request) is Notification, f"Invalid argument type {context.request}, Notification is expected."  # noqa
        return Result(data=context.request.name())


class TestQueryHandler(QueryHandler):
    def handle(self, context, next_handler=None):
        assert type(context.request) is Query, f"Invalid argument type {context.request}, Query is expected."
        if next_handler is not None:
            return next_handler(context)
        return Result(data=context.request.name())

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Query, f"Invalid argument type {context.request}, Query is expected."
        if next_handler is not None:
            return await next_handler(context)
        return Result(data=context.request.name())


class TestQueryInterceptor(QueryInterceptor):
    def intercept(self, context):
        assert type(context.request) is Query, f"Invalid argument type {context.request}, Query is expected."
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is Query, f"Invalid argument type {context.request}, Query is expected."
        return Result(data=context.request.name())


class TestRequestHandler(RequestHandler):
    def handle(self, context, next_handler=None):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        if next_handler is not None:
            return next_handler(context)
        return Result(data=context.request.name())

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        if next_handler is not None:
            return await next_handler(context)
        return Result(data=context.request.name())


class TestRequestInterceptor(RequestInterceptor):
    def intercept(self, context):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())


class Test(unittest.TestCase):
    @staticmethod
    def build_pipeline():
        pipeline = MiddlewarePipeline()
        return pipeline

    def test_mediator(self):
        configuration = Configuration()
        logger = Logger()

        commands_registry = None,
        notifications_registry = None,
        queries_registry = None,
        requests_registry = None,
        notification_publisher = None

        mediator = Mediator(configuration, logger)
        assert True


if __name__ == '__main__':
    """
    """
    unittest.main()
