# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Control flow graph """
from art.framework.core.adt.graph.graph import Graph
from art.framework.core.domain.base import Base


class ControlFlowGraph(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def collect_basic_blocks(code):
        """
        """
        basic_blocks = Graph(id=1,
                             label=f"{ControlFlowGraph.__qualname__}",
                             digraph=True)
        return basic_blocks
