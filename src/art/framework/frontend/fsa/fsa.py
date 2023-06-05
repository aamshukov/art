# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" FSA """
from art.framework.core.graph import Graph


class Fsa(Graph):
    """
    """

    def __init__(self,
                 id,
                 label='',
                 version='1.0'):
        """
        """
        super().__init__(id, label, version=version)
        self._start_state = None
        self._final_states = list()

    @property
    def start_state(self):
        """
        """
        return self._start_state

    @start_state.setter
    def start_state(self, state):
        """
        """
        self._start_state = state

    @property
    def final_states(self):
        """
        """
        return self._final_states

    def add_final_state(self, state):
        """
        """
        assert self.is_final_state(state), "State already exists in final states."
        self._final_states.append(state)

    def is_start_state(self, id):
        """
        """
        return self.start_state is not None and self.start_state.id == id

    def is_final_state(self, id):
        """
        """
        return any(state.id == id for state in self.final_states)

    def add_state(self, state):
        """
        """
        self.add_vertex(state)

    def remove_state(self, state):
        """
        """
        self.remove_vertex(state)

    def add_transition(self, start_state, end_state, predicate):
        """
        """
        self.add_edge(start_state, end_state, predicate)

    def remove_transition(self, transition):
        """
        """
        self.remove_edge(transition)

    def combine(self, fsas):
        """
        Combines given FSAs into a FSA
          ... 15 ----> 16 ...
          ... 15 ----> 16 ...

             2 ---> 3
           ε/
          1
           ε\
             4 ---> 5
        """
        pass

    def concatenate(self, fsa1, fsa2):
        """
        Concatenates given two FSAs into a FSA
          ... 15 ----> 16 ...
          ... 15 ----> 16 ...

          1 ----> 2 ---> 3 ----> 4
                     ε
        """
        pass

    def generate_graphviz_content(self, path):
        """
        Generates Graphviz content into file.
        """
        pass
