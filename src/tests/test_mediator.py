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
from art.framework.core.patterns.mediator.publishers.sequential_notification_publisher import \
    SequentialNotificationPublisher
from art.framework.core.result.result import Result


class TestCommand1(Command):
    def __init__(self,):
        super().__init__(correlation_id='1')

    def name(self):  # noqa
        return __class__.__qualname__


class TestCommand2(Command):
    def __init__(self,):
        super().__init__(correlation_id='2')

    def name(self):  # noqa
        return __class__.__qualname__


class TestNotification1(Notification):
    def __init__(self,):
        super().__init__(correlation_id='3')

    def name(self):  # noqa
        return __class__.__qualname__


class TestNotification2(Notification):
    def __init__(self,):
        super().__init__(correlation_id='4')

    def name(self):  # noqa
        return __class__.__qualname__


class TestQuery1(Query):
    def __init__(self,):
        super().__init__(correlation_id='5')

    def name(self):  # noqa
        return __class__.__qualname__


class TestQuery2(Query):
    def __init__(self,):
        super().__init__(correlation_id='6')

    def name(self):  # noqa
        return __class__.__qualname__


class TestRequest1(Request):
    def __init__(self,):
        super().__init__(correlation_id='7')

    def name(self):  # noqa
        return __class__.__qualname__


class TestRequest2(Request):
    def __init__(self,):
        super().__init__(correlation_id='8')

    def name(self):  # noqa
        return __class__.__qualname__


class TestCommandHandler(CommandHandler):
    def handle(self, context, next_handler=None):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Command, f"Invalid argument type {context.request}, Command is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


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
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Notification, f"Invalid argument type {context.request}, Notification is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


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
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Query, f"Invalid argument type {context.request}, Query is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


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
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestRequestInterceptor(RequestInterceptor):
    def intercept(self, context):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is Request, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())


class Test(unittest.TestCase):
    @staticmethod
    def build_command_pipeline():
        pipeline = MiddlewarePipeline()
        return pipeline

    @staticmethod
    def build_notification_pipeline():
        pipeline = MiddlewarePipeline()
        return pipeline

    @staticmethod
    def build_query_pipeline():
        pipeline = MiddlewarePipeline()
        return pipeline

    @staticmethod
    def build_request_pipeline():
        pipeline = MiddlewarePipeline()
        return pipeline

    @staticmethod
    def build_mediator():
        configuration = Configuration()
        logger = Logger()
        command_pipeline = Test.build_command_pipeline()
        notification_pipeline = Test.build_notification_pipeline()
        query_pipeline = Test.build_query_pipeline()
        request_pipeline = Test.build_request_pipeline()
        notification_publisher = SequentialNotificationPublisher()
        mediator = Mediator(configuration,
                            logger,
                            command_pipeline,
                            notification_pipeline,
                            query_pipeline,
                            request_pipeline,
                            notification_publisher)
        return mediator

    def test_mediator(self):
        mediator = Test.build_mediator()
        # result = mediator.send_command(TestCommand1())
        # assert result.success()


if __name__ == '__main__':
    """
    """
    unittest.main()
