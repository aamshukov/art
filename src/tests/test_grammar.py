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


if __name__ == '__main__':
    """
    """
    unittest.main()
