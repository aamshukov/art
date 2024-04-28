#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator notification publisher interface """
from art.framework.core.patterns.mediator.publishers.notification_publisher import NotificationPublisher
from art.framework.core.utils.helper import traceable


class SequentialPublisher(NotificationPublisher):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @traceable("Mediator sequential publisher: publish")
    def publish(self,
                handlers,  # notification handlers
                notification):
        """
        """
        result = list()
        for handler in handlers:
            result.append(handler.handle(notification))
        return result
