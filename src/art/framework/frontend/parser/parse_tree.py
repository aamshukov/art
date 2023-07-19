#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Parse tree """
from art.framework.core.colors import Colors
from art.framework.core.flags import Flags
from art.framework.core.graph_algorithms import GraphAlgorithms
from art.framework.core.tree import Tree


class ParseTree(Tree):
    """
    """
    def __init__(self,
                 id,
                 kind,
                 label='',
                 value=None,  # IR backend symbol
                 attributes=None,
                 flags=Flags.CLEAR,
                 color=Colors.UNKNOWN,
                 papa=None,
                 version='1.0'):
        """
        """
        super().__init__(id,
                         label,
                         value,
                         attributes,
                         flags,
                         color,
                         papa,
                         version)
        self._kind = kind

    @property
    def kind(self):
        """
        """
        return self._kind

    @kind.setter
    def kind(self, kind):
        """
        """
        self._kind = kind

    @property
    def symbol(self):
        """
        """
        return self._value

    @symbol.setter
    def symbol(self, symbol):
        """
        """
        self._value = symbol

    def validate(self):
        """
        """
        return True

    def accept(self, visitor, *args, **kwargs):
        """
        """
        def default_action(_tree, *_args, **_kwargs):
            visitor.visit(_tree, *_args, **_kwargs)

        preorder_action = kwargs.pop('preorder', '')
        postorder_action = None
        if not preorder_action:
            postorder_action = kwargs.pop('postorder', '')
            if not postorder_action:
                preorder_action = default_action
        GraphAlgorithms.calculate_tree_traverses(self,
                                                 preorder_action=preorder_action,
                                                 postorder_action=postorder_action)

    # def accept(self, visitor, *args, **kwargs):
    #     """
    #     """
    #     recursive = False
    #     if 'recursive' in kwargs:
    #         recursive = kwargs['recursive']
    #     if recursive:
    #         if (self._flags & Flags.VISITED) != Flags.VISITED:
    #             self._flags = Flags.modify_flags(self._flags, Flags.VISITED, Flags.CLEAR)
    #             visitor.visit(self, *args, **kwargs)
    #             for kid in self._kids:
    #                 if (kid.flags & Flags.VISITED) != Flags.VISITED:
    #                     kid.accept(visitor, *args, **kwargs)
    #     else:
    #         def default_action(_tree, *_args, **_kwargs):
    #             visitor.visit(_tree, *_args, **_kwargs)
    #
    #         preorder_action = kwargs.pop('preorder', '')
    #         postorder_action = None
    #         if not preorder_action:
    #             postorder_action = kwargs.pop('postorder', '')
    #             if not postorder_action:
    #                 preorder_action = default_action
    #         GraphAlgorithms.calculate_tree_traverses(self,
    #                                                  preorder_action=preorder_action,
    #                                                  postorder_action=postorder_action)
