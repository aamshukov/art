#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification publisher interface """
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper
from art.framework.core.patterns.mediator.publishers.notification_publisher import NotificationPublisher


class SequentialNotificationPublisher(NotificationPublisher):
    """
    """
    def __init__(self, configuration, logger):
        """
        """
        super().__init__(configuration, logger)

    @MediatorDomainHelper.traceable()
    def publish(self, context, bindings):
        """
        """
        return MediatorDomainHelper.send(context, bindings)

    @MediatorDomainHelper.traceable_async()
    async def publish_async(self, context, bindings):
        """
        """
        return await MediatorDomainHelper.send_async(context, bindings)
