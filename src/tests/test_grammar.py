#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import os
import unittest
from art.framework.core.logger import Logger
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms


class Test(unittest.TestCase):
    GRAMMAR_PATH = 'd:/tmp/art/'
    GRAMMAR_FILE = '{}/{}.txt'

    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)
        if not os.path.exists(Test.GRAMMAR_PATH):
            os.makedirs(Test.GRAMMAR_PATH)

    def test_grammar_load_success(self):
        schema = """
            expression   : primary_expression
                         | '+' expression
                         | '-' expression
                         | '!' expression
                         | 'not' expression
                         | '++' expression                     # expression evaluates to integer
                         | '--' expression                     # expression evaluates to integer
                         | expression '.' identifier           # member access
                         | expression '[' arguments_opt ']     # array element access
                         | expression '(' arguments_opt ')'    # function invocation
                         | expression '++'                     # expression evaluates to integer
                         | expression '--'                     # expression evaluates to integer
                         ;

            primary_expression : literal                                        # 5, 'text'
                               | fully_qualified_identifier type_arguments_opt  # geo.point<T>, point<real>
                               | '(' expression ')'
                               ;
                               
            type_arguments_opt  : type_arguments
                                | ε
                                | λ
                                ;                               

        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 8
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 10

    def test_build_nullability_set_sudkamp_0_success(self):
        schema = """
            S   : S 'a' B
                | 'a' B
                ;
            B   : 'b' B
                | λ
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 2
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['B']}

    def test_build_nullability_set_sudkamp_4_2_1_success(self):
        schema = """
            S   : A C A
                ;
            A   : 'a' A 'a'
                | B
                | C
                ;
            B   : 'b' B
                | 'b'
                ;
            C   : 'c' C
                | λ
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 3
        assert nullables == {grammar.pool['S'], grammar.pool['A'], grammar.pool['C']}

    def test_build_nullability_set_sudkamp_4_2_3_success(self):
        schema = """
            S   : A B C
                ;
            A   : 'a' A
                | λ
                ;
            B   : 'b' B
                | λ
                ;
            C   : 'c' C
                | λ
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S'], grammar.pool['A'], grammar.pool['B'], grammar.pool['C']}

    def test_build_nullability_set_SWAB_success(self):
        schema = """
            S   : W A B
                | A B C S
                ;
            A   : B 
                | W B
                ;
            B   : ε 
                | 'y' B
                ;
            C   : 'z'
                ;
            W   : 'x'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['B']}

    def test_build_nullability_set_AaAb_success(self):
        schema = """
            S1 : S
               ;
           
            S  | A 'a' A 'b'
               | B 'b' B 'a'
               ;
            
            A  : ε
               ;
            
            B  : ε
               ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 2
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['B']}

    def test_build_nullability_set_aSAAA_success(self):
        schema = """
            S : 'a' S A A A
              | ε
              ;
            A : 'a'
              | ε
              ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['S'], grammar.pool['A']}

    def test_build_nullability_set_bRS_success(self):
        schema = """
            S   : 'b' R S
                | R 'c' S 'a'
                | ε
                ;
            
            R   : 'a' 'c' R
                | 'b'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['S']}

    def test_build_nullability_set_AzA_success(self):
        schema = """
            B   : A 'z' A
                ;
            A   : 'a'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 2
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['A']}

    def test_build_nullability_set_AAAA_success(self):
        schema = """
            S1  : S
                ;
            
            S   : A A A A
                ;
            
            A   : 'a'
                | E
                ;
            
            E   : ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S1'], grammar.pool['S'], grammar.pool['A'], grammar.pool['E']}

    def test_build_nullability_set_LAAAA_success(self):
        schema = """
            A   : 'a' A 'a'
                | L
                ;
            L   : 'a'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['L']}

    def test_build_nullability_set_SAB_success(self):
        schema = """
            S   : A B
                ;
            
            A   : B 'a'
                | ε
                ;
            
            B   : C 'b'
                | C
                ;
            
            C   : 'c'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S'], grammar.pool['A'], grammar.pool['B'], grammar.pool['C']}

    def test_build_nullability_set_SET1_success(self):
        schema = """
            S   : E
                ;
            
            E   : T E1
                ;
            
            E1  : '+' E
                | ε
                ;
            
            T   : F T1
                ;
            
            T1  : '*' T
                | ε
                ;
            
            F   : '(' E ')'
                | 'id'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['E1'], grammar.pool['T1']}

    def test_build_nullability_set_SBA_success(self):
        schema = """
            S   : B A
                ;
            
            A   : '+' B A
                | ε
                ;
            
            B   : D C
                ;
            
            C   : '*' D C
                | ε
                ;
            
            D   : '(' S ')'
                | 'a'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['C']}

    def test_build_nullability_set_ABCd_success(self):
        schema = """
            S   : A B C 'd'
                ;
            
            A   : 'j'
                | 'f'
                | ε
                ;
            
            B   : 'g'
                | 'h'
                | ε
                ;
            
            C   : 'p'
                | 'q'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 7
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['B']}

    def test_build_nullability_set_ETQ_success(self):
        schema = """
            E   : T Q
                ;
            
            Q   : '+' T Q
                | '-' T Q
                | ε
                ;
            
            T   : F R
                ;
            
            R   : '*' F R
                | '/' F R
                | ε
                ;
            
            F   : '(' E ')'
                | 'i'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 7
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['Q'], grammar.pool['R']}

    def test_build_nullability_set_SaBA_success(self):
        schema = """
            S   : 'a' B A
                | B B
                | B 'c'
                ;
            
            A   : A 'd'
                | 'd'
                ;
            
            B   : ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['S'], grammar.pool['B']}

    def test_build_nullability_set_ABCabcd_success(self):
        schema = """
            S   : A B C 'a' 'b' 'c' 'd'
                ;
            
            A   : 'a'
                | ε
                ;
            
            B   : 'b'
                | ε
                ;
            
            C   : 'c'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 4
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 3
        assert nullables == {grammar.pool['A'], grammar.pool['B'], grammar.pool['C']}

    def test_build_nullability_set_SBA_DC_success(self):
        schema = """
            S   : B A
                ;
            
            A   : '+' B A
                | ε
                ;
            
            B   : D C
                ;
            
            C   : '*' D C
                | ε
                ;
            
            D   : '(' S ')'
                | 'a'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['C']}

    def test_build_nullability_set_AaAd_success(self):
        schema = """
            S   : A '#' '#'
                ;
            
            A   : 'a' A 'd'
                | B C
                ;
            
            B   : 'b' B 'c'
                | ε
                ;
            
            C   : 'a' 'c' C
                | 'a' 'd'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['B']}

    def test_build_nullability_set_S1S_success(self):
        schema = """
            S1 : S
               ;
            
            S : A
              | A B
              | B
              ;
            
            A : C
              ;
            
            B : D
              ;
            
            C : 'p'
              | ε
              ;
            
            D : 'q'
              ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 2
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S1'], grammar.pool['S'], grammar.pool['A'], grammar.pool['C']}

    def test_build_nullability_set_gBdS2_success(self):
        schema = """
            S   : 'g' B 'd' S2
                | 'h' 'f' 'd' S2
                ;
            
            S1  : 'e' B 'd' S1
                | ε
                ;
            
            S2  : 'h' B 'd' S1
                | 'e' B 'd' S1
                | ε
                ;
            
            B   : 'g'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 3
        assert nullables == {grammar.pool['S1'], grammar.pool['S2'], grammar.pool['B']}

    def test_build_nullability_set_uBz_success(self):
        schema = """
            S   : 'u' B 'z'
                ;
            
            B   : 'v' B2
                ;
            
            B1  : 'v' B1
                | 'y' E B1
                | ε
                ;
            
            B2  : 'u' E B1
                | 'x' 'u' E B1
                ;
            
            E   : 'v' E1
                ;
            
            E1  : 'x'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['B1'], grammar.pool['E1']}

    def test_build_nullability_set_ampSamp_success(self):
        schema = """
            S1  : '&' S '&'
                ;
            
            S   : 'a' A
                | 'b' B
                ;
            
            A   : 'c' A 'd'
                | ε
                ;
            
            B   : 'c' B 'd'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['A'], grammar.pool['B']}

    def test_build_nullability_set_LLE_success(self):
        schema = """
            L   : L ';' E
                | E
                ;
            
            E   : E ',' P
                | P
                ;
            
            P   : 'a'
                | '(' M ')'
                ;
            
            M   : L
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['M']}

    def test_build_nullability_set_BAAAA_success(self):
        schema = """
            S : B
              ;
            
            B : A A A A
              ;
            
            A : 'x'
              | E
              ;
            
            E : ε
              ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S'], grammar.pool['B'], grammar.pool['A'], grammar.pool['E']}

    def test_build_nullability_set_SAAx_success(self):
        schema = """
            S : A A 'x'
              ;
            
            A : ε
              ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['A']}

    def test_build_nullability_set_SACA_success(self):
        schema = """
            S  : A C A
               | C A
               | A A
               | A C
               | A
               | C
               | ε
               ;
            
            A  : 'a' A 'a'
               | 'a' 'a'
               | B
               | C
               ;
            
            B  : 'b' B
               | 'b'
               ;
            
            C  : 'c' C
               | 'c'
               ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['S']}

    def test_build_nullability_set_Aa_recursive_success(self):
        schema = """
            A   : 'a'
                | ε
                ;
            B   : B A
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 2
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 1
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['A']}

    def test_build_nullability_set_ABBB_success(self):
        schema = """
            S   : '0' A '0'
                | '1' B '1'
                | B B
                ;
            
            A   : C
                ;
            
            B   : S
                | A
                ;
            
            C   : S
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 2
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['S'], grammar.pool['A'], grammar.pool['B'], grammar.pool['C']}

    def test_build_nullability_set_uBDz_success(self):
        schema = """
            S   : 'u' B D 'z'
                ;
            B   : B 'v'
                | 'w'
                ;
            D   : E F
                ;
            E   : 'y'
                | ε
                ;
            F   : 'x'
                | ε
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 6
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 3
        assert nullables == {grammar.pool['D'], grammar.pool['E'], grammar.pool['F']}

    def test_build_nullability_set_Zd_success(self):
        schema = """
            Z   : 'd'
                | X Y Z
                ;
            Y   : ε
                | 'c'
                ;
            X   : Y
                | 'a'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 2
        assert nullables == {grammar.pool['Y'], grammar.pool['X']}

    def test_build_nullability_set_DABC_success(self):
        schema = """
            D   : A B C
                ;
            C   : A B
                | 'c'
                ;
            Q   : Q 'a'
                | 'b'
                ;
            B   : ε
                | 'b'
                | 'a' 'b' D Q
                ;
            A   : ε
                | 'a'
                ;
        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['A'], grammar.pool['B'], grammar.pool['C'], grammar.pool['D']}


if __name__ == '__main__':
    """
    """
    unittest.main()
