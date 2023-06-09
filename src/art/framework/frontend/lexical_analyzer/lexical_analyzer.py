# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lexical Analyzer """
from collections import deque
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind


class LexicalAnalyzer(Entity):
    """
    """
    def __init__(self,
                 id,
                 content,
                 version='1.0'):
        """
        """
        super().__init__(id,  # master lexer, id = 0
                         version=version)
        self._content = content  # loaded content
        self._start_content = 0  # beginning of content
        self._end_content = self._start_content + self._content.count  # end of content, sentinel
        self._content_position = self._start_content  # current position in content
        self._lexeme_position = self._start_content  # beginning position of lexeme in content
        self._token = Token(TokenKind.UNKNOWN)  # current lexeme
        self._tokens = deque()  # queue of current and lookahead lexemes
        self._prev_token = self._token  # previous lexeme
        self._snapshots = deque()  # stack of backtracking snapshots - positions

    def __hash__(self):
        """
        """
        result = super().__hash__() ^ hash(self._token)
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self._token == other.token)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._token < other.token)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._token <= other.token)
        return result

    @property
    def token(self):
        """
        """
        return self._token

    @property
    def content(self):
        """
        """
        return self._content

    def validate(self):
        """
        """
        return True

    def eol(self):
        """
        """
        return self._token == TokenKind.EOL

    def eos(self):
        """
        """
        return self._token == TokenKind.EOS

    def next_lexeme(self):
        """
        """
        if not self.eos():
            self._prev_token = self._token
            if self._tokens:
                self._token = self._tokens.popleft()
                self._content_position = self._start_content + self._token.offset
            else:
                self.prolog()
                self.next_lexeme_impl()
                self.epilog()

    def prolog(self):
        """
        """
        self._token.reset()
        self._lexeme_position = self._content_position

    def epilog(self, update_stats=True):
        """
        """
        if self._content_position > self._end_content:
            self._content_position = self._end_content
        self._token.offset = self._lexeme_position - self._start_content
        self._token.length = self._content_position - self._lexeme_position
        self._token.flags = Flags.modify_flags(self._token.flags, Flags.CONTEXTUAL.VISITED, Flags.CLEAR)
        self._token.source = self._content.id
        if update_stats:
            Statistics().update_stats(self._token)

    def next_lexeme_impl(self):
        """
        """

    def lookahead_lexemes(self):
        """
        """
        if self.eos():
            result = self._token
        else:
            # push state
            cached_position = self._content_position
            cached_token = self._token
            # update state based on the last collected tokens
            if self._tokens:
                token = self._tokens[len(self._tokens) - 1]
                self._content_position = self._start_content + token.offset + token.length
            # get lexeme
            self.prolog()
            self.next_lexeme_impl()
            self.epilog(update_stats=False)
            # save new token
            if not self.eos() or (self._tokens and self._tokens[len(self._tokens) - 1].kind != TokenKind.EOS):
                self._tokens.append(self._token)
            # pop state
            self._content_position = cached_position
            self._token = cached_token
            # collect result
            result = self._tokens[len(self._tokens) - 1]
        return result

    def take_snapshot(self):
        """
        """
        self._snapshots.append(self._content_position)

    def rewind_to_snapshot(self):
        """
        Backtrack
        """
        if self._snapshots:
            self._content_position = self._snapshots.pop()
            self._token.reset()
            self._prev_token.reset()
            self._tokens.clear()
