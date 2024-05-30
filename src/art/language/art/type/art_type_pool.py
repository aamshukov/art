#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art types pool """
from art.framework.core.domain.base import Base
from art.framework.core.patterns.singleton.singleton import singleton


@singleton
class ArtTypePool(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.types = dict()  # id:type
        self.build_types()

    def get_type(self, type):  # noqa
        """
        """
        result = None
        for value in self.types.values():
            if value.equivalent(type):
                result = value
                break
        return result
