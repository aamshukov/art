#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Content """
from art.framework.core.base import Base


class Content(Base):
    """
    See OpenJDK for details
        ../src/jdk.compiler/share/classes/com/sun/tools/javac/util/Position.java
    """
    FIRST_LINE = 0
    FIRST_COLUMN = 0
    FIRST_POSITION = 0  # -> (FIRST_LINE, FIRST_COLUMN)

    def __init__(self,
                 data,
                 source,       # origin of data - file path, DB schema, etc.
                 tab_size=4):  # tab size, default is 4 if == 0 - do not consider
        """
        """
        super().__init__()
        self.data = data
        self.count = len(data)
        self.source = source
        self.line_map = None  # start position of each line
        self.cached_line = Content.FIRST_LINE
        self.cached_position = Content.FIRST_POSITION
        self.tab_map = None  # tab positions
        self.tab_size = tab_size

    def build_line_map(self):
        """
        """
        k = 0
        i = 0
        n = self.count
        d = self.data
        t = self.tab_size > 0  # consider tabs if tab size > 0
        line_map = [0] * n
        tab_map = [False] * (n if t else 0)
        while i < n:
            line_map[k] = i
            k += 1
            while True:
                ch = d[i]
                if (ch == 0x0000000D or  # '\r'
                        ch == 0x0000000A):  # '\n'
                    if ch == 0x0000000D and (i + 1) < n and d[i + 1] == 0x0000000A:
                        i += 2
                    else:
                        i += 1
                    break
                elif t and ch == 0x00000009:  # '\t'
                    tab_map[i] = True  # i is column
                i += 1
                if i >= n:
                    break
        if self.line_map is not None:
            self.line_map.clear()
        self.line_map = [line_map[j] for j in range(k)]
        if t:
            if self.tab_map is not None:
                self.tab_map.clear()
            self.tab_map = tab_map.copy()

    def build_char_line_map(self):
        """
        """
        k = 0
        i = 0
        n = self.count
        d = self.data
        t = self.tab_size > 0  # consider tabs if tab size > 0
        line_map = [0] * n
        tab_map = [False] * (n if t else 0)
        while i < n:
            line_map[k] = i
            k += 1
            while True:
                ch = d[i]
                if ch == '\r' or ch == '\n':
                    if (ch == '\r' and (i + 1) < n and d[i + 1] == '\n') or \
                       (ch == '\n' and (i + 1) < n and d[i + 1] == '\r'):
                        i += 2
                    else:
                        i += 1
                    break
                elif t and ch == '\t':
                    tab_map[i] = True  # i is column
                i += 1
                if i >= n:
                    break
        if self.line_map is not None:
            self.line_map.clear()
        self.line_map = [line_map[j] for j in range(k)]
        if t:
            if self.tab_map is not None:
                self.tab_map.clear()
            self.tab_map = tab_map.copy()

    def get_line(self, position):
        """
        """
        if position != self.cached_position:
            self.cached_position = position
            lo = 0
            hi = len(self.line_map) - 1
            while lo <= hi:
                mid = (hi + lo) // 2
                mid_value = self.line_map[mid]
                if mid_value < position:
                    lo = mid + 1
                elif mid_value > position:
                    hi = mid - 1
                else:
                    result = mid  # no + 1, starts from 0
                    break
            else:
                result = lo - 1  # starts from 0
            self.cached_line = result
        else:
            result = self.cached_line
        return result

    def get_column(self, position):
        """
        """
        assert position <= self.count, f"Position out of range, {position}:{self.count}."
        line_start = self.line_map[self.get_line(position) - Content.FIRST_LINE]
        column = 0
        if self.tab_size > 0:  # consider tabs
            for k in range(line_start, position):
                if self.tab_map[k]:
                    column = (column // self.tab_size * self.tab_size) + self.tab_size
                else:
                    column += 1
        else:
            for k in range(line_start, position):
                column += 1
        return column + Content.FIRST_COLUMN

    def get_location(self, position):
        """
        """
        line = self.get_line(position)
        column = self.get_column(position)
        return f'{line}:{column}'
