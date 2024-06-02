# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Basic block """
from art.framework.backend.ir.code import Code
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
        self.code = Code()
        self.ins = list()
        self.outs = list()
        self.defs = list()
        self.uses = list()

    def stringify(self):
        """
        """
        return f"{self.code}:{super().stringify()}"
