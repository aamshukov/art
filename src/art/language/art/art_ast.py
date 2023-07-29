#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser Ast routines """
from art.framework.core.base import Base
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.language.art.art_cst_to_ast_visitor import ArtCstToAstVisitor
from art.language.art.art_parse_tree_kind import ArtParseTreeKind


class ArtAst(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def make_terminal_tree(kind, lexer, grammar, token=None):
        """
        """
        return ParseTreeFactory.make_tree(kind,
                                          grammar,
                                          lexer.token if not token else token)

    @staticmethod
    def make_non_terminal_tree(kind, grammar):
        """
        """
        return ParseTreeFactory.make_tree(kind, grammar)

    @staticmethod
    def type_cst_to_ast(cst, grammar):
        """
        """
        class TypeVisitor(ArtCstToAstVisitor):
            def __init__(self, cst, grammar):  # noqa
                """
                """
                super().__init__(cst, grammar)
                self.grammar = grammar
                self.ast = ParseTreeFactory.make_tree(ArtParseTreeKind.UNKNOWN, self.grammar)

            def accepted_non_terminal(self, kind):
                """
                """
                match kind:
                    case (ArtParseTreeKind.TYPE |
                          ArtParseTreeKind.TYPE_NAME |
                          ArtParseTreeKind.TYPE_PARAMETER_SEQ |
                          ArtParseTreeKind.TYPE_PARAMETERS |
                          ArtParseTreeKind.TYPE_PARAMETER |
                          ArtParseTreeKind.TYPE_ARGUMENT_SEQ |
                          ArtParseTreeKind.TYPE_ARGUMENTS |
                          ArtParseTreeKind.TYPE_ARGUMENT |
                          ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER |
                          ArtParseTreeKind.ARRAY_TYPE_RANKS |
                          ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER):
                        return True
                    case _:
                        return False

            def accepted_terminal(self, kind):
                """
                """
                match kind:
                    case (ArtParseTreeKind.LITERAL |
                          ArtParseTreeKind.IDENTIFIER |
                          ArtParseTreeKind.INTEGRAL_TYPE):
                        return True
                    case _:
                        return False

        visitor = TypeVisitor(cst, grammar)
        cst.accept(visitor)
        return visitor.ast
