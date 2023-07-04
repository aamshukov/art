# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context Free Grammar algorithms """
from art.framework.core.base import Base
from art.framework.core.text import Text


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
        The set of nullable non-terminals can be computed by the following algorithm:
          (a) Set "nullable" equal to the set of non-terminals appearing on the left side
              of productions of the form N -> e
          (b) Until doing so adds no new non-terminals to "nullable", examine each production
              in the grammar adding to "nullable" all left-hand-sides of productions whose
              right-hand-side consist entirely of symbols in "nullable"
         +
         Sudkamp, 3rd edition, p.108
        """
        non_terminals = GrammarAlgorithms.collect_non_terminals(grammar)
        # init NULL
        # NULL = { A | A -> λ ∈ P }
        nullables = set()
        for rule in grammar.rules:
            if rule.empty():
                rule.lhs.nullable = True
                nullables.add(rule.lhs)
        # calculate
        prev_nullables = set()
        while True:
            for non_terminal in non_terminals:
                for rule in grammar.rules:
                    if Text.equal(rule.lhs.name, non_terminal.name):
                        # w ∈ PREV* - all symbols in w either nullable or λ
                        nullable = True
                        for symbol in rule.rhs:
                            if not (symbol.non_terminal and symbol in prev_nullables):
                                nullable = False
                                break
                        if nullable:
                            # NULL = NULL ∪ { A }
                            rule.lhs.nullable = True
                            nullables.add(rule.lhs)
                            break
            if nullables == prev_nullables:
                break
            prev_nullables = nullables.copy()
        return nullables
