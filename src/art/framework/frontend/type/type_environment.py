#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Type environment """
from art.framework.core.domain.base import Base


class TypeEnvironment(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.env = dict()  # mapping of variable names and their inferred type (variable names to inferred type)
