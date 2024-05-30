#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Versional interface """
from art.framework.core.domain.base import Base


class Versional(Base):
    """
    """
    def __init__(self, version='1.0'):
        """
        """
        super().__init__()
        self.version = version.strip()
