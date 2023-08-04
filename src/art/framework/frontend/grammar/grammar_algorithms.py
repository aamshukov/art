# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context Free Grammar algorithms """
import itertools
from art.framework.core.base import Base
from art.framework.core.text import Text


class GrammarAlgorithms(Base):
    """
    Context Free Grammar algorithms.
    """
    def __init__(self):
        """
        """
        super().__init__()

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

    @staticmethod
    def truncate(grammar, sets, k):
        """
        Operator ⊕:
            F`1(A) ⊕k F`2(A) ... ⊕k ... F`N(A)

        L1 ⊕k L2
        L1 = { λ, abb }
        L2 = { b, bab }
        L1 ⊕2 L2 = { b, ba, ab }
        AU: p.348

        L1 = { ∅ }
        L2 = { b, bab }
        L1 ⊕2 L2 = { ∅ }

        L1 = { λ }
        L2 = { λ, λ }
        L1 ⊕2 L2 = { λ }

        Sudkamp 2nd ed. p. 499, 3rd ed. p. 575
        TRUNC3( {a, b, λ} {a} {b} {d} {λ} ) = TRUNC3( { aabd, babd, abd} ) = { aab, bab, abd }
        """
        result = list()
        flattened_sets = list(itertools.chain(*sets))
        if any(not s for s in flattened_sets):  # u ∅ = ∅ u = ∅
            if all(not s for s in flattened_sets):  # special case ∅* = λ
                result.append([grammar.epsilon])
        else:
            for product in itertools.product(*sets):  # calculate cartesian product
                n = 0
                line = list()
                for symbols in product:
                    for symbol in symbols:
                        assert symbol.terminal or symbol.epsilon, f"Symbol {symbol.name} must be TERMINAl or EPSILON."
                        line.append(symbol)
                        if symbol.terminal:
                            n += 1
                        if n == k:
                            break
                    else:
                        continue
                    break
                # adjusting lambdas (λs):
                #   if all λs -> λ* = λ, keep { λ λ...} as { λ }
                #   other way remove λs
                if all(s.epsilon for s in line):
                    line = line[:1]
                else:
                    line = list(filter(lambda s: not s.epsilon, line))
                if line not in result:
                    result.append(line)
        return result

    @staticmethod
    def compare_lists(list1, list2):
        result = len(list1) == len(list2)
        if result:
            for element in list1:
                if element not in list2:
                    result = False
                    break
        return result

    @staticmethod
    def make_list_unique(lst):
        """
        """
        return [[*x] for x in set(tuple(x) for x in lst)]

    @staticmethod
    def cleanup_lists(lists):
        """
        """
        return [lst for lst in lists if lst]

    @staticmethod
    def union_lists(lst1, lst2):
        """
        Union lists and removes empty ones.
        """
        result = GrammarAlgorithms.make_list_unique(lst1 + lst2)
        result = GrammarAlgorithms.cleanup_lists(result)
        return result

    @staticmethod
    def build_first_set(grammar, k=1):
        """
        Calculate FIRST(k) set.
        Based on AU, Russian edition, page 397 and on Sudkamp p. 498
         1. for each a ∈ T do F`(a) = {a}
         2. for each A ∈ N do F(A) = {λ} if A is nullable or empty otherwise
         3. repeat
             3.1 for each A ∈ N do F`(A) = F(A)
             3.2 for each rule A -> u1 u2 ... uN with n > 0 do
                 F(A) = F(A) ∪ TRUNCk(F`(u1) F`(u2) ... F`(uN))
            until F(A) = F`(A) for all A ∈ N
         4. FIRSTk(A) = F(A)

        FIRST set is list of lists for every non-terminal in grammar, size of "lists" is up to K
           ( )
            | \
            |   ---
            |      |
        (0,1..K) (0,1..K)

        ... recall that concatenation of empty set ∅ with any set yields empty set ∅:
             u ∅ = ∅ u = ∅
        but union does not:
             u ∪ ∅ = ∅ ∪ u = u
        """
        assert k > 0, "The k must be greater than zero."
        fs = dict()  # F name:list[a,bc,bb]
        fs_prime = dict()  # F` name:list[a,bc,bb]
        terminals = GrammarAlgorithms.collect_terminals(grammar)
        non_terminals = GrammarAlgorithms.collect_non_terminals(grammar)
        for terminal in terminals:
            terminal.first.clear()
        for non_terminal in non_terminals:
            non_terminal.first.clear()
        for terminal in terminals:  # for each a ∈ T do F`(a) = {a}
            fs_prime[terminal] = [[terminal]]
        for non_terminal in non_terminals:  # for each A ∈ N do F(A) = {λ} if A is nullable or empty otherwise
            alias = list()
            fs[non_terminal] = alias
            for rule in non_terminal.rules:
                if rule.empty():
                    alias.append([grammar.epsilon])
        while True:
            for non_terminal in non_terminals:  # for each A ∈ N do ...
                fs_prime[non_terminal] = fs[non_terminal].copy()  # F`(A) = F(A)
            for non_terminal in non_terminals:  # for each A ∈ N do ...
                for rule in non_terminal.rules:  # for each rule A -> u1 u2 ... uN with n > 0 do
                    if rule.empty():
                        continue
                    sets = list()
                    for symbol in rule.rhs:  # F(A) = F(A) ∪ TRUNCk(F`(u1) F`(u2) ... F`(uN))
                        sets.append(fs_prime[symbol])
                    trunc = GrammarAlgorithms.truncate(grammar, sets, k)  # TRUNCk(F`(u1) F`(u2) ... F`(uN))
                    fs[non_terminal] = GrammarAlgorithms.union_lists(fs[non_terminal], trunc)  # F(A) ∪ TRUNCk
            if all(GrammarAlgorithms.compare_lists(fs[non_terminal], fs_prime[non_terminal])
                   for non_terminal in non_terminals):  # until F(A) = F`(A) for all A ∈ N
                break
        for terminal in terminals:  # FIRSTk(a) = F(a)
            terminal.first.extend([[terminal]])
        for non_terminal in non_terminals:  # FIRSTk(A) = F(A)
            non_terminal.first.extend(fs[non_terminal])

    @staticmethod
    def build_follow_set(grammar, k=1):
        """
        Calculate FOLLOW(k) set.
        Sudkamp 2nd ed., p.501 and Ronald C. Backhouse, p.110
         1. FL(S) = {λ}
         2. for each A ∈ N-{S} do FL(A) = ∅
         3. repeat
             3.1 for each A ∈ N do FL'(A) = FL(A)
             3.2 for each rule A -> w = u1 u2 ... uN with w ∉ T* do  (w ∉ T* means at least one non-terminal must be
                                                                      in RHS, if not - skip)
                 3.2.1 L = FL'(A)
                 3.2.2 if uN ∈ N then FL(uN) = FL(uN) ∪ L
                 3.2.3 for i = n-1 to 1 do
                         3.2.3.1 L = TRUNCk(FIRSTk(ui+1) L)
                         3.2.3.2 if ui ∈ N then FL(ui) = FL(ui) ∪ L
                       end for
                 end for
            until FL(A) = FL`(A) for every A ∈ N
         4. FOLLOWk(A) = FL(A)

        FOLLOW set is list of lists for every non-terminal in grammar, size of "lists" is up to K
           ( )
            | \
            |   ---
            |      |
        (0,1..K) (0,1..K)

        ATTENTION:
         this algorithm assumes FIRSTk() are not empty, for some infinite grammars algorithm
         does NOT work correctly!!!
         One of them is:
             S : E + E
             E : E * E
        in this case, FIRSTk(S) and FIRSTk(E) are empty sets and the statement 3.2.3.1
        L = TRUNCk(FIRSTk(ui+1) L) always calculates L as an empty set ∅.
        For k = 1 consider to use alternative implementations
        build_first1_set and build_follow1_set, see C++ implementation.
        """
        assert k > 0, "The k must be greater than zero."
        fls = dict()  # FL name:list[a,bc,bb]
        fls_prime = dict()  # FL` name:list[a,bc,bb]
        fls[grammar.start] = [[grammar.epsilon]]  # FL(S) = {λ}
        non_terminals = GrammarAlgorithms.collect_non_terminals(grammar)
        for non_terminal in non_terminals:
            non_terminal.follow.clear()
        for non_terminal in non_terminals:
            if non_terminal != grammar.start:  # for each A ∈ N-{S} do FL(A) = ∅
                fls[non_terminal] = [[]]
        while True:
            for non_terminal in non_terminals:  # for each A ∈ N do ...
                fls_prime[non_terminal] = fls[non_terminal].copy()  # F`(A) = F(A)
            for rule in grammar.rules:  # for each rule A -> w = u1 u2 ... uN ...
                if all(symbol.terminal for symbol in rule.rhs):  # ... with w ∉ T*
                    continue
                ls = fls_prime[rule.lhs].copy()  # L = FL'(A)
                un = rule.rhs[-1]
                if un.non_terminal:  # if uN ∈ N ...
                    fls[un] = GrammarAlgorithms.union_lists(fls[un], ls)  # ... then FL(uN) = FL(uN) ∪ L
                for i in range(len(rule.rhs) - 1 - 1, -1, -1):  # for i = n-1 to 1 do, -1 as
                    sets = list()                               # starts from 0 and condition is 'n-1'
                    sets.append(rule.rhs[i + 1].first)
                    sets.append(ls)
                    trunc = GrammarAlgorithms.truncate(grammar, sets, k)  # TRUNCk(FIRSTk(ui+1) L)
                    ls = GrammarAlgorithms.make_list_unique(trunc)
                    ui = rule.rhs[i]
                    if ui.non_terminal:  # if ui ∈ N ...
                        fls[ui] = GrammarAlgorithms.union_lists(fls[ui], ls)  # ... then FL(ui) = FL(ui) ∪ L
            if all(GrammarAlgorithms.compare_lists(fls[non_terminal], fls_prime[non_terminal])
                   for non_terminal in non_terminals):  # until FL(A) = FL`(A) for every A ∈ N
                break
        for non_terminal in non_terminals:  # FOLLOWk(A) = FL(A)
            non_terminal.follow.extend(fls[non_terminal])

    @staticmethod
    def build_la_set(grammar, k=1):
        """
        Sudkamp 2nd ed., p.495
        LAk(A) = TRUNCk(FIRSTk(A) ∪ FOLLOWk(A))
        """
        non_terminals = GrammarAlgorithms.collect_non_terminals(grammar)
        for non_terminal in non_terminals:
            sets = list()
            if non_terminal.first:
                sets.append(non_terminal.first)
            if non_terminal.follow:
                sets.append(non_terminal.follow)
            trunc = GrammarAlgorithms.truncate(grammar, sets, k)
            non_terminal.la.clear()
            non_terminal.la.extend(trunc)

    @staticmethod
    def build_la_set_rule(grammar, rule, k=1):
        """
        Sudkamp 2nd ed., p.495
        LAk(A -> w) = TRUNCk(FIRSTk(w) ∪ FOLLOWk(A))
        """
        if rule.empty():  # A -> λ
            result = GrammarAlgorithms.cleanup_lists(rule.lhs.follow)
        else:
            sets = list()
            for symbol in rule.rhs:  # FIRSTk(w) = FIRSTk(u1) (+)k FIRSTk(u2) (+)k ... (+)k FIRSTk(uN)
                sets.append(symbol.first)
            if GrammarAlgorithms.cleanup_lists(rule.lhs.follow):
                sets.append(rule.lhs.follow)
            sets = GrammarAlgorithms.cleanup_lists(sets)
            result = GrammarAlgorithms.truncate(grammar, sets, k)
        if not result:
            result = [[]]
        return result
