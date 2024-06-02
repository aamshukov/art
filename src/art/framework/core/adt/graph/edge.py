#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from art.framework.core.utils.flags import Flags
from art.framework.core.domain.entity import Entity


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
        super().__init__(id, value, attributes, flags, version)
        self.endpoints = [endpoint for endpoint in endpoints]

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__lt__(other)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__le__(other)
        else:
            result = NotImplemented
        return result

    @property
    def uv(self):
        """
        """
        return self.endpoints[0], self.endpoints[1]

    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)

    def stringify(self):
        """
        """
        return f"{self.endpoints}:{self.value}:{super().stringify()}"

