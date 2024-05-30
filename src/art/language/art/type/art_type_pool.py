#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art types pool """
from art.framework.core.domain.base import Base
from art.framework.core.patterns.singleton.singleton import singleton
from art.language.art.type.art_scalar_type import ArtScalarType
from art.language.art.type.art_type_kind import ArtTypeKind


@singleton
class ArtTypePool(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.types = dict()  # id:type
        self.build_types()

    def get_type(self, type):  # noqa
        """
        """
        result = None
        for value in self.types.values():
            if value.equivalent(type):
                result = value
                break
        return result

    # def build_types(self):
    #     """
    #     """
    #     self.types[ArtTypeKind.INTEGER_TYPE] = ArtScalarType(1,
    #                                                          'integer',
    #                                                          ArtTypeKind.INTEGER_TYPE)
    #     self.types[ArtTypeKind.REAL_TYPE] = ArtScalarType(2,
    #                                                       'real',
    #                                                       ArtTypeKind.REAL_TYPE)
    #     self.types[ArtTypeKind.STRING_TYPE] = ArtScalarType(3,
    #                                                         'string',
    #                                                         ArtTypeKind.STRING_TYPE)
    #     self.types[ArtTypeKind.BOOLEAN_TYPE] = ArtScalarType(4,
    #                                                          'boolean',
    #                                                          ArtTypeKind.BOOLEAN_TYPE)
