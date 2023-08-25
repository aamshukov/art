#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import inspect
import unittest

from art.framework.core.domain_helper import DomainHelper
from art.framework.core.logger import Logger
from art.framework.core.diagnostics import Diagnostics
from art.framework.core.platform import Platform
from art.framework.frontend.data_provider.file_data_provider import FileDataProvider
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.ast.art_ast import ArtAst
from art.language.art.grammar.art_grammar import ArtGrammar
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind
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
            if 'PRIMARY_EXPRESSION' in rule.name:
                pass
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

    def test_type_1_success(self):
        program = """
        T
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_2_success(self):
        program = """
        int
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_3_success(self):
        program = """
        A < T >
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_4_success(self):
        program = """
        A < T > . B < U > . C < D < E < X >>>
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_5_success(self):
        program = """
        A < T[] > [ ]
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_6_success(self):
        program = """
        R.K . A < T.R <int>[] > . S.U <real[]>  . G. B.V <bool [,, ]> . W <A<H>> . Q.X <J,P>  [ , , ,  , ]
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    def test_type_7_success(self):
        program = """
        A < K . B < U [ , ] > [ , , ]  >[ , , , ]
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_type().tree
        filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
        ParseTreeDomainHelper.generate_graphviz(tree,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}'))
        assert parser.diagnostics.status
        ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
        ParseTreeDomainHelper.generate_graphviz(ast,
                                                Test.get_dot_filepath(
                                                    f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))

    # def test_type_8_success(self):
    #     program = """
    #     T[]  [,,][,]
    #     """
    #     parser = Test.get_parser(program)
    #     parser.lexical_analyzer.next_lexeme()
    #     tree = parser.parse_type().tree
    #     filename = ArtGrammar.normalize_symbol_name(tree.symbol.grammar_symbol.name)
    #     ParseTreeDomainHelper.generate_graphviz(tree,
    #                                             Test.get_dot_filepath(
    #                                                 f'{inspect.currentframe().f_code.co_name}_{filename}'))
    #     assert parser.diagnostics.status
    #     ast = ArtAst.type_cst_to_ast(tree, parser.grammar)
    #     ParseTreeDomainHelper.generate_graphviz(ast,
    #                                             Test.get_dot_filepath(
    #                                                 f'{inspect.currentframe().f_code.co_name}_{filename}.ast'))
    #     assert parser.diagnostics.status

    def test_type_array_elements_success(self):
        programs =\
            [
                '[0]',
                '[0, 2 ]',
                '[ 0,1,  2]',
                '[0]',
                '[0, 1 ]',
                '[ 0,1,  2]',
                '[ 0,1,  2, 3 ]',
                '[:]',
                '[: ]',
                '[ :]',
                '[ : ]',
                '[1:]',
                '[ 1 : ]',
                '[:1]',
                '[ : 1 ]',
                '[1:1]',
                '[ 1 : 1 ]'
                '[1::]',
                '[ 1 : : ]',
                '[:1:]',
                '[ : 1 : ]',
                '[::1]',
                '[ : : 1 ]',
                '[1:1:]',
                '[ 1 : 1 : ]',
                '[1::1]',
                '[ 1 : : 1 ]',
                '[:1:1]',
                '[ : 1 : 1 ]',
                '[1:1:1]',
                '[ 1 : 1 : 1 ]',
                '[column jagged sparse unchecked dynamic: 1..5,1..8,0..4]',
                '[ column unchecked dynamic :1,1..8,0..4]',
                '[ 1 .. 5,1..8, 0..4 ]',
                '[1..5 , 1 .. 8, 0 .. 4  ]',
                '[jagged:1, 8,  0..4]'
            ]
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_array_elements()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status
