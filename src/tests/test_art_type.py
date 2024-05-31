#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.language.art.type.art_scalar_type import ArtScalarType
from art.language.art.type.art_type import ArtType
from art.language.art.type.art_type_kind import ArtTypeKind


class Test(unittest.TestCase):
    def test_art_scalar0_type_success(self):
        scalar = ArtScalarType(10, 'int', ArtTypeKind.INTEGER_TYPE)
        assert ArtTypeKind.scalar(scalar.kind)
        assert scalar.equivalent(scalar)

    def test_art_scalar1_type_success(self):
        scalar1 = ArtScalarType(10, 'int', ArtTypeKind.INTEGER_TYPE)
        assert ArtTypeKind.scalar(scalar1.kind)
        scalar2 = ArtScalarType(10, 'int', ArtTypeKind.INTEGER_TYPE)
        assert ArtTypeKind.scalar(scalar2.kind)
        assert scalar1.equivalent(scalar2)


if __name__ == '__main__':
    """
    """
    unittest.main()
