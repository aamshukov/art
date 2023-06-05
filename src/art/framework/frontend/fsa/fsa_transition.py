# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" FSA transition """
from art.framework.core.text import Text
from art.framework.core.edge import Edge


class FsaTransition(Edge):
    """
    """

    def __init__(self,
                 id,
                 endpoints,
                 predicate=None,
                 version='1.0'):
        """
        """
        super().__init__(id, endpoints, predicate, version=version)

    def is_epsilon_transition(self):
        return Text.equal(self.predicate, Text.epsilon())

    @property
    def predicate(self):
        """
        """
        return self.value

    @staticmethod
    def empty_predicate(self):
        """
        """
        return ''
