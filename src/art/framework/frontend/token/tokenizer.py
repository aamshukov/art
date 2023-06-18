# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Tokenizer """
from copy import deepcopy
from collections import deque
from abc import abstractmethod
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.core.status import Status
from art.framework.core.text import Text
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind


class Tokenizer(Entity):
    """
    """
    def __init__(self,
                 id,
                 content,
                 statistics,
                 diagnostics,
                 version='1.0'):
        """
        """
        super().__init__(id,  # master lexer, id = 0
                         version=version)
        self._content = content  # loaded content
        self._start_content = 0  # beginning of content
        self._end_content = self._start_content + self._content.count  # end of content, sentinel
        self._content_position = self._start_content - 1  # current position in content
        self._lexeme_position = self._start_content  # beginning position of lexeme in content
        self._token = Token(TokenKind.UNKNOWN)  # current lexeme
        self._snapshots = deque()  # stack of backtracking snapshots - positions
        self._unicode_backslash_count = 0  # tracks how many '\' has been observed
        self._codepoint = Text.eos_codepoint()
        self._statistics = statistics
        self._diagnostics = diagnostics
        self.next_codepoint()  #

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
    def codepoint(self):
        """
        """
        return self._codepoint

    @property
    def character(self):
        """
        """
        return chr(self._codepoint)

    @property
    def content(self):
        """
        """
        return self._content

    def calculate_codepoint(self, content_position, n):
        """
        Return True if sequence of digits is correct.
        """
        k = 0
        result = 0
        valid = True
        for k in range(n):
            if content_position == self._end_content:
                result = 0
                valid = False
                self._diagnostics.add(Status(f'Invalid unicode escape sequence length at'
                                             f'{self.content.get_location(content_position)}',
                                             'tokenizer',
                                             Status.INVALID_UNICODE_ESCAPE))
                break
            codepoint = self._content.data[content_position]
            if Text.hexadecimal_digit(codepoint):
                result = (result << 4) | Text.ascii_number(codepoint)
                content_position += 1
            else:
                self._diagnostics.add(Status(f'Invalid unicode escape sequence (digits) at'
                                             f'{self.content.get_location(content_position)}',
                                             'tokenizer',
                                             Status.INVALID_UNICODE_ESCAPE))
                result = 0
                valid = False
                break
        return valid, result, content_position

    @staticmethod
    def unicode_escape_prefix(codepoint):
        """
        Return u or U.
        """
        return (codepoint == 0x00000075 or  # 'u'
                codepoint == 0x00000055)    # 'U'

    def consume_unicode_escape(self, mode, content_position, check_for_surrogates=True):
        """
        Parce unicode escape(s):
            '\'uHexDigitHexDigitHexDigitHexDigit - up to 0xFFFF
            '\'uHexDigitHexDigitHexDigitHexDigit
            '\'uHexDigitHexDigitHexDigitHexDigit - up to 0x10FFFF with surrogates
            '\'UHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigit - codepoint
        At this point current position points to '\\'.
        """
        result = Text.BAD_CODEPOINT
        content_position = content_position + 1  # skip '\\'
        while (content_position < self._end_content and  # consume (squash) unicode escape prefixes as in Java
               Tokenizer.unicode_escape_prefix(self._content.data[content_position])):
            content_position += 1
        valid, codepoint, content_position = self.calculate_codepoint(content_position, 4 if mode == 'u' else 8)
        if valid:
            if mode == 'u':
                if check_for_surrogates:
                    if Text.high_surrogate(codepoint):
                        if Tokenizer.unicode_escape_prefix(self.peek_codepoint()):
                            high_surrogate = codepoint
                            low_surrogate, content_position = self.consume_unicode_escape(mode,
                                                                                          content_position,
                                                                                          check_for_surrogates=False)
                            if Text.low_surrogate(low_surrogate):
                                result = Text.make_codepoint(high_surrogate, low_surrogate)
                            else:
                                self._diagnostics.add(Status(f'Invalid unicode escape sequence, invalid low surrogate '
                                                             f'at {self.content.get_location(content_position)}',
                                                             'tokenizer',
                                                             Status.INVALID_UNICODE_ESCAPE))
                        else:
                            self._diagnostics.add(Status(f'Invalid unicode escape sequence, missing low surrogate '
                                                         f'at {self.content.get_location(content_position)}',
                                                         'tokenizer',
                                                         Status.INVALID_UNICODE_ESCAPE))
                    else:
                        if Text.ascii(codepoint) or not Text.low_surrogate(codepoint):
                            result = codepoint
                            content_position -= 1
                        else:
                            self._diagnostics.add(Status(f'Invalid unicode escape sequence, invalid high surrogate '
                                                         f'at {self.content.get_location(content_position)}',
                                                         'tokenizer',
                                                         Status.INVALID_UNICODE_ESCAPE))
                else:
                    result = codepoint
                    content_position -= 1
            else:  # mode == U
                result = codepoint
                content_position -= 1
        return result, content_position

    def next_codepoint(self):
        """
        Content is represented as string with 'virtual' codepoints.
        To deal with genuine codepoints content must be loaded with to_codepoints=True.
        """
        self._content_position += 1
        if self._content_position < self._end_content:
            self._codepoint = self._content.data[self._content_position]
            if Text.back_slash(self._codepoint):
                if self._unicode_backslash_count % 2 == 0:  # '\' might start unicode escape sequence
                    prefix = self.peek_codepoint()          # check for single '\': ..._count = 0, 2, etc.
                    if Tokenizer.unicode_escape_prefix(prefix):
                        mode = 'u' if prefix == 0x00000075 else 'U'
                        self._codepoint, self._content_position = self.consume_unicode_escape(mode,
                                                                                              self._content_position)
                    else:
                        self._unicode_backslash_count += 1
                else:
                    self._unicode_backslash_count += 1  # single '\'
            else:
                self._unicode_backslash_count = 0
        else:
            self._codepoint = Text.eos_codepoint()
        if self._content_position > self._end_content:
            self._content_position = self._end_content
        return self._codepoint

    def peek_codepoint(self):
        """
        """
        if self._content_position + 1 < self._end_content:
            result = self._content.data[self._content_position + 1]
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
