#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import inspect
import unittest
from art.framework.core.logger import Logger
from art.framework.core.diagnostics import Diagnostics
from art.framework.core.platform import Platform
from art.framework.frontend.data_provider.file_data_provider import FileDataProvider
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.grammar.art_grammar import ArtGrammar
from art.language.art.parser.art_parser import ArtParser
from art.language.art.parser.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    grammar = None

    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @classmethod
    def setUp(cls):
        Platform.increase_recursion_limit()
        if not cls.grammar:
            logger = Logger(path=r'd:\tmp\art', mode='w')
            dp = FileDataProvider(r'../../docs/art-grammar.txt')
            grammar = ArtGrammar(logger=logger)
            grammar.load(dp)
            # k = 1
            # GrammarAlgorithms.build_first_set(grammar, k)
            # GrammarAlgorithms.build_follow_set(grammar, k)
            # GrammarAlgorithms.build_la_set(grammar, k)
            # decorated_grammar = grammar.decorate()
            # logger.info(decorated_grammar)
            # decorated_pool = grammar.decorate_pool()
            # logger.info(decorated_pool)
            # Test.dump_rules_la(grammar, logger, k)
            cls.grammar = grammar

    @staticmethod
    def dump_rules_la(grammar, logger, k=1):
        logger.info('Rules LA')
        for rule in grammar.rules:
            la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
            la_str = f'{rule.name}: {GrammarSymbol.sets_to_string(la)}'
            logger.info(la_str)

    @staticmethod
    def get_parser(program):
        dp = StringDataProvider(program)
        data = dp.load()
        content = Content(data, '')
        content.build_line_map()
        statistics = Statistics()
        diagnostics = Diagnostics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        context = ParseContext()
        parser = ArtParser(context, lexer, Test.grammar, statistics, diagnostics)
        return parser

    @staticmethod
    def get_dot_filepath(filename):
        return rf'd:\tmp\art\{filename}.png'

    def test_pm_expression_empty_success(self):
        program = """
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        pm_expr = parser.parse_primary_expression()
        ParseTreeDomainHelper.generate_graphviz(pm_expr.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        assert not parser.diagnostics.status

    def test_pm_expression_literals_success(self):
        programs = ['1', '3.14', 'false', 'true', '"str"']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_integral_types_success(self):
        programs = ['int.a',
                    'integer.a<T>',
                    'real.a',
                    'float.a',
                    'double.a',
                    'decimal.a',
                    'number.a',
                    'bool.a',
                    'boolean.a',
                    'string.a']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_member_access_success(self):
        programs = ['a', 'x.y', 'e . f . g']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_invocation_success(self):
        programs = ['foo ( )', 'a.bar()', 'a.b.bar()', 'a .b .c .d. foo(1,2,3)']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_post_success(self):
        programs = ['a ++', 'a --']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_array_element_access_success(self):
        programs = ['array[0]', 'array[0, 2 ]', 'array[ 0,1,  2]']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_array_slicing_success(self):
        programs = [
                    'a[:]',
                    'a[: ]',
                    'a[ :]',
                    'a[ : ]',
                    'a[1:]',
                    'a[ 1 : ]',
                    'a[:1]',
                    'a[ : 1 ]',
                    'a[1:1]',
                    'a[ 1 : 1 ]',
                    'a[1::]',
                    'a[ 1 : : ]',
                    'a[:1:]',
                    'a[ : 1 : ]',
                    'a[::1]',
                    'a[ : : 1 ]',
                    'a[1:1:]',
                    'a[ 1 : 1 : ]',
                    'a[1::1]',
                    'a[ 1 : : 1 ]',
                    'a[:1:1]',
                    'a[ : 1 : 1 ]',
                    'a[1:1:1]',
                    'a[ 1 : 1 : 1 ]'
                ]
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_pm_expression_object_creation_array_success(self):
        programs =\
            [
                'int.len [ 1..5, -1..8,0..4 ] { {3, 4 }, {}, { 1}  }',
                'real.len [column jagged sparse unchecked dynamic: 1..5, -1..8,0..4 ] { {3.14, 4.01 }, {0.0} }'
            ]
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            # assert parser.diagnostics.status

    def test_pm_expression_parenthesized_success(self):
        programs = [
            '( 2 )',
            '( ( 3))',
            '(( ( 4 )))',
            '(foo( ) )',
            '((foo( ) ) )'
        ]
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status
