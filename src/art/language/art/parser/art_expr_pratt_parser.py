#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art precedence climbing parser """
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.precedence.operator_precedence.operator_precedence_level import \
    OperatorPrecedenceLevel
from art.framework.frontend.parser.precedence.pratt.pratt_parser import \
    PrattParser
from art.framework.frontend.parser.precedence.pratt.pratt_parser_handler import PrattParserHandler


class ArtExprPrattParser(PrattParser):
    """
    """
    def __init__(self,
                 context,
                 lexical_analyzer,
                 grammar,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__(context,
                         lexical_analyzer,
                         grammar,
                         statistics,
                         diagnostics)
        self.handlers = self.build_handlers()

    def parse(self, *args, **kwargs):
        """
        """
        super().parse(rbp=OperatorPrecedenceLevel.UNKNOWN)

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
        handlers = {
            TokenKind.PLUS_SIGN: PrattParserHandler(OperatorPrecedenceLevel.LOGICAL_OR,
                                                    self.parse_infix_operator,
                                                    self.parse_postfix_operator)
        }
        return handlers
