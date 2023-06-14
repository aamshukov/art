# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Tokenizer """
from copy import deepcopy
from collections import deque
from abc import abstractmethod
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind


class Tokenizer(Entity):
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
        self._snapshots = deque()  # stack of backtracking snapshots - positions

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
    def content(self):
        """
        """
        return self._content

    def advance_codepoint(self):
        """
        """
        if self._content_position < self._end_content:
            result = self._content[self._content_position]
            self._content_position += 1
        else:
            result = Text.eos_codepoint()
        return result

    def revoke_codepoint(self):
        """
        """
        if self._content_position > self._start_content:
            self._content_position -= 1
        result = self._content[self._content_position]
        return result

    def peek_codepoint(self):
        """
        """
        if self._content_position + 1 < self._end_content:
            result = self._content[self._content_position + 1]
        else:
            result = Text.eos_codepoint()
        return result

    def next_lexeme(self):
        """
        """
        self.prolog()
        self.next_lexeme_impl()
        self.epilog()
        return deepcopy(self._token)

    def prolog(self):
        """
        """
        self._token.reset()
        self._lexeme_position = self._content_position

    def epilog(self):
        """
        """
        if self._content_position > self._end_content:
            self._content_position = self._end_content
        self._token.offset = self._lexeme_position - self._start_content
        self._token.length = self._content_position - self._lexeme_position
        self._token.literal = self._content.data[self._token.offset: self._token.offset + self._token.length]
        self._token.source = self._content.id
        self._token.flags = Flags.modify_flags(self._token.flags, Flags.CONTEXTUAL.VISITED, Flags.CLEAR)

    @abstractmethod
    def next_lexeme_impl(self):
        """
        """
        raise NotImplemented(self.next_lexeme_impl.__qualname__)

    def take_snapshot(self):
        """
        Snapshot the current content position for backtracking.
        Usually called by lexical analyzers.
        """
        self._snapshots.append(self._content_position)

    def rewind_to_snapshot(self):
        """
        Restore the last saved content position for backtracking.
        Usually called by lexical analyzers.
        """
        if self._snapshots:
            self._content_position = self._snapshots.pop()
