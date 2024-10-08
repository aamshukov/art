#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Pratt parser handler """
from art.framework.core.domain.base import Base


class PrattParserHandler(Base):
    """
    """
    def __init__(self, lbp, nud=None, led=None):
        """
        Top Down Operator Precedence, Douglas Crockford
        http://crockford.com/javascript/tdop/tdop.html
            nud - null denotation, null context - nothing on the left, nud does not care about the tokens to the left
            led - left denotation, left context - led does
            lbp - left binding power, precedence
            rbp - right binding power, precedence
        """  # noqa
        super().__init__()
        self.lbp = lbp
        self.nud = nud
        self.led = led
