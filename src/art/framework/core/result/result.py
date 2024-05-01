#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Result """
from art.framework.core.diagnostics.code import Code
from art.framework.core.diagnostics.status import Status
from art.framework.core.domain.base import Base


class Result(Base):
    """
    """

    def __init__(self, status=None, data=None):
        """
        """
        super().__init__()
        self.status = status if status is not None else Status()
        self.data = data

    def success(self):
        """
        """
        return self.status.custom_code == Code.Success
