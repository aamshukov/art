#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.logging.logger import Logger
from art.framework.core.diagnostics.diagnostics import Diagnostics
from art.framework.core.utils.platform import Platform
from art.framework.frontend.data_provider.file_data_provider import FileDataProvider
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.parser.parse_context import ParseContext
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
            k = 1
            GrammarAlgorithms.build_nullability_set(grammar)
            GrammarAlgorithms.build_first_set(grammar, k)
            GrammarAlgorithms.build_follow_set(grammar, k)
            GrammarAlgorithms.build_la_set(grammar, k)
            decorated_grammar = grammar.decorate()
            logger.info(decorated_grammar)
            decorated_pool = grammar.decorate_pool()
            logger.info(decorated_pool)
            Test.dump_rules_la(grammar, logger, k)
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

    def test_art_grammar_success(self):
        parser = Test.get_parser("")
        assert parser
