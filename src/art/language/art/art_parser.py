#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from art.framework.frontend.parser.backtracking.\
    recursive_descent.recursive_descent_parser import RecursiveDescentParser
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind
from art.framework.frontend.symtable.symbol_factory import SymbolFactory
from art.framework.frontend.token.token_kind import TokenKind


class ArtParser(RecursiveDescentParser):
    """
    """
    def __init__(self,
                 context,
                 lexical_analyzer,
                 grammar,
                 statistics,
                 diagnostics):
        """
        """
        super().__init__(context,
                         lexical_analyzer,
                         grammar,
                         statistics,
                         diagnostics)

    def parse(self, *args, **kwargs):
        """
        """
        pass

    def parse_fully_qualified_identifier(self):
        """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;
        """
        if self.accept(TokenKind.IDENTIFIER):
            root = ParseTreeFactory.create(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER)
            root.symbol = SymbolFactory.create()
            root.symbol.grammar_symbol =\
                self._grammar.get_non_terminal(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER.name)
            tree = root
            while True:
                if self._lexical_analyzer.token.kind == TokenKind.DOT:
                    la_token = self._lexical_analyzer.lookahead_lexeme()
                    if la_token.kind == TokenKind.IDENTIFIER:
                        kid = ParseTreeFactory.create(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER)
                        kid.symbol = SymbolFactory.create()
                        kid.symbol.grammar_symbol =\
                            self._grammar.get_non_terminal(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER.name)
                        tree.add_kid(kid)
                        kid = ParseTreeFactory.create(ParseTreeKind.IDENTIFIER)
                        kid.symbol = SymbolFactory.create()
                        kid.symbol.grammar_symbol =\
                            self._grammar.get_non_terminal(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER.name)
                        tree.add_kid(kid)
                        tree = tree.kids[0]
                        self._lexical_analyzer.next_lexeme()  # consume DOT
                        self._lexical_analyzer.next_lexeme()  # consume IDENTIFIER
                    else:
                        break
                elif self._lexical_analyzer.token.kind == TokenKind.IDENTIFIER:
                    kid = ParseTreeFactory.create(ParseTreeKind.IDENTIFIER)
                    kid.symbol = SymbolFactory.create()
                    kid.symbol.grammar_symbol = \
                        self._grammar.get_non_terminal(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER.name)
                    tree.add_kid(kid)
                    break
                else:
                    break
        else:
            root = ParseTreeFactory.create(ParseTreeKind.UNKNOWN)
            root.symbol = SymbolFactory.create()
        return root
