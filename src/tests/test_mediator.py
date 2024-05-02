#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest

from art.framework.core.configuration.configuration import Configuration
from art.framework.core.logging.logger import Logger
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper
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
from art.framework.core.patterns.mediator.middleware.middleware import Middleware
from art.framework.core.patterns.mediator.middleware.middleware_pipeline import MiddlewarePipeline
from art.framework.core.patterns.mediator.publishers.sequential_notification_publisher import \
    SequentialNotificationPublisher
from art.framework.core.result.result import Result


class TestCommand1(Command):
    def __init__(self,):
        super().__init__(correlation_id='1')

    def name(self):  # noqa
        return str(self)


class TestCommand2(Command):
    def __init__(self,):
        super().__init__(correlation_id='2')

    def name(self):  # noqa
        return str(self)


class TestNotification(Notification):
    def __init__(self,):
        super().__init__(correlation_id='3')

    def name(self):  # noqa
        return str(self)


class TestQuery(Query):
    def __init__(self,):
        super().__init__(correlation_id='5')

    def name(self):  # noqa
        return str(self)


class TestRequest1(Request):
    def __init__(self,):
        super().__init__(correlation_id='7')

    def name(self):  # noqa
        return str(self)


class TestRequest2(Request):
    def __init__(self,):
        super().__init__(correlation_id='8')

    def name(self):  # noqa
        return str(self)


