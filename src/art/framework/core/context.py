#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context """
from art.framework.core.base import Base
from art.framework.core.status import Status


class Context(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self._status = Status('Context initialization', 'context')

    @property
    def status(self):
        """
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        """
        self._status = status
