#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator query interface """
from art.framework.core.patterns.mediator.messages.message import Message


class Query(Message):
    """
    """
    def __init__(self,
                 correlation_id,
                 version='1.0'):
        """
        """
        super().__init__(correlation_id, version)
