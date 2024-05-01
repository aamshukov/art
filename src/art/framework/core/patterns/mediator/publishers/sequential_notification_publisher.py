#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification publisher interface """
from art.framework.core.patterns.mediator.helpers.helpers import MediatorDomainHelper
from art.framework.core.patterns.mediator.publishers.notification_publisher import NotificationPublisher
from art.framework.core.utils.helper import traceable


class SequentialNotificationPublisher(NotificationPublisher):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @traceable("Mediator sequential publisher: publish")
    def publish(self, context, bindings):
        """
        """
        return MediatorDomainHelper.send(context, bindings)

    @traceable("Mediator sequential publisher: publish")
    async def publish_async (self, context, bindings):
        """
        """
        return await MediatorDomainHelper.send_async(context, bindings)
