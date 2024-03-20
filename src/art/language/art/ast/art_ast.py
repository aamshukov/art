#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser Ast routines """
from art.framework.core.domain.base import Base
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.language.art.ast.art_parse_tree_visitor import ArtParseTreeVisitor
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind


class ArtAst(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def make_terminal_tree(kind, grammar, token):
        """
        """
        return ParseTreeFactory.make_tree(kind, grammar, token)

    @staticmethod
    def make_non_terminal_tree(kind, grammar):
        """
        """
        return ParseTreeFactory.make_tree(kind, grammar)

    @staticmethod
    def type_cst_to_ast(cst, grammar):
        """
        """
        class TypeVisitor(ArtParseTreeVisitor):
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
                          ArtParseTreeKind.TYPE_PARAMETER_SEQ_OPT |
                          ArtParseTreeKind.TYPE_PARAMETER_SEQ |
                          ArtParseTreeKind.TYPE_PARAMETERS |
                          ArtParseTreeKind.TYPE_PARAMETER |
                          ArtParseTreeKind.TYPE_ARGUMENT_SEQ_OPT |
                          ArtParseTreeKind.TYPE_ARGUMENT_SEQ |
                          ArtParseTreeKind.TYPE_ARGUMENTS |
                          ArtParseTreeKind.TYPE_ARGUMENT |
                          ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER_OPT |
                          ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER |
                          ArtParseTreeKind.ARRAY_TYPE_RANKS_OPT |
                          ArtParseTreeKind.ARRAY_TYPE_RANKS |
                          ArtParseTreeKind.INTEGRAL_TYPE |
                          ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER |
                          ArtParseTreeKind.IDENTIFIER |
                          ArtParseTreeKind.LITERAL):
                        return True
                    case _:
                        return False

            def accepted_terminal(self, kind):
                """
                """
                match kind:
                    case (TokenKind.IDENTIFIER):
                        return True
                    case _:
                        return False

        visitor = TypeVisitor(cst, grammar)
        cst.accept(visitor)
        return visitor.ast
