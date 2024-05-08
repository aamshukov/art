# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Code """
import os
from art.framework.core.domain.base import Base


class Code(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.instructions = list()

    def add(self, instruction):
        """
        """
        self.instructions.append(instruction)

    def remove(self, instruction):
        """
        """
        self.instructions.remove(instruction)

    def clear(self):
        """
        """
        self.instructions.clear()

    def stringify(self):
        """
        """
        result = f'{os.linesep}'.join([instruction.stringify() for instruction in self.instructions])
        return result
