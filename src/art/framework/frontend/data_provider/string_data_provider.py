#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" String data provider """
from art.framework.frontend.data_provider.data_provider import DataProvider


class StringDataProvider(DataProvider):
    """
    """
    def __init__(self, data, raw_bytes=False):
        """
        """
        assert data is not None, "Invalid argument 'data'"
        if raw_bytes:
            self._data = data.decode('UTF-8')
        else:
            self._data = data

    def load(self):
        """
        """
        return self._data
