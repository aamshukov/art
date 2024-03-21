# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lexical Analyzer """
from collections import deque
from copy import deepcopy
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags
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
        self.prev_token = deepcopy(self.token)  # previous lexeme
        self.tokens = deque()  # queue of lookahead (cached) lexemes
        self.statistics = statistics
        self.diagnostics = diagnostics

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__eq__(other)
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__lt__(other)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = super().__le__(other)
        else:
            result = NotImplemented
        return result

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
        if self.tokens:
            state = self.tokens.popleft()
            self.tokenizer.rewind(state)
            self.token = deepcopy(self.tokenizer.token)
            self.prev_token = deepcopy(self.tokenizer.prev_token)
        else:
            self.prev_token = deepcopy(self.token)
            self.token = self.tokenizer.next_lexeme()
        self.statistics.update_stats(self.token)
        return self.token

    def lookahead_lexeme(self, skip=None):
        """
        """
        if skip:
            i = 0
            n = len(self.tokens)
            while i < n and self.tokens[i][3].kind in skip:  # [3] - token
                i += 1
            if i < len(self.tokens):
                token = self.tokens[i][3]
            else:
                state = self.tokenizer.snapshot(persist=False)
                token = self.tokenizer.next_lexeme()
                self.tokens.append(self.tokenizer.snapshot(persist=False))
                while token.kind in skip:
                    token = self.tokenizer.next_lexeme()
                    self.tokens.append(self.tokenizer.snapshot(persist=False))
                self.tokenizer.rewind(state)
        else:
            if self.tokens:
                token = self.tokens[0][3]
            else:
                state = self.tokenizer.snapshot(persist=False)
                token = self.tokenizer.next_lexeme()
                self.tokens.append(self.tokenizer.snapshot(persist=False))
                self.tokenizer.rewind(state)
        return token

    def lookahead_lexemes(self, k=1):
        """
        """
        assert k > 0, f"Number of look ahead tokens must be greater than zero, {k} specified."
        i = 0
        tokens = list()
        state = self.tokenizer.snapshot(persist=False)
        while i < k:
            token = self.tokenizer.next_lexeme()
            tokens.append(token)
            i += 1
        self.tokenizer.rewind(state)
        return tokens

    def reset(self):
        """
        """
        self.token = TokenFactory.unknown_token()
        self.prev_token = deepcopy(self.token)
        self.tokens.clear()

    def snapshot(self):
        """
        """
        self.tokenizer.snapshot()
        self.tokens.clear()

    def rewind(self):
        """
        """
        self.tokenizer.rewind()
        self.token = deepcopy(self.tokenizer.token)
        self.prev_token = deepcopy(self.tokenizer.prev_token)
