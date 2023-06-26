# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Grammar symbol """
from art.framework.core.flags import Flags
from art.framework.core.colors import Colors
from art.framework.core.text import Text
from art.framework.core.value import Value
from art.framework.core.visitable import Visitable


class GrammarSymbol(Value, Visitable):
    """
    """
    def __init__(self,
                 label='',
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(version)
        self._label = label
        self._flags = flags
        self._first_set = list()  # first set for k = 1
        self._first_set2 = list()  # first set for k = 2
        self._la_set = list()  # lookahead set for k = 1
        self._la_set2 = list()  # lookahead set for k = 2

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._label}:{self._version}:"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self._label)
        return result

    def __eq__(self, other):
        """
        """
        result = (super().__eq__(other) and
                  Text.equal(self._label, other.label))
        return result

    def __lt__(self, other):
        """
        """
        result = (super().__lt__(other) and
                  Text.compare(self._label, other.label) < 0)
        return result

    def __le__(self, other):
        """
        """
        result = (super().__le__(other) and
                  Text.compare(self._label, other.label) <= 0)
        return result

    @property
    def label(self):
        """
        """
        return self._label

    @label.setter
    def label(self, label):
        """
        """
        self._label = label

    @property
    def flags(self):
        """
        """
        return self._flags

    @flags.setter
    def flags(self, flags):
        """
        """
        self._flags = flags

    def validate(self):
        """
        """
        return True

    def accept(self, visitor, *args, **kwargs):
        """
        """
        pass
