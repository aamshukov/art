#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.domain.entity import Entity
from art.framework.core.utils.flags import Flags


class EntityTest(Entity):
    """
    """
    def __init__(self,
                 id,
                 label,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.label = label

    def stringify(self):
        """
        """
        return f"{self.label}:{super().stringify()}"


class Test(unittest.TestCase):
    def test_repr_str_success(self):
        et = EntityTest(1, "odin")
        repr1 = repr(et)
        str1 = str(et)
        assert repr1 == str1


if __name__ == '__main__':
    """
    """
    unittest.main()
