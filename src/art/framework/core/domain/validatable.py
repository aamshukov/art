#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Validatable interface """
from abc import abstractmethod
from art.framework.core.domain.base import Base


class Validatable(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)
