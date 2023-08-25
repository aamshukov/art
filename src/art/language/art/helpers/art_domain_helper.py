#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser domain helper """
from art.framework.core.base import Base
from art.framework.frontend.parser.parse_tree_visitor import ParseTreeVisitor
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind


class ArtDomainHelper(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def to_string(tree):
        """
        """
        match tree.kind:
            case ArtParseTreeKind.UNKNOWN:
                return ArtDomainHelper.to_string_unknown(tree)
            case ArtParseTreeKind.TERMINAL:
                return ArtDomainHelper.to_string_literal(tree)
            case ArtParseTreeKind.IDENTIFIER:
                return ArtDomainHelper.to_string_identifier(tree)
            case ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER:
                return ArtDomainHelper.to_string_fq_identifier(tree)

    @staticmethod
    def to_string_unknown(tree):
        """
        """
        return ArtParseTreeKind.UNKNOWN.name

    @staticmethod
    def to_string_literal(tree):
        """
        """
        return f'{ArtParseTreeKind.TERMINAL.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_identifier(tree):
        """
        """
        return f'{ArtParseTreeKind.IDENTIFIER.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_fq_identifier(tree):
        """
        """
        class FqIdVisitor(ParseTreeVisitor):
            def __init__(self, _tree):
                """
                """
                super().__init__(_tree)
                self.data_sink = ''

            @property
            def data(self):
                """
                """
                return self.data_sink

            def visit(self, tree, *args, **kwargs):  # noqa
                """
                """
                if (tree.kind == ArtParseTreeKind.TERMINAL and
                   (tree.symbol.token.kind == TokenKind.IDENTIFIER or
                    tree.symbol.token.kind == TokenKind.DOT or
                    tree.symbol.token.kind == TokenKind.COMMA or
                    tree.symbol.token.kind == TokenKind.WS or
                    tree.symbol.token.kind == TokenKind.LESS_THAN_SIGN or
                        tree.symbol.token.kind == TokenKind.GREATER_THAN_SIGN)):
                    self.data_sink = f'{self.data_sink}{tree.symbol.token.literal}'
                for kid in tree.kids:
                    kid.accept(visitor, *args, **kwargs)
                return self.data_sink

        visitor = FqIdVisitor(tree)
        tree.accept(visitor)
        return visitor.data
