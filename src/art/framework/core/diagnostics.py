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
        self._state = True  # quick state check, true - valid (continue), false - erroneous
        self._statuses = list()  # list of Status objects
        self._spurious_errors = spurious_errors  # how many spurious error before termination

    @property
    def state(self):
        """
        """
        return self._state

    @property
    def successes(self):
        """
        """
        return [status for status in self._statuses
                if not (status.custom_code & Status.INFO_MASK) == Status.INFO_MASK and
                not (status.custom_code & Status.WARNING_MASK) == Status.WARNING_MASK and
                not (status.custom_code & Status.ERROR_MASK) == Status.ERROR_MASK and
                not (status.custom_code & Status.FATAL_ERROR_MASK) == Status.FATAL_ERROR_MASK]

    @property
    def infos(self):
        """
        """
        return [status for status in self._statuses
                if (status.custom_code & Status.INFO_MASK) == Status.INFO_MASK]

    @property
    def warnings(self):
        """
        """
        return [status for status in self._statuses
                if (status.custom_code & Status.WARNING_MASK) == Status.WARNING_MASK]

    @property
    def errors(self):
        """
        """
        return [status for status in self._statuses
                if (status.custom_code & Status.ERROR_MASK) == Status.ERROR_MASK]

    @property
    def fatal_errors(self):
        """
        """
        return [status for status in self._statuses
                if (status.custom_code & Status.FATAL_ERROR_MASK) == Status.FATAL_ERROR_MASK]

    @property
    def statuses(self):
        """
        """
        return self._statuses

    @property
    def last_status(self):
        """
        """
        if self._statuses:
            return self._statuses[-1]
        else:
            return Status(Diagnostics.__name__, Diagnostics.__name__)

    def add(self, status):
        """
        """
        if len(self._statuses) < self._spurious_errors:
            self._statuses.append(status)
