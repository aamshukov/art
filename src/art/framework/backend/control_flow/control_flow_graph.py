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
        # phase I (collect leaders)
        #   1. Первая команда (instruction) промежуточного кода является лидером. # noqa
        #   2. Любая команда (instruction), являющаяся целевой для условного или безусловного перехода, # noqa
        #      является лидером. # noqa
        #   3. Любая команда (instruction), следующая непосредственно за условным или безусловным # noqa
        #      переходом or 'return', является лидером. # noqa



        # phase II (build basic blocks)  # noqa
        #  1. Базовый блок каждого лидера определяется как содержащий самого лидера и все команды до # noqa
        #     (но не включая) следующего лидера или до конца промежуточной программы. # noqa


        # phase III (build CFG)


        return basic_blocks
