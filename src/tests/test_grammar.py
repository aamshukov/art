# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import itertools
import os
import unittest
from art.framework.core.domain_helper import profile
from art.framework.core.logger import Logger
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.language.art.grammar.art_grammar import ArtGrammar


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

            primary_expression : literal                                        # 5, 'content'
                               | fully_qualified_identifier type_arguments_opt  # geo.point<T>, point<real>
                               | '(' expression ')'
                               ;
                               
            type_arguments_opt  : type_arguments
                                | ε
                                | λ
                                ;                               

        """
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 9
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 7
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 7
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 7
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
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
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 4
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
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 6
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 3
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 4
        assert nullables == {grammar.pool['A'], grammar.pool['B'], grammar.pool['C'], grammar.pool['D']}

    def test_truncate_AU_success(self):
        """
            L1 ⊕k L2
            L1 = { λ, abb }
            L2 = { b, bab }
            L1 ⊕2 L2 = { b, ba, ab }
            AU: p.348
        """
        schema = """
            
            S   : 'a' 'b'
                : λ
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        s1 = [[grammar.pool['λ']], [grammar.pool['a'], grammar.pool['b'], grammar.pool['b']]]
        s2 = [[grammar.pool['b']], [grammar.pool['b'], grammar.pool['a'], grammar.pool['b']]]
        result = GrammarAlgorithms.truncate(grammar, [s1, s2], 2)
        assert result == [[grammar.pool['b']],
                          [grammar.pool['b'], grammar.pool['a']],
                          [grammar.pool['a'], grammar.pool['b']]]

    def test_truncate_empty_success(self):  # ∅
        """
            L1 = { ∅ }
            L2 = { b, bab }
            L1 ⊕2 L2 = { ∅ }
        """
        schema = """
            S   : 'a' 'b'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        s1 = [[]]
        s2 = [[grammar.pool['b']], [grammar.pool['b'], grammar.pool['a'], grammar.pool['b']]]
        result = GrammarAlgorithms.truncate(grammar, [s1, s2], 2)
        assert result == []

    def test_truncate_empty_epsilon_success(self):  # ∅
        """
            L1 = { ∅ }
            L2 = { ∅, ∅ }
            L1 ⊕2 L2 = { ∅ }
        """
        schema = """
            S   : 'a' 'b'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        s1 = [[]]
        s2 = [[], [], []]
        result = GrammarAlgorithms.truncate(grammar, [s1, s2], 2)
        assert result == [[grammar.epsilon]]

    def test_truncate_lambdas_success(self):  # ∅
        """
            L1 = { λ }
            L2 = { λ, λ }
            L1 ⊕2 L2 = { λ }
        """
        schema = """
            S   : λ
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        s1 = [[grammar.pool['λ']]]
        s2 = [[grammar.pool['λ']], [grammar.pool['λ']]]
        result = GrammarAlgorithms.truncate(grammar, [s1, s2], 2)
        assert result == [[grammar.pool['λ']]]

    def test_truncate_Sudkamp_success(self):  # ∅
        """
            TRUNC3( {a, b, λ} {a} {b} {d} {λ} ) = TRUNC3( { aabd, babd, abd} ) = { aab, bab, abd }
        """
        schema = """
            S   : 'a' 'b' 'd'
                : λ
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        s1 = [[grammar.pool['a']], [grammar.pool['b']], [grammar.pool['λ']]]
        s2 = [[grammar.pool['a']]]
        s3 = [[grammar.pool['b']]]
        s4 = [[grammar.pool['d']]]
        s5 = [[grammar.pool['λ']]]
        sets = [s1, s2, s3, s4, s5]
        for i, element in enumerate(itertools.product(*sets)):
            print(str(i) + ': ' + str(element))
        result = GrammarAlgorithms.truncate(grammar, [s1, s2, s3, s4, s5], 3)
        assert result == [[grammar.pool['a'], grammar.pool['a'], grammar.pool['b']],
                          [grammar.pool['b'], grammar.pool['a'], grammar.pool['b']],
                          [grammar.pool['a'], grammar.pool['b'], grammar.pool['d']]]

    def test_build_first_set_Sudkamp_16_4_1_success(self):
        schema = """
            S   : A '#' '#'
                ; 

            A   : 'a' A 'd'
                | B C
                ; 

            B   : 'b' B 'c'
                | λ
                ; 

            C   : 'a' 'c' C
                | 'a' 'd'
                ; 
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['B']}
        GrammarAlgorithms.build_first_set(grammar, 2)
        e = grammar.epsilon
        s = grammar.pool['#']
        a = grammar.pool['a']
        b = grammar.pool['b']
        c = grammar.pool['c']
        d = grammar.pool['d']
        S = grammar.pool['S']
        A = grammar.pool['A']
        B = grammar.pool['B']
        C = grammar.pool['C']
        assert ([a, a] in S.first and
                [a, b] in S.first and
                [a, c] in S.first and
                [a, d] in S.first and
                [b, b] in S.first and
                [b, c] in S.first) and \
            len(S.first) == 6
        assert ([a, a] in A.first and
                [a, b] in A.first and
                [a, c] in A.first and
                [a, d] in A.first and
                [b, b] in A.first and
                [b, c] in A.first) and \
            len(A.first) == 6
        assert ([e] in B.first and
                [b, c] in B.first and
                [b, b] in B.first) and \
            len(B.first) == 3
        assert ([a, d] in C.first and
                [a, c] in C.first) and \
            len(C.first) == 2
        GrammarAlgorithms.build_first_set(grammar, 1)
        assert ([a] in S.first and
                [b] in S.first) and \
            len(S.first) == 2
        assert ([a] in A.first and
                [b] in A.first) and \
            len(A.first) == 2
        assert ([e] in B.first and
                [b] in B.first) and \
            len(B.first) == 2
        assert ([a] in C.first) and \
            len(C.first) == 1
        GrammarAlgorithms.build_first_set(grammar, 3)
        assert len(S.first) == 11
        assert len(A.first) == 11
        assert len(B.first) == 4
        assert len(C.first) == 2

    def test_build_first_follow_la_k2_set_Sudkamp_16_4_1_success(self):
        schema = """
            S   : A '#' '#'
                ; 

            A   : 'a' A 'd'
                | B C
                ; 

            B   : 'b' B 'c'
                | λ
                ; 

            C   : 'a' 'c' C
                | 'a' 'd'
                ; 
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 5
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 5
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['B']}
        e = grammar.epsilon
        s = grammar.pool['#']
        a = grammar.pool['a']
        b = grammar.pool['b']
        c = grammar.pool['c']
        d = grammar.pool['d']
        S = grammar.pool['S']
        A = grammar.pool['A']
        B = grammar.pool['B']
        C = grammar.pool['C']
        GrammarAlgorithms.build_first_set(grammar, 2)
        assert ([a, a] in S.first and
                [a, b] in S.first and
                [a, c] in S.first and
                [a, d] in S.first and
                [b, b] in S.first and
                [b, c] in S.first) and \
            len(S.first) == 6
        assert ([a, a] in A.first and
                [a, b] in A.first and
                [a, c] in A.first and
                [a, d] in A.first and
                [b, b] in A.first and
                [b, c] in A.first) and \
            len(A.first) == 6
        assert ([e] in B.first and
                [b, c] in B.first and
                [b, b] in B.first) and \
            len(B.first) == 3
        assert ([a, d] in C.first and
                [a, c] in C.first) and \
            len(C.first) == 2
        GrammarAlgorithms.build_follow_set(grammar, 2)
        assert [e] in S.follow and len(S.follow) == 1
        assert ([s, s] in A.follow and
                [d, s] in A.follow and
                [d, s] in A.follow) and \
            len(A.follow) == 3
        assert ([a, d] in B.follow and
                [a, c] in B.follow and
                [c, a] in B.follow and
                [c, c] in B.follow) and \
            len(B.follow) == 4
        assert ([s, s] in C.follow and
                [d, s] in C.follow and
                [d, d] in C.follow) and \
            len(C.follow) == 3
        GrammarAlgorithms.build_la_set(grammar, 2)
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[0], 2)
        assert ([a, a] in la and
                [a, b] in la and
                [a, c] in la and
                [a, d] in la and
                [b, b] in la and
                [b, c] in la) and \
            len(la) == 6
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[1], 2)
        assert ([a, a] in la and
                [a, b] in la) and \
            len(la) == 2
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[2], 2)
        assert ([a, c] in la and
                [a, d] in la and
                [b, b] in la and
                [b, c] in la) and \
            len(la) == 4
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[3], 2)
        assert ([b, b] in la and
                [b, c] in la) and \
            len(la) == 2
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[4], 2)
        assert ([a, c] in la and
                [a, d] in la and
                [c, a] in la and
                [c, c] in la) and \
            len(la) == 4
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[5], 2)
        assert ([a, c] in la) and \
            len(la) == 1
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[6], 2)
        assert ([a, d] in la) and \
            len(la) == 1

    def test_build_first_follow_la_k4_set_Sudkamp_16_1_1_success(self):
        schema = """
            S   : A 'a' 'b' 'd'
                | 'c' A 'b' 'c' 'd'
                ; 

            A   : 'a'
                | 'b'
                | λ
                ; 
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        assert len(GrammarAlgorithms.collect_non_terminals(grammar)) == 3
        assert len(GrammarAlgorithms.collect_terminals(grammar)) == 4
        nullables = GrammarAlgorithms.build_nullability_set(grammar)
        assert len(nullables) == 1
        assert nullables == {grammar.pool['A']}
        e = grammar.epsilon
        a = grammar.pool['a']
        b = grammar.pool['b']
        c = grammar.pool['c']
        d = grammar.pool['d']
        S = grammar.pool['S']
        A = grammar.pool['A']
        k = 4
        GrammarAlgorithms.build_first_set(grammar, k)
        assert ([c, b, b, c] in S.first and
                [a, b, d] in S.first and
                [c, b, c, d] in S.first and
                [c, a, b, c] in S.first and
                [b, a, b, d] in S.first and
                [a, a, b, d] in S.first) and \
            len(S.first) == 6
        assert ([e] in A.first and
                [a] in A.first and
                [b] in A.first) and \
            len(A.first) == 3
        GrammarAlgorithms.build_follow_set(grammar, k)
        assert ([e] in S.follow) and \
            len(S.follow) == 1
        assert ([a, b, d] in A.follow and
                [b, c, d] in A.follow) and \
            len(A.follow) == 2
        GrammarAlgorithms.build_la_set(grammar, k)
        assert ([c, a, b, c] in S.la and
                [c, b, b, c] in S.la and
                [c, b, c, d] in S.la and
                [b, a, b, d] in S.la and
                [a, a, b, d] in S.la and
                [a, b, d] in S.la) and \
            len(S.la) == 6
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[0], k)
        assert ([a, a, b, d] in la and
                [a, b, d] in la and
                [b, a, b, d] in la) and \
            len(la) == 3
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[1], k)
        assert ([c, b, c, d] in la and
                [c, a, b, c] in la and
                [c, b, b, c] in la) and \
            len(la) == 3
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[2], k)
        assert ([a, b, c, d] in la and
                [a, a, b, d] in la) and \
            len(la) == 2
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[3], k)
        assert ([b, a, b, d] in la and
                [b, b, c, d] in la) and \
            len(la) == 2
        la = GrammarAlgorithms.build_la_set_rule(grammar, grammar.rules[4], k)
        assert ([b, c, d] in la and
                [a, b, d] in la) and \
            len(la) == 2

    def test_build_first_follow_la_k2_set_SaBA_success(self):
        schema = """
            S   :  ε
                | 'a' 'b' A
                ;
            A   : S 'a' 'a'
                | 'b'
                ; 
        """
        k = 2
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        GrammarAlgorithms.build_first_set(grammar, k)
        GrammarAlgorithms.build_follow_set(grammar, k)
        GrammarAlgorithms.build_la_set(grammar, k)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        for rule in grammar.rules:
            la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
            assert la

    def test_build_first_follow_la_k1_set_SuBz_success(self):
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
        k = 1
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        GrammarAlgorithms.build_first_set(grammar, k)
        GrammarAlgorithms.build_follow_set(grammar, k)
        GrammarAlgorithms.build_la_set(grammar, k)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        for rule in grammar.rules:
            la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
            assert la

    def test_build_first_follow_la_k1_set_SaAb_success(self):
        schema = """
            S   : 'a' A 'b'
                | 'b' A 'a'
                ;
            
            A   : 'c' S
                | ε
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 4):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SaAaa_success(self):
        schema = """
            S   : 'a' A 'a' 'a'
                | 'b' A 'b' 'a'
                ;
            
            A   : 'b'
                | ε
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SgBdS2a_success(self):
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
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SE_success(self):
        schema = """
            S   : E
                | E 'a'
                ;
            
            E   : 'b'
                | ε
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SAcB_success(self):
        schema = """
            S   : A 'c' B
                ;
            
            A   : 'a' A 'b'
                | 'a' 'b'
                ;
            
            B   : 'a' B 'b'
                | 'a' 'c' 'b'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SiEt_success(self):
        schema = """
            S   : 'i' E 't' S S1
                | 'a'
                ;
            
            S1  : 'e' S
                | ε
                ;
            
            E   : 'b'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SET1E_success(self):
        schema = """
            E   : T E1
                ;
            
            E1  : '+' T E1
                | ε
                ;
            
            T   : F T1
                ;
            
            T1  : '*' F T1
                | ε
                ;
            
            F   : '(' E ')'
                | 'a'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SA_Parsons_success(self):
        """
        Parsons, p.87
        """
        schema = """
            S   : A
                | B
                | S 'c'
                | 'd' S
                ;
            
            A   : B 'd'
                | 'c' A
                | 'f'
                ;
            
            B   : S 'e'
                | A 'd'
                | 'g'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)

        @profile('Parson build first set...')
        def fs_profile(_grammar, _k):
            GrammarAlgorithms.build_first_set(_grammar, _k)

        for k in range(1, 5):  # 5+ is too long for python, Ran 1 test in 89.022s
            print(k)
            fs_profile(grammar, k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SaA_Parsons_success(self):
        """
        Parsons, p.87
        """
        schema = """
            S   : 'a' A
                | 'b'
                | 'c' S
                ;
            
            A   : S 'd'
                | 'e'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SSc_success(self):
        """
        Compiler construction, JavaCC, p. 72, 3.9
        """
        schema = """
            S   : S 'c'
                | S B B B
                | S 'c' B
                | B
                | 'c'
                ;
            
            B   : 'b'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_DDx_success(self):
        """
        Kompaniec p.63, 3.1.7
        """
        schema = """
            D   : D 'x'
                | E 'y'
                | F 'z'
                ;
            
            E   : D 'a'
                | F 'c'
                ;
            
            F   : D 'p'
                | E 'q'
                | F 'r'
                | 'w'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SL_success(self):
        """
        Algorithms.For.Compiler.Design.pdf 3.12
        """
        schema = """
            S   : '(' L ')'
                | 'a'
                ;
            
            L   : L ',' S
                | S
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SaBDh_success(self):
        """
        Algorithms.For.Compiler.Design.pdf 3.10
        """
        schema = """
            S   : 'a' B D 'h'
                ;
            
            B   : B 'b'
                | 'c'
                ;
            
            D   : E F
                ;
            
            E   : 'g'
                | ε
                ;
            
            F   : 'f'
                | ε
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SabAB_success(self):
        """
        """
        schema = """
            S   : 'a' 'b' A B 'k' C 'j' D E F
                | 'a' 'b' A B E
                | A B C D
                | A B C
                | A 'k' 's' B
                | A 'k' 's' B
                | A 'k'
                | 'a' 'b' 'c' 'd'
                | 'a' 'b' 'c'
                | 'a' 'b'
                | 'a'
                | 'a' F
                | 'a' 'b' A F
                | ε
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
            D   : 'd'
                | ε
                ;                
            E   : 'e'
                | ε
                ;                
            F   : 'f'
                | ε
                ;                
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SSS_success(self):
        """
        """
        schema = """
            S   : S S '+'
                | S S '*'
                | 'a'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SaAaba_success(self):
        """
        """
        schema = """
            S   : 'a' A
                | 'a' 'b' A
                | 'a' 'b' 'c' A
                | 'a' 'b' 'c'
                | 'k' 'b' 'c' A
                | 'g' 'c' 'c' A
                | '1' '2' '3' '4' '5' A
                | ε
                ;
            A   : 'a'
                | ε
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SBA_success(self):
        """
        """
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
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SaSAAA_success(self):
        """
        """
        schema = """
            S   : 'a' S A A A
                | ε
                ;
            
            A   : 'a'
                | ε
              ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SABABa_success(self):
        """
        """
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
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_S1SAAAA_success(self):
        """
        """
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
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la

    def test_build_first_follow_la_set_SSSn_success(self):
        """
        """
        schema = """
            S   : S '+' S
                | S
                | 'n'
                ;
        """
        logger = Logger(mode='w')
        grammar = ArtGrammar(logger=logger)
        grammar.load(schema)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        GrammarAlgorithms.build_nullability_set(grammar)
        for k in range(1, 5):
            print(k)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            for rule in grammar.rules:
                la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
                assert la


if __name__ == '__main__':
    """
    """
    unittest.main()