class TestCommand11Handler(CommandHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    @MediatorDomainHelper.traceable()
    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = next_handler(context)
        return result

    @MediatorDomainHelper.traceable_async()
    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestCommand12Handler(CommandHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestCommand11Interceptor(CommandInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")

    async def intercept_async(self, context):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")


class TestCommand12Interceptor(CommandInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")

    async def intercept_async(self, context):
        assert isinstance(context.request, TestCommand1), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")


class TestCommand21Handler(CommandHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestCommand22Handler(CommandHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        result = Result(data=f"Handler: {context.request.name()}")
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestCommand21Interceptor(CommandInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")

    async def intercept_async(self, context):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")


class TestCommand22Interceptor(CommandInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")

    async def intercept_async(self, context):
        assert isinstance(context.request, TestCommand2), f"Invalid argument type {context.request}, Command is expected."  # noqa
        return Result(data=f"Interceptor: {__class__} {context.request.name()}")


class TestNotificationHandler(NotificationHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestNotification), f"Invalid argument type {context.request}, Notification is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestNotification), f"Invalid argument type {context.request}, Notification is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestNotificationInterceptor(NotificationInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestNotification), f"Invalid argument type {context.request}, Notification is expected."  # noqa
        return Result(data=context.request.name())

    async def intercept_async(self, context, next_handler=None):
        assert isinstance(context.request, TestNotification), f"Invalid argument type {context.request}, Notification is expected."  # noqa
        return Result(data=context.request.name())


class TestQueryHandler(QueryHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestQuery), f"Invalid argument type {context.request}, Query is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestQuery), f"Invalid argument type {context.request}, Query is expected."
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestQueryInterceptor(QueryInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestQuery), f"Invalid argument type {context.request}, Query is expected."
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert isinstance(context.request, TestQuery), f"Invalid argument type {context.request}, Query is expected."
        return Result(data=context.request.name())


class TestRequest1Handler(RequestHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestRequest1), f"Invalid argument type {context.request}, Request is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestRequest1), f"Invalid argument type {context.request}, Request is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestRequest2Handler(RequestHandler):
    def __init__(self, configuration, logger):
        super().__init__(configuration, logger)

    def handle(self, context, next_handler=None):
        assert isinstance(context.request, TestRequest2), f"Invalid argument type {context.request}, Request is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = next_handler(context)
        return result

    async def handle_async(self, context, next_handler=None):
        assert isinstance(context.request, TestRequest2), f"Invalid argument type {context.request}, Request is expected."  # noqa
        result = Result(data=context.request.name())
        if next_handler is not None:
            result = await next_handler(context)
        return result


class TestRequest1Interceptor(RequestInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestRequest1), f"Invalid argument type {context.request}, Request is expected."  # noqa
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is TestRequest1, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())


class TestRequest2Interceptor(RequestInterceptor):
    def intercept(self, context):
        assert isinstance(context.request, TestRequest2), f"Invalid argument type {context.request}, Request is expected."  # noqa
        return Result(data=context.request.name())

    async def intercept_async(self, context):
        assert type(context.request) is TestRequest2, f"Invalid argument type {context.request}, Request is expected."
        return Result(data=context.request.name())


class Test(unittest.IsolatedAsyncioTestCase):
    @staticmethod
    def build_command_pipeline(configuration, logger):
        pipeline = MiddlewarePipeline()
        middleware = Middleware(configuration, logger, TestCommand11Handler, [TestCommand11Interceptor, TestCommand12Interceptor])  # noqa
        pipeline.register_command(TestCommand1, middleware)
        middleware = Middleware(configuration, logger, TestCommand12Handler, [TestCommand11Interceptor, TestCommand12Interceptor])  # noqa
        pipeline.register_command(TestCommand1, middleware)
        middleware = Middleware(configuration, logger, TestCommand21Handler, [TestCommand21Interceptor, TestCommand22Interceptor])  # noqa
        pipeline.register_command(TestCommand2, middleware)
        middleware = Middleware(configuration, logger, TestCommand21Handler, [TestCommand21Interceptor, TestCommand22Interceptor])  # noqa
        pipeline.register_command(TestCommand2, middleware)
        return pipeline

    @staticmethod
    def build_notification_pipeline(configuration, logger):
        pipeline = MiddlewarePipeline()
        middleware = Middleware(configuration, logger, TestNotificationHandler, [TestNotificationInterceptor])
        pipeline.register_notification(TestNotification, middleware)
        return pipeline

    @staticmethod
    def build_query_pipeline(configuration, logger):
        pipeline = MiddlewarePipeline()
        middleware = Middleware(configuration, logger, TestQueryHandler, [TestQueryInterceptor])
        pipeline.register_query(TestQuery, middleware)
        return pipeline

    @staticmethod
    def build_request_pipeline(configuration, logger):
        pipeline = MiddlewarePipeline()
        middleware = Middleware(configuration, logger, TestRequest1Handler, [TestRequest1Interceptor, TestRequest1Interceptor])  # noqa
        pipeline.register_request(TestRequest1, middleware)
        middleware = Middleware(configuration, logger, TestRequest1Handler, [TestRequest1Interceptor, TestRequest1Interceptor])  # noqa
        pipeline.register_request(TestRequest1, middleware)
        middleware = Middleware(configuration, logger, TestRequest2Handler, [TestRequest2Interceptor, TestRequest2Interceptor])  # noqa
        pipeline.register_request(TestRequest2, middleware)
        middleware = Middleware(configuration, logger, TestRequest2Handler, [TestRequest2Interceptor, TestRequest2Interceptor])  # noqa
        pipeline.register_request(TestRequest2, middleware)
        return pipeline

    @staticmethod
    def build_mediator():
        configuration = Configuration()
        logger = Logger()
        command_pipeline = Test.build_command_pipeline(configuration, logger)
        notification_pipeline = Test.build_notification_pipeline(configuration, logger)
        query_pipeline = Test.build_query_pipeline(configuration, logger)
        request_pipeline = Test.build_request_pipeline(configuration, logger)
        notification_publisher = SequentialNotificationPublisher(configuration, logger)
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
        result = mediator.send_command(TestCommand1())
        assert result.success()
        result = mediator.send_command(TestCommand2())
        assert result.success()
        result = mediator.publish(TestNotification())
        assert result.success()
        result = mediator.send_query(TestQuery())
        assert result.success()
        result = mediator.send_request(TestRequest1())
        assert result.success()
        result = mediator.send_request(TestRequest2())
        assert result.success()

    async def test_mediator_async(self):
        mediator = Test.build_mediator()
        result = await mediator.send_command_async(TestCommand1())
        assert result.success()
        result = await mediator.send_command_async(TestCommand2())
        assert result.success()
        result = await mediator.publish_async(TestNotification())
        assert result.success()
        result = await mediator.send_query_async(TestQuery())
        assert result.success()
        result = await mediator.send_request_async(TestRequest1())
        assert result.success()
        result = await mediator.send_request_async(TestRequest2())
        assert result.success()


if __name__ == '__main__':
    """
    """
    unittest.main()
