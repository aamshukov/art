# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" FSA """
from art.framework.core.flags import Flags
from art.framework.core.text import Text
from art.framework.core.graph import Graph


class Fsa(Graph):
    """
    """
    def __init__(self,
                 id=0,
                 label='',
                 value=None,       # graph specific value
                 attributes=None,  # graph specific attributes
                 flags=Flags.CLEAR,
                 version='1.0'):
        """
        """
        super().__init__(id, label, value, attributes, flags, digraph=True, version=version)
        self.start_state = None
        self.final_states = list()

    @property
    def states(self):
        """
        """
        return self.vertices

    def add_final_state(self, state):
        """
        """
        assert not self.is_final_state(state), "State already exists in final states."
        self.final_states.append(state)

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

    @property
    def transitions(self):
        """
        """
        return self.edges

    def add_transition(self, start_state, end_state, predicate):
        """
        """
        self.add_edge(start_state, end_state, predicate)

    def remove_transition(self, transition):
        """
        """
        self.remove_edge(transition)

    @staticmethod
    def empty_predicate():
        """
        """
        return ''

    @staticmethod
    def epsilon_transition(predicate):
        return Text.epsilon(predicate)

    def combine(self, fsas):  # noqa
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
        Generates Graphviz content.
        """
        assert path is not None, "Invalid argument 'path'."

        def get_state_label(_state):
            return f'"{_state.label}_{_state.id}_{_state.token}"'

        indent = '    '
        linesep = '\n'
        with open(path, 'wt') as stream:
            stream.write(f"digraph FSA{linesep}")
            stream.write(f"{{{linesep}")
            if self.final_states:
                stream.write(f"{indent}node [shape = doublecircle];{linesep}")
                line = indent
                for state in self.final_states:
                    line += f"{get_state_label(state)} "
                line += f";{linesep}"
                stream.write(line)
            stream.write(f"{indent}node [shape = circle];{linesep}")
            stream.write(f"{indent}rankdir = LR;{linesep}")
            line = indent
            for state in self.states.values():
                line += f"{get_state_label(state)} "
            line += f";{linesep}"
            stream.write(line)
            for transition in self.transitions.values():
                line = indent
                start_state, end_state = transition.uv
                line += f"{get_state_label(start_state)} -> {get_state_label(end_state)}"
                predicate = ''
                if transition.value:
                    predicate = transition.value
                line += f' [label = "{predicate}"];{linesep}'
                stream.write(line)
            stream.write(f"}}")
