#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from collections import deque

from art.framework.core.status import Status
from art.framework.frontend.parser.backtracking.\
    recursive_descent.recursive_descent_parser import RecursiveDescentParser
from art.framework.frontend.parser.parse_tree_factory import ParseTreeFactory
from art.framework.frontend.parser.parse_tree_kind import ParseTreeKind
from art.framework.frontend.token.token_factory import TokenFactory
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

    def skip_tokens(self, *args, **kwargs):
        """
        """
        pass

    def parse(self, *args, **kwargs):
        """
        """
        pass

    def parse_expression(self):
        """
        """

    def parse_assignment(self):
        """
        """

    def parse_unary_expression(self):
        """
        """

    def parse_primary_expression(self):
        """
        """

    def parse_parenthesized_expression(self):
        """
        """

    def parse_pre_increment_expression(self):
        """
        """

    def parse_pre_decrement_expression(self):
        """
        """

    def parse_post_increment_expression(self):
        """
        """

    def parse_post_decrement_expression(self):
        """
        """

    def parse_multiplicative_expression(self):
        """
        """

    def parse_additive_expression(self):
        """
        """

    def parse_relational_expression(self):
        """
        """

    def parse_equality_expression(self):
        """
        """

    def parse_and_expression(self):
        """
        """

    def parse_exclusive_or_expression(self):
        """
        """

    def parse_inclusive_or_expression(self):
        """
        """

    def parse_conditional_and_expression(self):
        """
        """

    def parse_conditional_or_expression(self):
        """
        """

    def parse_assignment_operator(self):
        """
        assignment_operator : '='
                            | '+='
                            | '-='
                            | '*='
                            | '/='
                            | '%='
                            | '&='
                            | '|='
                            | '^='
                            | '~='
                            | '<<='
                            | '>>=' NOT considered
                            ;
        """
        match self._lexical_analyzer.token.kind:
            case (TokenKind.EQUALS_SIGN |
                  TokenKind.ADD_ASSIGNMENT |
                  TokenKind.SUB_ASSIGNMENT |
                  TokenKind.MUL_ASSIGNMENT |
                  TokenKind.DIV_ASSIGNMENT |
                  TokenKind.MOD_ASSIGNMENT |
                  TokenKind.BITWISE_AND_ASSIGNMENT |
                  TokenKind.BITWISE_OR_ASSIGNMENT |
                  TokenKind.BITWISE_XOR_ASSIGNMENT |
                  TokenKind.BITWISE_NOT_ASSIGNMENT |
                  TokenKind.SHIFT_LEFT_OR_EQUAL):
                return ParseTreeFactory.make_tree(ParseTreeKind.ASSIGNMENT_OPERATOR,
                                                  self.grammar,
                                                  self._lexical_analyzer.token)
            case _:
                self._diagnostics.add(Status(f'Expected assignment operator, found '
                                             f'{self._lexical_analyzer.token.kind.name}, mismatch occurred at '
                                             f'{self._lexical_analyzer.get_content_position()}',
                                             'parser',
                                             Status.INVALID_TOKEN))
                return ParseTreeFactory.make_tree(ParseTreeKind.UNKNOWN,
                                                  self.grammar,
                                                  TokenFactory.UNKNOWN_TOKEN)

    def parse_literal(self):
        """
        literal : integer_number_literal
                | real_number_literal
                | string_literal
                | boolean_literal
                ;
        """
        match self._lexical_analyzer.token.kind:
            case (TokenKind.INTEGER | TokenKind.REAL | TokenKind.STRING | TokenKind.TRUE | TokenKind.FALSE):
                return ParseTreeFactory.make_tree(ParseTreeKind.LITERAL,
                                                  self.grammar,
                                                  self._lexical_analyzer.token)
            case _:
                self._diagnostics.add(Status(f'Expected literal, found {self._lexical_analyzer.token.kind.name}, '
                                             f'mismatch occurred at '
                                             f'{self._lexical_analyzer.get_content_position()}',
                                             'parser',
                                             Status.INVALID_TOKEN))
                return ParseTreeFactory.make_tree(ParseTreeKind.UNKNOWN,
                                                  self.grammar,
                                                  TokenFactory.UNKNOWN_TOKEN)

    def parse_fully_qualified_identifier(self):
        """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;

        identifier                 : 'identifier'
                                   ;
        """
        if self.accept(TokenKind.IDENTIFIER):
            root = tree = ParseTreeFactory.make_tree(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER,
                                                     self.grammar,
                                                     self._lexical_analyzer.prev_token)
            stack = deque()
            stack.append(self._lexical_analyzer.prev_token)  # push IDENTIFIER
            while not self._lexical_analyzer.eos():
                if self._lexical_analyzer.token.kind == TokenKind.DOT:
                    self._lexical_analyzer.next_lexeme()  # consume DOT
                elif self._lexical_analyzer.token.kind == TokenKind.IDENTIFIER:
                    stack.append(self._lexical_analyzer.token)  # push IDENTIFIER
                    self._lexical_analyzer.next_lexeme()  # consume IDENTIFIER
                else:
                    break
            while stack:
                token = stack.pop()
                if stack:
                    fq_kid = ParseTreeFactory.make_tree(ParseTreeKind.FULLY_QUALIFIED_IDENTIFIER,
                                                        self.grammar,
                                                        token)
                    tree.add_kid(fq_kid)
                    kid = ParseTreeFactory.make_tree(ParseTreeKind.IDENTIFIER,
                                                     self.grammar,
                                                     token)
                    tree.add_kid(kid)
                    tree = fq_kid
                else:
                    kid = ParseTreeFactory.make_tree(ParseTreeKind.IDENTIFIER,
                                                     self.grammar,
                                                     token)
                    tree.add_kid(kid)
        else:
            root = ParseTreeFactory.make_tree(ParseTreeKind.UNKNOWN,
                                              self.grammar,
                                              TokenFactory.UNKNOWN_TOKEN)
        return root
