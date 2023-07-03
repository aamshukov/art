# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context Free Grammar algorithms """
from art.framework.core.base import Base


class GrammarAlgorithms(Base):
    """
    Context Free Grammar algorithms.
    """
    def __init__(self):
        """
        """
        pass

    @staticmethod
    def collect_non_terminals(grammar):
        """
        """
        return [symbol for symbol in grammar.pool.values() if symbol.non_terminal]

    @staticmethod
    def collect_terminals(grammar):
        """
        """
        return [symbol for symbol in grammar.pool.values() if symbol.terminal]

    @staticmethod
    def collect_nullable(grammar):
        """
        """
        return [symbol for symbol in grammar.pool.values() if symbol.nullable]

    @staticmethod
    def build_nullability_set(grammar):
        """
        """