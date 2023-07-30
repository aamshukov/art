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
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.tokenizer.token_factory import TokenFactory
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.helpers.art_domain_helper import ArtDomainHelper
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind
from art.language.art.parser.art_parser import ArtParser
from art.language.art.parser.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    literal_grammar = """
        literal : 'integer_number_literal'
                | 'real_number_literal'
                | 'string_literal'
                | 'boolean_literal'
                ;
    """

    fq_id_grammar = """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;

        identifier                 : 'identifier'
                                   ;

        terminal                   : 'terminal'
                                   ;
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @staticmethod
    def get_dot_filepath(filename):
        return rf'd:\tmp\art\{filename}.png'

    @staticmethod
    def make_tree(kind, grammar):
        """
        """
        return ParseTreeFactory.make_tree(kind, grammar, TokenFactory.UNKNOWN_TOKEN)

    @staticmethod
    def get_parser(schema, program):
        logger = Logger()
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
        content = Content(data, '')
        content.build_line_map()
        statistics = Statistics()
        diagnostics = Diagnostics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        context = ParseContext()
        parser = ArtParser(context, lexer, grammar, statistics, diagnostics)
        return parser

    def test_fully_qualified_identifier_empty_success(self):
        program = """
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        if parser.lexical_analyzer.token.kind == TokenKind.IDENTIFIER:
            tree = parser.parse_fully_qualified_identifier()
            ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
            assert tree.kind == ArtParseTreeKind.UNKNOWN
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_1_success(self):
        program = """
        foo
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_2_success(self):
        program = """
        foo.
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == program.strip(' \n.')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_3_success(self):
        program = """
        foo.bar
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_4_success(self):
        program = """
        foo.bar.tree
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_5_success(self):
        program = """
        parser.lexical_analyzer.next_lexeme.kind.TokenKind.IDENTIFIER
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == program.strip(' \n')
        assert parser.diagnostics.status

    def test_fully_qualified_identifier_6_success(self):
        program = """
        parser.lexical_analyzer.while.kind.TokenKind.IDENTIFIER
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        tree_str = ArtDomainHelper.to_string(tree)
        print(tree_str)
        assert tree_str == 'parser.lexical_analyzer'
        assert parser.diagnostics.status

    def test_literals_success(self):
        program = """
        123 3.14 'text' true false
        """
        parser = Test.get_parser(Test.literal_grammar, program)
        while not parser.lexical_analyzer.eos():
            parser.lexical_analyzer.next_lexeme()
            kind = parser.lexical_analyzer.token.kind
            if (kind == TokenKind.WS or
                    kind == TokenKind.INDENT or
                    kind == TokenKind.DEDENT or
                    kind == TokenKind.EOL or
                    kind == TokenKind.EOS):
                continue
            root = Test.make_tree(ArtParseTreeKind.UNKNOWN, parser.grammar)
            tree = parser.parse_literal(root)
            tree.papa = None
            filename = Grammar.normalize_symbol_name(tree.symbol.token.literal)
            ParseTreeDomainHelper.generate_graphviz(tree,
                                                    Test.get_dot_filepath(
                                                        f'{inspect.currentframe().f_code.co_name}_{filename}'))
            tree_str = ArtDomainHelper.to_string(tree)
            print(tree_str)
            assert parser.diagnostics.status
