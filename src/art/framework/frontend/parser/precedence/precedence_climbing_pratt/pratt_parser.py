#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Pratt/Precedence climbing parser """
from abc import abstractmethod
from art.framework.frontend.parser.precedence.operator_precedence.operator_prcedence_parser import \
    OperatorPrecedenceParser


class PrattParser(OperatorPrecedenceParser):
    """
    """
    def __init__(self,
                 handlers,
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
        self.handlers = handlers  # dict of TokeKind:PrattParserHandler

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        Top Down Operator Precedence, Douglas Crockford
        http://crockford.com/javascript/tdop/tdop.html
            nud - null denotation, null context - nothing on the left, nud does not care about the tokens to the left
            led - left denotation, left context - led does
            lbp - left binding power
            rbp - right binding power
        """  # noqa
        rbp = kwargs['rbp']
        lexer = self.lexical_analyzer
        token = lexer.token
        handler = self.handlers[token.kind]
        left = handler.nud()
        while rbp < handler.lbp:
            handler = self.context.handler(lexer.token.kind)
            lexer.next_lexeme()
            left = handler.led(left)
        return left
