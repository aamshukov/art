# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Vertex """
from collections import namedtuple
from art.framework.core.text.text import Text
from art.framework.core.utils.flags import Flags
from art.framework.core.utils.colors import Colors
from art.framework.core.domain.entity import Entity
from art.framework.core.patterns.visitor.visitable import Visitable


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

    def __hash__(self):
        """
        """
        return hash((super().__hash__(), self.__class__, self.label))

    def __eq__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__eq__(other) and
                      Text.equal(self.label, other.label))
        else:
            result = NotImplemented
        return result

    def __lt__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__lt__(other) and
                      Text.compare(self.label, other.label) < 0)
        else:
            result = NotImplemented
        return result

    def __le__(self, other):
        """
        """
        if other.__class__ is self.__class__:
            result = (super().__le__(other) and
                      Text.compare(self.label, other.label) <= 0)
        else:
            result = NotImplemented
        return result

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

    def stringify(self):
        """
        """
        return f"{super().stringify()}:{self.label}"
