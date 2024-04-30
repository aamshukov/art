#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator context """
from art.framework.core.domain.value import Value


class Context(Value):
    """
    """
    def __init__(self,
                 request=None,
                 response=None,
                 version='1.0'):
        """
        """
        super().__init__(version=version)
        self.request = request
        self.response = response
        self.results = list()  # aggregated list of Result(s)

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
