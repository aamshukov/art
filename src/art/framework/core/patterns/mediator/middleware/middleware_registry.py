#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Mediator bindings registry """
from art.framework.core.domain.base import Base


class MiddlewareRegistry(Base):
    """
    """
    def __init__(self, registry=None):
        """
        """
        super().__init__()
        self.registry = registry if registry is not None else list()  # set of bindings

    def get_bindings(self, message):
        """
        """
        bindings = list()
        message_type = type(message)
        for binding in self.registry:
            if type(binding.message) is message_type:
                bindings.append(binding)
        return bindings

    def register_binding(self, new_binding):
        """
        """
        message_type = type(new_binding.message)
        for binding in self.registry:
            if type(binding.message) is message_type:
                break
        else:
            self.registry.append(new_binding)
