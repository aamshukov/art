#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art enum member declaration """
from art.framework.core.domain.value import Value


class ArtEnumMemberDecl(Value):
    """
    """
    def __init__(self,
                 label,
                 value,
                 version='1.0'):
        """
        """
        super().__init__(value=value, version=version)
        self.label = label

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.label))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and self.label == other.label)
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
        return f"{super().stringify()}:{self.label}"
