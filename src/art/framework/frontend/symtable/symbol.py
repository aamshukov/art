# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" IR (Intermediate Representation) symbol """
from art.framework.core.text.text import Text
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags
from art.framework.frontend.symtable.symbol_kind import SymbolKind


class Symbol(Entity):
    """
    IR (Intermediate Representation) symbol.
    """
    def __init__(self,
                 id,
                 label='',
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        Value: inferred value if any, might be integer value, real value or identifier (correlated with name).
        Metadata: attributes, annotations, etc.
        """
        super().__init__(id, value, attributes, flags, version)
        self.label = label
        self.grammar_symbol = None  # CFG (Context Free Grammar) parsed symbol
        self.token = None  # link with content
        self.kind = SymbolKind.UNKNOWN
        self.type = None  # ?? type
        self.machine_type = None  # ?? mapped type to machine specific representation
        self.offset = 0  # ?? run time offset
        self.size = 0  # ?? runtime size in bytes, might be aligned
        self.bits_size = 0  # ?? runtime size in bits

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.label))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      Text.equal(self.label, other.label))
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      Text.compare(self.label, other.label) < 0)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      Text.compare(self.label, other.label) <= 0)
        else:
            result = NotImplemented
        return result

    def validate(self):
        """
        """
        return True

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.label}"
