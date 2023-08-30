# #! /usr/bin/env python3
# # -*- encoding: utf-8 -*-
# # UI Lab Inc. Arthur Amshukov
# #
# """ Art Cst cleansing visitor """
# from abc import abstractmethod
# from collections import deque
# from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
# from art.framework.frontend.parser.parse_tree_visitor import ParseTreeVisitor
# from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind
#
#
# class ArtCstCleansingVisitor(ParseTreeVisitor):
#     """
#     """
#     def __init__(self, cst, grammar):
#         """
#         """
#         super().__init__(cst)
#         self.grammar = grammar
#         self.cst = ParseTreeFactory.make_tree(ArtParseTreeKind.UNKNOWN, self.grammar)
#
#     @abstractmethod
#     def accepted_non_terminal(self, kind):
#         """
#         """
#         raise NotImplemented(self.accepted_non_terminal.__qualname__)
#
#     @abstractmethod
#     def accepted_terminal(self, kind):
#         """
#         """
#         raise NotImplemented(self.accepted_terminal.__qualname__)
#
#     def make_tree(self, cst, papa=None):
#         """
#         """
#         result = None
#         if self.accepted_non_terminal(cst.kind) or self.accepted_terminal(cst.kind):
#             result = ParseTreeFactory.clone(cst)
#         if papa and result:
#             papa.add_kid(result)
#         return result
#
#     def visit(self, cst, *args, **kwargs):
#         """
#         """
#         stack = deque()
#         self.ast = papa = self.make_tree(cst)  # set root, avoid update self.ast in the loop
#         for kid in reversed(cst.kids):
#             if self.accepted_non_terminal(kid.kind) or self.accepted_terminal(kid.kind):
#                 stack.append(ArtCstToAstVisitor.TvpPair(kid, 1, papa))
#         while stack:
#             pair = stack.pop()
#             if pair.value == 1:
#                 pair.value += 1
#                 stack.append(pair)
#                 papa = self.make_tree(pair.tree, pair.papa)
#                 assert papa, 'Unable to build TYPE Ast from Cst.'
#                 for kid in reversed(pair.tree.kids):
#                     if (self.accepted_non_terminal(kid.kind) or
#                             (kid.symbol.grammar_symbol.terminal and self.accepted_terminal(kid.symbol.token.kind))):
#                         stack.append(ArtCstToAstVisitor.TvpPair(kid, 1, papa))
#             elif pair.value == 2:
#                 pair.value += 1
#                 stack.append(pair)
