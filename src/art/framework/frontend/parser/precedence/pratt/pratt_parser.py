#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Pratt/Precedence climbing parser """
from abc import abstractmethod
from art.framework.core.diagnostics.status import Status
from art.framework.frontend.parser.precedence.operator_precedence.operator_prcedence_parser import \
    OperatorPrecedenceParser


class PrattParser(OperatorPrecedenceParser):
    """
    """
    def __init__(self, parser):
        """
        """
        super().__init__(parser.context,
                         parser.lexical_analyzer,
                         parser.grammar,
                         parser.statistics,
                         parser.diagnostics)
        self.parser = parser  # master parser
        self.handlers = None  # dict of TokeKind:PrattParserHandler

    @abstractmethod
    def parse(self, *args, **kwargs):
        """
        Top Down Operator Precedence, Douglas Crockford
        http://crockford.com/javascript/tdop/tdop.html
        https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html
            nud - null denotation, null context - nothing on the left, nud does not care about the tokens to the left
            led - left denotation, left context - led does
            lbp - left binding power, precedence
            rbp - right binding power, precedence
        """  # noqa
        assert self.handlers, "Handlers of Pratt parser are not initialized."
        rbp = kwargs.get('rbp')  # precedence
        papa = kwargs.get('papa')
        lexer = self.lexical_analyzer
        self.parser.consume_noise(papa)
        if lexer.eos():
            return self.parser.syntax_error(None, Status.UNEXPEXTED_EOS, f'Unexpected EOS')
        handler = self.handlers[lexer.token.kind]
        assert handler.nud, f"Nud of the Pratt parser's handler is not defined for {lexer.token.kind.name}."
        lhs = handler.nud()
        while rbp < handler.lbp:
            self.parser.consume_noise(papa)
            lexer.next_lexeme()
            if lexer.eos():
                break
            if not self.valid_led_token(lexer.token.kind):
                lhs = self.parser.syntax_error(papa,
                                               Status.INVALID_TOKEN,
                                               f'Expected Led valid token, found {lexer.token.kind.name}')
                break
            handler = self.context.handler(lexer.token.kind)
            assert handler.led, f"Led of the Pratt parser's handler is not defined for {lexer.token.kind.name}."
            lhs = handler.led(lhs)
        return lhs

    def valid_led_token(self, kind):
        """
        """
        return True
