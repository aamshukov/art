#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art type """
from art.framework.core.text.text import Text
from art.framework.core.utils.flags import Flags
from art.framework.frontend.type.type import Type


class ArtType(Type):
    """
    integer
    real
    string
    boolean

    struct <T <K, S = record <T <K, J>, U, integer=5, real=1> >, U, integer, real=1>
            T <K, S = record <T <K, J>, U, integer=5, real=1> >  U  integer  real
               K  S = record <T <K, J>, U, integer=5, real=1>
                      record <T <K, J>, U, integer    real
                              T <K, J>  U
                                 K  J
    """  # noqa
    def __init__(self,
                 id,
                 label,
                 kind,
                 cardinality=0,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id=id,
                         label=label,
                         kind=kind,
                         cardinality=cardinality,
                         value=value,
                         attributes=attributes,
                         flags=flags,
                         version=version)

    def equal(self, other):
        """
        """
        return self == other

    def equivalent(self, other):
        """
        """
        return (self.id == other.id and
                self.kind == other.kind and
                self.cardinality == other.cardinality and
                Text.equal(self.label, other.label))
