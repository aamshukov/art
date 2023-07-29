#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Diagnostics """
from art.framework.core.base import Base
from art.framework.core.status import Status


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
        return not self.warnings and not self.errors and not self.fatal_errors

    @property
    def successes(self):
        """
        """
        return [status for status in self.statuses
                if not (status.custom_code & Status.INFO_MASK) == Status.INFO_MASK and
                not (status.custom_code & Status.WARNING_MASK) == Status.WARNING_MASK and
                not (status.custom_code & Status.ERROR_MASK) == Status.ERROR_MASK and
                not (status.custom_code & Status.FATAL_ERROR_MASK) == Status.FATAL_ERROR_MASK]

    @property
    def infos(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Status.INFO_MASK) == Status.INFO_MASK]

    @property
    def warnings(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Status.WARNING_MASK) == Status.WARNING_MASK]

    @property
    def errors(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Status.ERROR_MASK) == Status.ERROR_MASK]

    @property
    def fatal_errors(self):
        """
        """
        return [status for status in self.statuses
                if (status.custom_code & Status.FATAL_ERROR_MASK) == Status.FATAL_ERROR_MASK]

    @property
    def last_status(self):
        """
        """
        if self.statuses:
            return self.statuses[-1]
        else:
            return Status(Diagnostics.__name__, Diagnostics.__name__)

    def add(self, status):
        """
        """
        if len(self.statuses) < self.spurious_errors:
            self.statuses.append(status)
