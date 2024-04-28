#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Diagnostics """
from art.framework.core.diagnostics.code import Code
from art.framework.core.domain.base import Base
from art.framework.core.diagnostics.status import Status


class Diagnostics(Base):
    """
    """
    def __init__(self, spurious_errors=128):
        """
        """
        super().__init__()
        self.statuses = list()  # list of Status objects
        self.spurious_errors = spurious_errors  # how many spurious error before termination

    @property
    def status(self):
        """
        """
        return not self.errors and not self.fatal_errors

    @property
    def successes(self):
        """
        """
        return [status for status in self.statuses
                if not (status.custom_code & Code.INFORMATION_MASK) == Code.INFORMATION_MASK and
                not (status.custom_code & Code.WARNING_MASK) == Code.WARNING_MASK and
                not (status.custom_code & Code.ERROR_MASK) == Code.ERROR_MASK and
                not (status.custom_code & Code.FATAL_ERROR_MASK) == Code.FATAL_ERROR_MASK]

    @property
    def infos(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Code.INFORMATION_MASK) == Code.INFORMATION_MASK]

    @property
    def warnings(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Code.WARNING_MASK) == Code.WARNING_MASK]

    @property
    def errors(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Code.ERROR_MASK) == Code.ERROR_MASK]

    @property
    def fatal_errors(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Code.FATAL_ERROR_MASK) == Code.FATAL_ERROR_MASK]

    @property
    def last_status(self):
        """
        """
        if self.statuses:
            return self.statuses[-1]
        else:
            return Status(messages=Diagnostics.__name__, origin=Diagnostics.__name__)

    def add(self, status):
        """
        """
        if len(self.statuses) < self.spurious_errors:
            self.statuses.append(status)
