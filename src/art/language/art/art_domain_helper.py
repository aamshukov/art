#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser domain helper """
from art.framework.core.base import Base
from art.framework.frontend.parser.parse_tree_visitor import ParseTreeVisitor
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.language.art.art_parse_tree_kind import ArtParseTreeKind


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
                self._data_sink = ''

            @property
            def data(self):
                """
                """
                return self._data_sink

            def visit(self, _tree, *args, **kwargs):
                """
                """
                if _tree.kind == ArtParseTreeKind.IDENTIFIER:
                    self._data_sink = f'{self._data_sink}{_tree.symbol.token.literal}'
                elif _tree.kind == ArtParseTreeKind.TERMINAL and _tree.symbol.token.kind == TokenKind.DOT:
                    self._data_sink = f'{self._data_sink}{_tree.symbol.token.literal}'
                return self._data_sink

        visitor = FqIdVisitor(tree)
        tree.accept(visitor, preorder=True)
        return visitor.data
