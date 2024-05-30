#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art array type """
from collections import namedtuple
from art.framework.core.utils.flags import Flags
from art.language.art.type.art_type import ArtType
from art.language.art.type.art_type_kind import ArtTypeKind


class ArtArrayType(ArtType):
    """
    """
    ArrayBound = namedtuple('ArrayBound', 'lower_bound upper_bound')

    def __init__(self,
                 id,
                 label,
                 kind,
                 bounds,  # list of ArrayBound
                 underlying_type,
                 checked=True,
                 row_based=True,
                 layout=None,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        assert bounds, "Bounds must be greater than zero: scalar(0), vector/1D-array(1), matrix/2D-array(2), etc."
        super().__init__(id=id,
                         label=label,
                         kind=kind | ArtTypeKind.ARRAY_MASK,
                         cardinality=len(bounds),
                         layout=layout,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)
        self.bounds = bounds  # list of dimensions: ArrayBound(lower_bound=0, upper_bound)
        self.underlying_type = underlying_type
        self.checked = checked
        self.row_based = row_based

    def equivalent(self, other):
        """
        """
        return (ArtTypeKind.array(other.kind) and
                self.bounds == other.bounds and
                self.underlying_type.equivalent(other) and
                self.checked == other.checked and
                self.row_based == other.row_based and
                super().equivalent(other))

    def stringify(self):
        """
        """
        return f"{super().stringify()}:" \
               f"{self.underlying_type.label}:" \
               f"{str(self.bounds).strip('[]')}:" \
               f"{self.checked}"
