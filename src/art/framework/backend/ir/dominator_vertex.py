# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Code """
from art.framework.core.adt.graph.vertex import Vertex


class DominatorVertex(Vertex):
    """
    """
    def __init__(self,
                 id,
                 label='',
                 version='1.0'):
        """
        """
        super().__init__(id, label=label, version=version)
