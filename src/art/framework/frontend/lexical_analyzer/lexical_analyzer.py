# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lexical Analyzer """
from copy import deepcopy
from collections import deque
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.frontend.lexical_analyzer.tokenizer.token_factory import TokenFactory
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class LexicalAnalyzer(Entity):
    """
    """
    def __init__(self,
                 id,
                 tokenizer,
                 statistics,
                 diagnostics,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id,  # master lexer, id = 0
                         value,
                         attributes,
                         flags,
                         version)
        self.tokenizer = tokenizer
        self.token = TokenFactory.unknown_token()  # current lexeme
        self.tokens = deque()  # queue of lookahead (cached) lexemes
        self.prev_token = deepcopy(self.token)  # previous lexeme
        self.statistics = statistics
        self.diagnostics = diagnostics

    def __hash__(self):
        """
        """
        return super().__hash__()

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

    def eol(self):
        """
        """
        return self.token.kind == TokenKind.EOL

    def eos(self):
        """
        """
        return self.token.kind == TokenKind.EOS

    def validate(self):
        """
        """
        return True

    def get_content_position(self):
        """
        """
        return self.tokenizer.content.get_location(self.tokenizer.content_position)

    def next_lexeme(self):
        """
        """
        self.prev_token = deepcopy(self.token)
        if self.tokens:
            self.token = self.tokens.popleft()
        else:
            self.token = self.tokenizer.next_lexeme()
        self.statistics.update_stats(self.token)
        return self.token

    def lookahead_lexeme(self, skip=None):
        """
        """
        if skip:
            i = 0
            n = len(self.tokens)
            while i < n and self.tokens[i].kind in skip:
                i += 1
            if i < len(self.tokens):
                token = self.tokens[i]
            else:
                saved_token = deepcopy(self.token)
                saved_prev_token = deepcopy(self.prev_token)
                token = self.tokenizer.next_lexeme()
                self.tokens.append(token)
                while token.kind in skip:
                    token = self.tokenizer.next_lexeme()
                    self.tokens.append(token)
                self.token = saved_token
                self.prev_token = saved_prev_token
        else:
            if self.tokens:
                token = self.tokens[0]
            else:
                saved_token = deepcopy(self.token)
                saved_prev_token = deepcopy(self.prev_token)
                token = self.tokenizer.next_lexeme()
                self.tokens.append(token)
                self.token = saved_token
                self.prev_token = saved_prev_token
        return token

    def lookahead_lexemes(self, k=1):
        """
        """
        assert k > 0, f"Number of look ahead tokens must be greater than zero, {k} specified."
        tokens = list()
        i = 0
        n = len(self.tokens)
        while i < n:
            tokens.append(self.tokens[i])
            i += 1
        saved_token = deepcopy(self.token)
        saved_prev_token = deepcopy(self.prev_token)
        while i < k:
            token = self.tokenizer.next_lexeme()
            tokens.append(token)
            self.tokens.append(token)
            i += 1
        self.token = saved_token
        self.prev_token = saved_prev_token
        return tokens

    def take_snapshot(self):
        """
        Snapshot the current content position for backtracking.
        Usually called by parsers.
        """
        self.tokenizer.take_snapshot()

    def rewind_to_snapshot(self):
        """
        Restore the last saved content position for backtracking.
        Usually called by parsers.
        """
        self.token.reset()
        self.tokens.clear()
        self.prev_token.reset()
        self.tokenizer.rewind_to_snapshot()

    def discard_snapshot(self):
        """
        Discard the last saved content position for backtracking.
        Usually called by lexical analyzers.
        """
        self.tokenizer.discard_snapshot()
