#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from art.framework.core.flags import Flags
from art.framework.core.entity import Entity


class Edge(Entity):
    """
    """
    def __init__(self,
                 id,
                 endpoints,
                 value=None,        # edge specific value, might be weight, etc.
                 attributes=None,   # edge specific attributes
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._endpoints = [endpoint for endpoint in endpoints]
        self._value = value
        self._attributes = attributes
        self._flags = flags

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._id}:{self._value}:{self._flags}:{self._version}" \
               f"[{self._attributes}]:({self._endpoints})"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  tuple(self._endpoints) == tuple(other.endpoints) and
                  self._value == other.value)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._value < other.value)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._value <= other.value)
        return result

    @property
    def endpoints(self):
        """
        """
        return self._endpoints

    @property
    def uv(self):
        """
        """
        return self._endpoints[0], self._endpoints[1]

    @property
    def value(self):
        """
        """
        return self._value

    @value.setter
    def value(self, value):
        """
        """
        self._value = value

    @property
    def attributes(self):
        """
        """
        return self._attributes

    @attributes.setter
    def attributes(self, attributes):
        """
        """
        self._attributes = attributes

    @property
    def flags(self):
        """
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        """
        self._flags = flags

    def validate(self):
        """
        """
        return True
