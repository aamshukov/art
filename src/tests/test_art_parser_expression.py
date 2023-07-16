#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import inspect
import unittest
from art.framework.core.logger import Logger
from art.framework.core.diagnostics import Diagnostics
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_tree_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.art_parser import ArtParser
from art.language.art.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    expression_grammar = """
        expression                          : assignment
                                            ;

        assignment                          : unary_expression assignment_operator expression
                                            ;

        unary_expression                    : primary_expression
                                            | '+' unary_expression
                                            | '-' unary_expression
                                            | '!' unary_expression
                                            | 'not' unary_expression
                                            | '~' unary_expression
                                            | pre_increment_expression
                                            | pre_decrement_expression
                                            ;

        primary_expression                  : literal                               # 5, 3.14, 'text', true
                                            | member_access                         # Foo.name, foo.name, geo.point<T>, point<real>
                                            | post_increment_expression             # i++
                                            | post_decrement_expression             # i--
                                            | parenthesized_expression              # '(' expression ')'
                                            ;
        
        member_access                       : fully_qualified_identifier
                                            | primary_expression '.' identifier
                                            ;
        
        parenthesized_expression            : '(' expression ')'
                                            ;

        post_increment_expression           : primary_expression '++'
                                            ;
        
        post_decrement_expression           : primary_expression '--'
                                            ;

        pre_increment_expression            : '++' unary_expression
                                            ;

        pre_decrement_expression            : '--' unary_expression
                                            ;

        multiplicative_expression           : unary_expression
                                            | multiplicative_expression '*' unary_expression
                                            | multiplicative_expression '/' unary_expression
                                            | multiplicative_expression '%' unary_expression
                                            ;
        
        additive_expression                 : multiplicative_expression
                                            | additive_expression '+' multiplicative_expression
                                            | additive_expression '-' multiplicative_expression
                                            ;
        
        shift_expression                    : additive_expression
                                            | shift_expression '<<' additive_expression
                                            | shift_expression '>>' additive_expression
                                            ;

        relational_expression               : shift_expression
                                            | relational_expression '<' shift_expression
                                            | relational_expression 'lt' shift_expression
                                            | relational_expression '>' shift_expression
                                            | relational_expression 'gt' shift_expression
                                            | relational_expression '<=' shift_expression
                                            | relational_expression 'le' shift_expression
                                            | relational_expression '>=' shift_expression
                                            | relational_expression 'gt' shift_expression
                                            ;
        
        equality_expression                 : relational_expression
                                            | equality_expression '==' relational_expression
                                            | equality_expression 'eq' relational_expression
                                            | equality_expression '!=' relational_expression
                                            | equality_expression 'ne' relational_expression
                                            ;
        
        and_expression                      : equality_expression
                                            | and_expression '&' equality_expression
                                            ;
        
        exclusive_or_expression             : and_expression
                                            | exclusive_or_expression '^' and_expression
                                            ;
        
        inclusive_or_expression             : exclusive_or_expression
                                            | inclusive_or_expression '|' exclusive_or_expression
                                            ;
        
        conditional_and_expression          : inclusive_or_expression
                                            | conditional_and_expression '&&' inclusive_or_expression
                                            | conditional_and_expression 'and' inclusive_or_expression
                                            ;
        
        conditional_or_expression           : conditional_and_expression
                                            | conditional_or_expression '||' conditional_and_expression
                                            | conditional_or_expression 'or' conditional_and_expression
                                            ;

        assignment_operator                 : '='
                                            | '+='
                                            | '-='
                                            | '*='
                                            | '/='
                                            | '%='
                                            | '&='
                                            | '|='
                                            | '^='
                                            | '~='
                                            | '<<='
                                            | '>>='
                                            ;

        literal                             : 'integer_number_literal'
                                            | 'real_number_literal'
                                            | 'string_literal'
                                            | 'boolean_literal'
                                            ;

        fully_qualified_identifier          : identifier
                                            | fully_qualified_identifier '.' identifier
                                            ;

        identifier                          : 'identifier'
                                            ;

    """  # noqa

    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @staticmethod
    def get_dot_filepath(filename):
        return rf'd:\tmp\art\{filename}.png'

    @staticmethod
    def get_parser(schema, program):
        logger = Logger(path=r'd:\tmp\art', mode='w')
        grammar = Grammar(logger=logger)
        grammar.load(schema)
        GrammarAlgorithms.build_first_set(grammar, 1)
        GrammarAlgorithms.build_follow_set(grammar, 1)
        GrammarAlgorithms.build_la_set(grammar, 1)
        decorated_grammar = grammar.decorate()
        logger.info(decorated_grammar)
        decorated_pool = grammar.decorate_pool()
        logger.info(decorated_pool)
        dp = StringDataProvider(program)
        data = dp.load()
        content = Content(0, data, '')
        content.build_line_map()
        statistics = Statistics()
        diagnostics = Diagnostics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        context = ParseContext()
        parser = ArtParser(context, lexer, grammar, statistics, diagnostics)
        return parser

    def test_expression_1_success(self):
        program = """
        """
        parser = Test.get_parser(Test.expression_grammar, program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_expression()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        assert parser.diagnostics.status
