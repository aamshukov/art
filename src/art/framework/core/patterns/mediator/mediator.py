#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator interface """
from abc import abstractmethod
from art.framework.core.patterns.mediator.publisher import Publisher
from art.framework.core.patterns.mediator.sender import Sender


class Mediator(Sender, Publisher):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @abstractmethod
    def process(self, *args, **kwargs):
        """
        """
        raise NotImplemented(self.process.__qualname__)
