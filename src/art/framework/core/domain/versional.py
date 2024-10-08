#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Versional interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Versional(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def version(self):
        """
        """
        raise NotImplemented(self.version.__qualname__)
