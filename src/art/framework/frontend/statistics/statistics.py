#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Statistics """
from collections import defaultdict
from art.framework.core.domain.base import Base
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind

NUMBER_OF_LEXEMES = 'number_of_lexemes'
NUMBER_OF_KEYWORDS = 'number_of_keywords'
NUMBER_OF_IDENTIFIERS = 'number_of_identifiers'


class Statistics(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.quantities = defaultdict(lambda: 0)  # source:quantity
        self.timings = defaultdict(lambda: 0.0)  # source:duration

    def update_stats(self, token):
        """
        """
        self.quantities[NUMBER_OF_LEXEMES] += 1
        match token.kind:
            case TokenKind.IDENTIFIER:
                self.quantities[NUMBER_OF_IDENTIFIERS] += 1
            case TokenKind.CASE_KW | TokenKind.BOOLEAN_KW:
                self.quantities[NUMBER_OF_KEYWORDS] += 1
        # ?? print(tokenizer)
