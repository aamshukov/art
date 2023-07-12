#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" IR symbol factory """
from art.framework.core.base import Base
from art.framework.core.flags import Flags
from art.framework.frontend.symtable.symbol import Symbol


class SymbolFactory(Base):
    """
    """
    id_generator = 0

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def get_next_id():
        """
        """
        SymbolFactory.id_generator += 1
        return SymbolFactory.id_generator

    @staticmethod
    def create(label='',
               flags=Flags.CLEAR,
               version='1.0'):
        """
        """
        return Symbol(SymbolFactory.get_next_id(),
                      label=label,
                      flags=flags,
                      version=version)
