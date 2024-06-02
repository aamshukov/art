# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Tree """
from art.framework.core.text.text import Text
from art.framework.core.utils.flags import Flags
from art.framework.core.utils.colors import Colors
from art.framework.core.domain.entity import Entity
from art.framework.core.patterns.visitor.visitable import Visitable


class Tree(Entity, Visitable):
    """
    """
    def __init__(self,
                 id,
                 label='',
                 papa=None,
                 value=None,
                 attributes=None,
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 version='1.0'):
        """
        """
        super().__init__(id, value, attributes, flags, version)
        self.label = label
        self.color = color
        self.papa = papa
        self.kids = list()

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

    def insert_kid(self, kid, index=0):
        """
        """
        kid.papa = self
        self.kids.insert(index, kid)

    def add_kid(self, kid):
        """
        """
        kid.papa = self
        self.kids.append(kid)

    def remove_kid(self, kid):
        """
        """
        kid.papa = None
        self.kids.remove(kid)

    def validate(self):
        """
        """
        raise NotImplemented(self.validate.__qualname__)

    def accept(self, visitor, *args, **kwargs):
        """
        """
        visitor.visit(*args, **kwargs)

    def stringify(self):
        """
        """
        return f"{self.label}:{super().stringify()}"
