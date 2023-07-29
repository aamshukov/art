# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from collections import namedtuple
from art.framework.core.flags import Flags
from art.framework.core.colors import Colors
from art.framework.core.domain_helper import DomainHelper
from art.framework.core.entity import Entity
from art.framework.core.visitable import Visitable


class Vertex(Entity, Visitable):
    """
    """
    AdjValue = namedtuple('AdjValue', 'vertex edge')

    def __init__(self,
                 id,
                 label='',
                 value=None,        # vertex specific value
                 attributes=None,   # vertex specific attributes
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.label = label
        self.color = color
        self.adjacencies = list()  # list of Vn/Em pairs (AdjValue)

    def __repr__(self):
        """
        """
        return f"{type(self).__name__}:{self.id}:{self.label}:{self.value}:" \
               f"({DomainHelper.dict_to_string(self.attributes)}):{self.version}"

    __str__ = __repr__

    def __hash__(self):
        """
        """
        result = super().__hash__()
        result ^= hash(self.label)
        return result

    def __eq__(self, other):
        """
        """
        return super().__eq__(other)

    def __lt__(self, other):
        """
        """
        return super().__lt__(other)

    def __le__(self, other):
        """
        """
        return super().__le__(other)

    @property
    def edges(self):
        """
        """
        return [adj.edge for adj in self.adjacencies]

    def add_adjacence(self, vertex, edge):
        """
        """
        self.adjacencies.append(Vertex.AdjValue(vertex, edge))

    def remove_adjacence(self, vertex, edge):
        """
        """
        self.adjacencies.remove(Vertex.AdjValue(vertex, edge))

    def validate(self):
        """
        """
        return True

    def accept(self, visitor, *args, **kwargs):
        """
        """
        visitor.visit(self, *args, **kwargs)
