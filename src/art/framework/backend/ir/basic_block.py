# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Code """
import os
from art.framework.backend.ir.dominator_vertex import DominatorVertex


class BasicBlock(DominatorVertex):
    """
    """
    def __init__(self,
                 id,
                 label='',
                 version='1.0'):
        """
        """
        super().__init__(id, label=label, version=version)

    def stringify(self):
        """
        """
        #?? result = f'{os.linesep}'.join([instruction.stringify() for instruction in self.instructions])
        # return result
