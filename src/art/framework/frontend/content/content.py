#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Content """
from art.framework.core.entity import Entity


class Content(Entity):
    """
    See OpenJDK for details
        ../src/jdk.compiler/share/classes/com/sun/tools/javac/util/Position.java
    """
    FIRST_LINE = 0
    FIRST_COLUMN = 0
    FIRST_POSITION = 0  # -> (FIRST_LINE, FIRST_COLUMN)

    def __init__(self,
                 id,
                 data,
                 source,  # origin of data - file path, DB schema, etc.
                 tab_size=4,  # tab size, default is 4 if == 0 - do not consider
                 version='1.0'):
        """
        """
        super().__init__(id, version=version)
        self._data = data
        self._count = len(data)
        self._source = source
        self._line_map = None  # start position of each line
        self._cached_line = Content.FIRST_LINE
        self._cached_position = Content.FIRST_POSITION
        self._tab_map = None  # tab positions
        self._tab_size = tab_size

    def __hash__(self):
        """
        """
        result = (super().__hash__() ^
                  hash(self._data) ^
                  hash(self._source))
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  self._data == other.data and
                  self._source == other.source)
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  self._data < other.data and
                  self._source < other.source)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  self._data <= other.data and
                  self._source <= other.source)
        return result

    @property
    def data(self):
        """
        """
        return self._data

    @property
    def count(self):
        """
        """
        return self._count

    @property
    def source(self):
        """
        """
        return self._source

    @property
    def tab_size(self):
        """
        """
        return self._tab_size

    def validate(self):
        """
        """
        return True

    def build_line_map(self):
        """
        """
        k = 0
        i = 0
        n = self._count
        d = self._data
        t = self._tab_size > 0  # consider tabs if tab size > 0
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
        if self._line_map is not None:
            self._line_map.clear()
        self._line_map = [line_map[j] for j in range(k)]
        if t:
            if self._tab_map is not None:
                self._tab_map.clear()
            self._tab_map = tab_map.copy()

    def get_line(self, position):
        """
        """
        if position != self._cached_position:
            self._cached_position = position
            lo = 0
            hi = len(self._line_map) - 1
            while lo <= hi:
                mid = (hi + lo) // 2
                mid_value = self._line_map[mid]
                if mid_value < position:
                    lo = mid + 1
                elif mid_value > position:
                    hi = mid - 1
                else:
                    result = mid  # no + 1, starts from 0
                    break
            else:
                result = lo - 1  # starts from 0
            self._cached_line = result
        else:
            result = self._cached_line
        return result

    def get_column(self, position):
        """
        """
        assert position < self._count, "Position out of range."
        line_start = self._line_map[self.get_line(position) - Content.FIRST_LINE]
        column = 0
        if self._tab_size > 0:  # consider tabs
            for k in range(line_start, position):
                if self._tab_map[k]:
                    column = (column // self._tab_size * self._tab_size) + self._tab_size
                else:
                    column += 1
        else:
            for k in range(line_start, position):
                column += 1
        return column + Content.FIRST_COLUMN
