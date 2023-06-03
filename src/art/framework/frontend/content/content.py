#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Content """
from art.framework.core.base import Base


class Content(Base):
    """
    """

    def __init__(self, data, source):
        """
        """
        self._data = data
        self._count = len(data)
        self._source = source

    @property
    def data(self):
        """
        """
        return self._data

    @property
    def count(self):
        """
        """
        return self._count

    @property
    def source(self):
        """
        """
        return self._source
