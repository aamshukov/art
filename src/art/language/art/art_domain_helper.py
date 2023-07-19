#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser domain helper """
from art.framework.core.base import Base
from art.framework.frontend.parser.parse_tree_visitor import ParseTreeVisitor
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
            case ArtParseTreeKind.LITERAL:
                return ArtDomainHelper.to_string_literal(tree)
            case ArtParseTreeKind.IDENTIFIER:
                return ArtDomainHelper.to_string_identifier(tree)
            case ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER:
                return ArtDomainHelper.to_string_fq_identifier(tree)

    @staticmethod
    def to_string_unknown(tree):
        """
        """
        return ParseTreeKind.UNKNOWN.name

    @staticmethod
    def to_string_literal(tree):
        """
        """
        return f'{ArtParseTreeKind.LITERAL.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_identifier(tree):
        """
        """
        return f'{ArtParseTreeKind.IDENTIFIER.name}:{tree.label}:{tree.symbol.token.label}:{tree.symbol.token.literal}'

    @staticmethod
    def to_string_fq_identifier(tree):
        """
        D:\Python\envs\python311-64bit\Lib\site-packages\pptree\pptree.py
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
                    if self._data_sink:
                        self._data_sink += '.'
                    self._data_sink = f'{self._data_sink}{_tree.symbol.token.literal}'
                return self._data_sink

        visitor = FqIdVisitor(tree)
        tree.accept(visitor, recursive=False)
        return visitor.data
