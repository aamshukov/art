# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" IR (Intermediate Representation) symbol """
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

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self.id}:{self.label}:{self.value}:" \
               f"({DomainHelper.dict_to_string(self.attributes)}):{self.version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self.label)
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

    def validate(self):
        """
        """
        return True
