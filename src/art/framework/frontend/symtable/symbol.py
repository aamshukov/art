# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" IR (Intermediate Representation) symbol """
from art.framework.core.entity import Entity
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.frontend.symtable.symbol_kind import SymbolKind


class Symbol(Entity):
    """
    IR (Intermediate Representation) symbol.
    """
    def __init__(self,
                 id,
                 label='',
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, version)
        self._label = label
        self._grammar_symbol = None  # CFG (Context Free Grammar) parsed symbol
        self._token = None  # link with content
        self._value = None  # inferred value if any, might be integer value,
                            # real value or identifier (correlated with name)
        self._kind = SymbolKind.UNKNOWN
        self._type = None  # ?? type
        self._machine_type = None  # ?? mapped type to machine spcific representation
        self._offset = 0  # ?? run time offset
        self._size = 0  # ?? runtime size in bytes, might be aligned
        self._bits_size = 0  # ?? runtime size in bits
        self._flags = flags
        self._metadata = dict()  # attributes, annotations, etc.

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self._id}:{self._label}:{self._version}:"

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

    @property
    def grammar_symbol(self):
        """
        """
        return self._grammar_symbol

    @grammar_symbol.setter
    def grammar_symbol(self, grammar_symbol):
        """
        """
        self._grammar_symbol = grammar_symbol
