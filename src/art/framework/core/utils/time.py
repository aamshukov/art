#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Time """
import datetime as dt
from dateutil.tz import gettz
from art.framework.core.domain.base import Base


class Time(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.tz_name = dt.datetime.now(dt.timezone.utc).astimezone().tzname()
        self.tz_info = gettz(self.tz_name)

    @staticmethod
    def timestamp():
        """
        """
        return dt.datetime.now(dt.timezone.utc).timestamp()

    @staticmethod
    def from_timestamp(timestamp):
        """
        """
        return dt.datetime.fromtimestamp(timestamp, tz=dt.timezone.utc)

    def now(self, local=True, tz=None):
        """
        """
        timezone = dt.timezone.utc
        if local:
            timezone = self.tz_info
        else:
            if tz is not None:
                timezone = gettz(tz)
        return dt.datetime.now(tz=timezone).isoformat()
