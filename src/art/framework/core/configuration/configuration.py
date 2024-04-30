#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Configuration """
from art.framework.core.domain.base import Base


class Configuration(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.settings = dict()
