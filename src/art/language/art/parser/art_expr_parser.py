#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Pratt's parser """
from collections import defaultdict
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_result import ParseResult
from art.framework.frontend.parser.precedence.operator_precedence.operator_precedence_level import \
    OperatorPrecedenceLevel
from art.framework.frontend.parser.precedence.pratt.pratt_parser import \
    PrattParser
from art.framework.frontend.parser.precedence.pratt.pratt_parser_handler import PrattParserHandler
from art.language.art.ast.art_ast import ArtAst
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind


class ArtExprParser(PrattParser):
    """
    Art expression parser based on the Pratt's algorithm.
    """
    def __init__(self, parser):
        """
        """
        super().__init__(parser)
        self.handlers = self.build_handlers()

    def parse(self, *args, **kwargs):
        """
        """
        expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.EXPRESSION, self.grammar)
        return super().parse(rbp=OperatorPrecedenceLevel.UNKNOWN, papa=expression)

    def parse_primary_expr(self):
        """
        primary_expr : literal
                     | identifier
                     ;
        """ # noqa
        self.parser.inc_recursion_level()
        primary_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.PRIMARY_EXPRESSION, self.grammar)
        self.parser.consume_noise(primary_expression)
        if self.parser.literal():
            self.parser.parse_literal(primary_expression)
        elif self.parser.lexer.token.kind == TokenKind.IDENTIFIER:
            identifier = self.parser.parse_identifier()
            primary_expression.add_kid(identifier.tree)
        self.parser.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, primary_expression)

    def parse_prefix_operator(self, nud):
        """
        """
        return None

    def parse_infix_operator(self, led):
        """
        """
        return None

    def parse_postfix_operator(self, led):
        """
        """
        return None

    def build_handlers(self):
        """
        """
        handlers = defaultdict(lambda: PrattParserHandler(OperatorPrecedenceLevel.UNKNOWN))

        handlers[TokenKind.INTEGER] = PrattParserHandler(OperatorPrecedenceLevel.LITERAL,
                                                         nud=self.parse_primary_expr)
        handlers[TokenKind.REAL] = PrattParserHandler(OperatorPrecedenceLevel.LITERAL,
                                                      nud=self.parse_primary_expr)
        handlers[TokenKind.STRING] = PrattParserHandler(OperatorPrecedenceLevel.LITERAL,
                                                        nud=self.parse_primary_expr)
        handlers[TokenKind.TRUE_KW] = PrattParserHandler(OperatorPrecedenceLevel.LITERAL,
                                                         nud=self.parse_primary_expr)
        handlers[TokenKind.FALSE_KW] = PrattParserHandler(OperatorPrecedenceLevel.LITERAL,
                                                          nud=self.parse_primary_expr)

        handlers[TokenKind.PLUS_SIGN] = PrattParserHandler(OperatorPrecedenceLevel.ADDITIVE,
                                                           nud=self.parse_prefix_operator,
                                                           led=self.parse_infix_operator)
        handlers[TokenKind.ADD_KW] = PrattParserHandler(OperatorPrecedenceLevel.ADDITIVE,
                                                        nud=self.parse_prefix_operator,
                                                        led=self.parse_infix_operator)
        handlers[TokenKind.HYPHEN_MINUS] = PrattParserHandler(OperatorPrecedenceLevel.ADDITIVE,
                                                              nud=self.parse_prefix_operator,
                                                              led=self.parse_infix_operator)
        handlers[TokenKind.SUB_KW] = PrattParserHandler(OperatorPrecedenceLevel.ADDITIVE,
                                                        nud=self.parse_prefix_operator,
                                                        led=self.parse_infix_operator)
        return handlers
