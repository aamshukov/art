#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type substitution """
from art.framework.core.domain.base import Base


class TypeSubstitution(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.substitution = dict()  # mapping of type variables to types
