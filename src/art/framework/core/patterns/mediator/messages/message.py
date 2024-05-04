#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator message interface """
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.time import Time


class Message(Entity):
    """
    """
    def __init__(self,
                 correlation_id,
                 version='1.0'):
        """
        """
        super().__init__(correlation_id, version)
        self.timestamp = Time.timestamp()

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

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}"
