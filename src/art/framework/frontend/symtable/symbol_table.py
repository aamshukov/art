#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Symbol table """
from art.framework.core.base import Base


class SymbolTable(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.scopes = None  # root of scope tree, might represent 'global' scope
        self.scope = None   # current scope, level
