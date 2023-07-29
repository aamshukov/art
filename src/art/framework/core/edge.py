#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Edge """
from art.framework.core.domain_helper import DomainHelper
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
        super().__init__(id, value, attributes, flags, version)
        self.endpoints = [endpoint for endpoint in endpoints]

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self.id}:{self.value}:" \
               f"({DomainHelper.dict_to_string(self.attributes)}):{self.endpoints}:{self.version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        return super().__hash__()

    def __eq__(self, other):
        """
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        """
        return super().__le__(other)

    @property
    def uv(self):
        """
        """
        return self.endpoints[0], self.endpoints[1]

    def validate(self):
        """
        """
        return True
