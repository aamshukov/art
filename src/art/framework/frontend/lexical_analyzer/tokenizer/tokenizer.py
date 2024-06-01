# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Tokenizer """
from copy import deepcopy
from collections import deque
from abc import abstractmethod
from art.framework.core.diagnostics.code import Code
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags
from art.framework.core.diagnostics.status import Status
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.text.text import Text
from art.framework.frontend.content.location import Location
from art.framework.frontend.lexical_analyzer.tokenizer.token_factory import TokenFactory


class Tokenizer(Entity):
    """
    """
    def __init__(self,
                 id,
                 content,
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
        self.content = content  # loaded content
        self.start_content = 0  # beginning of content
        self.end_content = self.start_content + self.content.count  # end of content, sentinel
        self.content_position = self.start_content - 1  # current position in content
        self.codepoint = Text.eos_codepoint()
        self.lexeme_position = self.content_position  # beginning position of lexeme in content
        self.token = TokenFactory.unknown_token()  # current lexeme
        self.prev_token = self.token
        self.snapshots = deque()  # stack of backtracking snapshots - positions
        self.escaped = False  # True if codepoint has been derived from escape sequence
        self.statistics = statistics
        self.diagnostics = diagnostics
        self.advance()

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

    @property
    def character(self):
        """
        """
        return chr(self.codepoint)

    def calculate_codepoint(self, content_position, n):
        """
        Return True if sequence of digits is correct.
        """
        k = 0
        result = 0
        valid = True
        for k in range(n):
            if content_position == self.end_content:
                result = 0
                valid = False
                self.diagnostics.add(Status(f'Invalid unicode escape sequence length at '
                                            f'{self.content.get_location(content_position)}',
                                            'tokenizer',
                                            Code.INVALID_UNICODE_ESCAPE))
                break
            codepoint = self.content.data[content_position]
            if Text.hexadecimal_digit(codepoint):
                result = (result << 4) | Text.ascii_digit(codepoint)
                content_position += 1
            else:
                self.diagnostics.add(Status(f'Invalid unicode escape sequence (digits) at '
                                            f'{self.content.get_location(content_position)}',
                                            'tokenizer',
                                            Code.INVALID_UNICODE_ESCAPE))
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

    def consume_unicode_escape(self, mode, content_position):
        """
        Parse unicode escape(s):
            '\'uHexDigitHexDigitHexDigitHexDigit - up to 0xFFFF
            '\'uHexDigitHexDigitHexDigitHexDigit
            '\'uHexDigitHexDigitHexDigitHexDigit - up to 0x10FFFF with surrogates
            '\'UHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigitHexDigit - codepoint
        At this point current position points to '\\'.
        """
        def squash_unicode_prefixes(_content_position):
            while (_content_position < self.end_content and  # consume (squash) unicode escape prefixes as in Java
                   Tokenizer.unicode_escape_prefix(self.content.data[_content_position])):
                _content_position += 1
            return _content_position

        result = Text.BAD_CODEPOINT
        content_position = squash_unicode_prefixes(content_position + 1)  # +1, skip '\\'
        escape_seq_len = 4 if mode == 'u' else 8
        valid, codepoint, content_position = self.calculate_codepoint(content_position, escape_seq_len)
        if valid:
            if mode == 'u':
                if Text.high_surrogate(codepoint):
                    if Tokenizer.unicode_escape_prefix(self.peek_at(content_position)):
                        high_surrogate = codepoint
                        content_position = squash_unicode_prefixes(content_position + 1)  # +1, skip '\\'
                        valid, low_surrogate, content_position = self.calculate_codepoint(content_position,
                                                                                          escape_seq_len)
                        if valid and Text.low_surrogate(low_surrogate):
                            result = Text.make_codepoint(high_surrogate, low_surrogate)
                        else:
                            self.diagnostics.add(Status(f'Invalid unicode escape sequence, invalid low surrogate '
                                                        f'at {self.content.get_location(content_position)}',
                                                        'tokenizer',
                                                        Code.INVALID_UNICODE_ESCAPE))
                    else:
                        self.diagnostics.add(Status(f'Invalid unicode escape sequence, missing low surrogate '
                                                    f'at {self.content.get_location(content_position)}',
                                                    'tokenizer',
                                                    Code.INVALID_UNICODE_ESCAPE))
                else:
                    if Text.ascii(codepoint) or not Text.low_surrogate(codepoint):
                        result = codepoint
                    else:
                        self.diagnostics.add(Status(f'Invalid unicode escape sequence, invalid high surrogate '
                                                    f'at {self.content.get_location(content_position)}',
                                                    'tokenizer',
                                                    Code.INVALID_UNICODE_ESCAPE))
            else:  # mode == U
                result = codepoint
        return result, content_position - 1

    def consume_escape(self):
        """
        """
        content_position = self.content_position + 1  # skip '\'
        codepoint = self.content.data[content_position]
        match codepoint:
            case 0x00000061:  # 'a'
                codepoint = 0x07
            case 0x00000062:  # 'b'
                codepoint = 0x08
            case 0x00000074:  # 't'
                codepoint = 0x09
            case 0x00000076:  # 'v'
                codepoint = 0x0B
            case 0x0000006E:  # 'n'
                codepoint = 0x0A
            case 0x00000066:  # 'f'
                codepoint = 0x0C
            case 0x00000072:  # 'r'
                codepoint = 0x0D
            case 0x00000022:  # '"'
                codepoint = 0x22
            case 0x00000027:  # '\''
                codepoint = 0x27
            case 0x0000005C:  # '\\':
                codepoint = 0x5C
            case 'N':
                # \N{name}
                # NAME in the Unicode.
                # NOT IMPLEMENTED
                codepoint = Text.ERRONEOUS_CODEPOINT
                self.diagnostics.add(Status(f'Escape \\N(name) is not implemented, at '
                                            f'{self.content.get_location(self.content_position)}',
                                            'tokenizer',
                                            Code.INVALID_LITERAL))
            case 'x':
                # \xh
                # \xhh
                # NOT IMPLEMENTED
                codepoint = Text.ERRONEOUS_CODEPOINT
                self.diagnostics.add(Status(f'Escape \\xhh is not implemented, at '
                                            f'{self.content.get_location(self.content_position)}',
                                            'tokenizer',
                                            Code.INVALID_LITERAL))
            case (0x00000030 |  # 0
                  0x00000031 |  # 1
                  0x00000032 |  # 2
                  0x00000033 |  # 3
                  0x00000034 |  # 4
                  0x00000035 |  # 5
                  0x00000036 |  # 6
                  0x00000037):  # 7
                # may start octal, up to 377, sequence
                d1 = codepoint = Text.ascii_digit(codepoint)
                d2 = self.peek_at(content_position)
                if 0x00000030 <= d2 <= 0x00000037:
                    content_position += 1
                    codepoint = codepoint * 8 + Text.ascii_digit(d2)
                    d3 = self.peek_at(content_position)
                    if d1 <= 3 and (0x00000030 <= d3 <= 0x00000037):
                        content_position += 1
                        codepoint = codepoint * 8 + Text.ascii_digit(d3)
            case _:
                self.diagnostics.add(Status(f'Invalid escape literal at '
                                            f'{self.content.get_location(self.content_position)}',
                                            'tokenizer',
                                            Code.INVALID_LITERAL))
                codepoint = Text.ERRONEOUS_CODEPOINT
        return codepoint, content_position

    def advance(self):
        """
        Content is represented as string of codepoints.
        """
        self.escaped = False
        self.content_position += 1
        if self.content_position < self.end_content:
            self.codepoint = self.content.data[self.content_position]
            if Text.back_slash(self.codepoint):
                prefix = self.peek()
                if Tokenizer.unicode_escape_prefix(prefix):  # '\' might start unicode escape sequence
                    mode = 'u' if prefix == 0x00000075 else 'U'
                    self.codepoint, self.content_position =\
                        self.consume_unicode_escape(mode, self.content_position)
                else:
                    self.codepoint, self.content_position = self.consume_escape()
                self.escaped = True
        else:
            self.codepoint = Text.eos_codepoint()
        if self.content_position > self.end_content:
            self.content_position = self.end_content
        assert Text.valid_codepoint(self.codepoint)
        return self.codepoint

    def peek(self):
        """
        Lookahead.
        """
        if self.content_position + 1 < self.end_content:
            result = self.content.data[self.content_position + 1]
        else:
            result = Text.eos_codepoint()
        return result

    def peek_at(self, content_position):
        """
        Lookahead at.
        """
        if content_position + 1 < self.end_content:
            result = self.content.data[content_position + 1]
        else:
            result = Text.eos_codepoint()
        return result

    def next_lexeme(self):
        """
        """
        self.prolog()
        self.next_lexeme_impl()
        self.epilog()
        return deepcopy(self.token)

    def prolog(self):
        """
        """
        self.prev_token = deepcopy(self.token)
        self.token.reset()
        self.lexeme_position = self.content_position

    def epilog(self):
        """
        """
        if self.content_position > self.end_content:
            self.content_position = self.end_content
        self.token.location = Location(self.lexeme_position - self.start_content,
                                       self.content_position - self.lexeme_position,
                                       self.content.source)
        self.token.literal = ''.join(chr(codepoint) for codepoint in
                                     self.content.data[self.token.location.offset:
                                                       self.token.location.offset + self.token.location.length])
        self.token.flags = DomainHelper.modify_flags(self.token.flags, Flags.PROCESSED, Flags.CLEAR)

    @abstractmethod
    def next_lexeme_impl(self):
        """
        """
        raise NotImplemented(self.next_lexeme_impl.__qualname__)

    @abstractmethod
    def snapshot(self, offset=0, persist=False):
        """
        Snapshot the current state for backtracking.
        Usually called by lexical analyzers.
        """
        raise NotImplemented(self.snapshot.__qualname__)

    @abstractmethod
    def rewind(self, state=None):
        """
        Restore the last saved state for backtracking.
        Usually called by lexical analyzers.
        """
        raise NotImplemented(self.rewind.__qualname__)

    def discard(self):
        """
        Discard the last saved state for backtracking.
        Usually called by lexical analyzers.
        """
        if self.snapshots:
            self.snapshots.pop()

    @abstractmethod
    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)

    def stringify(self):
        """
        """
        return f"{super().stringify()}"
