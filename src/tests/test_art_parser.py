#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest

from art.framework.core.logger import Logger
from art.framework.core.text import Text
from art.framework.core.diagnostics import Diagnostics
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_tree_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.token.tokenizer import Tokenizer
from art.language.art.art_parser import ArtParser
from art.language.art.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    fq_id_grammar = """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;
    """

    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @staticmethod
    def get_parser(schema, program):
        logger = Logger()
        grammar = Grammar(logger=logger)
        grammar.load(schema)
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

    def test_fully_qualified_identifier_empty_success(self):
        program = """
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        parser.lexical_analyzer.next_lexeme()
        tree = parser.parse_fully_qualified_identifier()
        assert tree.kind == ParseTreeKind.UNKNOWN
        assert not parser.diagnostics.status

    def test_fully_qualified_identifier_1_success(self):
        program = """
        foo
        """
        parser = Test.get_parser(Test.fq_id_grammar, program)
        while (not parser.lexical_analyzer.eos() and
               parser.lexical_analyzer.next_lexeme().kind != TokenKind.IDENTIFIER):
            pass
        tree = parser.parse_fully_qualified_identifier()
        assert tree.kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert not tree.kids
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
        assert tree.kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert not tree.kids
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
        assert tree.kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert tree.kids
        assert len(tree.kids) == 2
        assert tree.kids[0].kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert tree.kids[1].kind == ParseTreeKind.IDENTIFIER
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
        assert tree.kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert tree.kids
        assert len(tree.kids) == 2
        assert tree.kids[0].kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert tree.kids[1].kind == ParseTreeKind.IDENTIFIER
        assert tree.kids[0].kids
        assert len(tree.kids[0].kids) == 2
        assert tree.kids[0].kids[0].kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        assert tree.kids[0].kids[1].kind == ParseTreeKind.IDENTIFIER
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
        assert tree.kind == ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER
        # assert ParseTreeDomainHelper.to_string(tree) == ''
        assert parser.diagnostics.status
