#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Semantic analyzer """
from art.framework.core.domain.base import Base


class Semantics(Base):
    """
    """
    def __init__(self,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__()
        self.statistics = statistics
        self.diagnostics = diagnostics

    def analyze_enum_decl(self, decl):
        """
        """
        pass
