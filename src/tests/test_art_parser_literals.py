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
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.tokenizer.token_factory import TokenFactory
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.grammar.art_grammar import ArtGrammar
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
        dp = StringDataProvider(schema)
        grammar = ArtGrammar(logger=logger)
        grammar.load(dp)
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
            fq_identifier = parser.parse_literal(root)
            fq_identifier.tree.papa = None
            filename = ArtGrammar.normalize_symbol_name(fq_identifier.tree.symbol.token.literal)
            ParseTreeDomainHelper.generate_graphviz(fq_identifier.tree,
                                                    Test.get_dot_filepath(
                                                        f'{inspect.currentframe().f_code.co_name}_{filename}'))
            assert parser.diagnostics.status
