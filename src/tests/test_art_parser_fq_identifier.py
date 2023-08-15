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
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.parser.parse_result import ParseResult
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.tokenizer.token_factory import TokenFactory
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.grammar.art_grammar import ArtGrammar
from art.language.art.helpers.art_domain_helper import ArtDomainHelper
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
            cls.grammar = grammar

    @staticmethod
    def get_dot_filepath(filename):
        return rf'd:\tmp\art\{filename}.png'

    @staticmethod
    def make_tree(kind, grammar):
        """
        """
        return ParseTreeFactory.make_tree(kind, grammar, TokenFactory.UNKNOWN_TOKEN)

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

    def test_fully_qualified_identifier_empty_success(self):
        program = """
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_1_success(self):
        program = """
        foo
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        assert fq_identifier.status == ParseResult.Status.OK
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_2_success(self):
        program = """
        foo.
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert not parser.diagnostics.status

    def test_fully_qualified_identifier_3_success(self):
        program = """
        foo.bar
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_4_success(self):
        program = """
        foo.bar.tree
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_5_success(self):
        program = """
        parser.lexical_analyzer.next_lexeme.kind.TokenKind.IDENTIFIER
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_kw_success(self):
        program = """
        parser.lexical_analyzer.while.kind.TokenKind.IDENTIFIER
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str == 'parser.lexical_analyzer.'
        assert not parser.diagnostics.status

    def test_fully_qualified_identifier_7_success(self):
        program = """
        A<T>
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_8_success(self):
        program = """
        A<T>.B<U, X, Y>.C< A <B<X> >, Z>
        """
        parser = Test.get_parser(program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        fq_identifier = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(fq_identifier.tree)
        print(tree_str)
        assert tree_str.strip(' \n') == program.strip(' \n')
        assert parser.diagnostics.status
