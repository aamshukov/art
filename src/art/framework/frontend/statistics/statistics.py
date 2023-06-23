#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Statistics """
from collections import defaultdict
from art.framework.core.base import Base
from art.framework.frontend.token.token_kind import TokenKind

NUMBER_OF_LEXEMES = 'number_of_lexemes'
NUMBER_OF_KEYWORDS = 'number_of_keywords'
NUMBER_OF_IDENTIFIERS = 'number_of_identifiers'


class Statistics(Base):
    """
    """
    def __init__(self):
        """
        """
        self._quantities = defaultdict(lambda: 0)  # source:quantity
        self._timings = defaultdict(lambda: 0.0)  # source:duration

    def update_stats(self, token):
        """
        """
        self._quantities[NUMBER_OF_LEXEMES] += 1
        match token.kind:
            case TokenKind.IDENTIFIER:
                self._quantities[NUMBER_OF_IDENTIFIERS] += 1
            case TokenKind.CASE | TokenKind.BOOLEAN:
                self._quantities[NUMBER_OF_KEYWORDS] += 1
        # ?? print(token)

    @property
    def quantities(self):
        """
        """
        return self._quantities

    @property
    def timings(self):
        """
        """
        return self._timings
