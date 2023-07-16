# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lexical Analyzer """
from copy import deepcopy
from collections import deque
from art.framework.core.entity import Entity
from art.framework.frontend.token.token_factory import TokenFactory
from art.framework.frontend.token.token_kind import TokenKind


class LexicalAnalyzer(Entity):
    """
    """
    def __init__(self,
                 id,
                 tokenizer,
                 statistics,
                 diagnostics,
                 version='1.0'):
        """
        """
        super().__init__(id,  # master lexer, id = 0
                         version=version)
        self._tokenizer = tokenizer
        self._token = TokenFactory.unknown_token()  # current lexeme
        self._tokens = deque()  # queue of lookahead (cached) lexemes
        self._prev_token = deepcopy(self._token)  # previous lexeme
        self._statistics = statistics
        self._diagnostics = diagnostics

    def __hash__(self):
        """
        """
        result = super().__hash__()
        return result

    def __eq__(self, other):
        """
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        """
        return super().__le__(other)

    @property
    def token(self):
        """
        """
        return self._token

    @property
    def prev_token(self):
        """
        """
        return self._prev_token

    def eol(self):
        """
        """
        return self._token.kind == TokenKind.EOL

    def eos(self):
        """
        """
        return self._token.kind == TokenKind.EOS

    def validate(self):
        """
        """
        return True

    def get_content_position(self):
        """
        """
        return self._tokenizer.content.get_location(self._tokenizer.content_position)

    def next_lexeme(self):
        """
        """
        self._prev_token = deepcopy(self._token)
        if self._tokens:
            self._token = self._tokens.popleft()
        else:
            self._token = self._tokenizer.next_lexeme()
        self._statistics.update_stats(self._token)
        return self._token

    def lookahead_lexeme(self):
        """
        """
        token = self._tokenizer.next_lexeme()
        self._tokens.append(token)
        return token

    def take_snapshot(self):
        """
        Snapshot the current content position for backtracking.
        Usually called by parsers.
        """
        self._tokenizer.take_snapshot()

    def rewind_to_snapshot(self):
        """
        Restore the last saved content position for backtracking.
        Usually called by parsers.
        """
        self._tokenizer.rewind_to_snapshot()
