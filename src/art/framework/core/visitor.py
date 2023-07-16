#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Visitor design pattern """
from abc import abstractmethod
from art.framework.core.base import Base


class Visitor(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def visit(self, visitable, *args, **kwargs):
        """
        """
        raise NotImplemented(self.visit.__qualname__)
