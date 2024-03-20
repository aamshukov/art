# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Tree """
from art.framework.core.utils.helper import DomainHelper
from art.framework.core.utils.flags import Flags
from art.framework.core.utils.colors import Colors
from art.framework.core.domain.entity import Entity
from art.framework.core.patterns.visitable import Visitable


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
        return True

    def accept(self, visitor, *args, **kwargs):
        """
        """
        raise NotImplemented(self.accept.__qualname__)
