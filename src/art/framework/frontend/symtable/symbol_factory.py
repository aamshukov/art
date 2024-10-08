#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" IR symbol factory """
from copy import deepcopy
from art.framework.core.domain.base import Base
from art.framework.core.utils.flags import Flags
from art.framework.frontend.symtable.symbol import Symbol
from art.framework.frontend.symtable.symbol_kind import SymbolKind


class SymbolFactory(Base):
    """
    """
    id_generator = 0

    UNKNOWN_SYMBOL = Symbol(id_generator, SymbolKind.UNKNOWN.name)

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def get_next_uid():
        """
        """
        SymbolFactory.id_generator += 1
        return SymbolFactory.id_generator

    @staticmethod
    def create(label='',
               value=None,
               attributes=None,
               flags=Flags.CLEAR,
               version='1.0'):
        """
        """
        return Symbol(SymbolFactory.get_next_uid(),
                      label,
                      value,
                      attributes,
                      flags,
                      version)

    @staticmethod
    def unknown_symbol():
        """
        """
        return deepcopy(SymbolFactory.UNKNOWN_SYMBOL)
