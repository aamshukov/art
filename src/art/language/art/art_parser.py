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
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.language.art.art_parse_tree_kind import ArtParseTreeKind


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

    def skip_tokens(self, kind, *args, **kwargs):
        """
        """
        while not self._lexical_analyzer.eos():
            if self._lexical_analyzer.token.kind != kind:
                self._lexical_analyzer.next_lexeme()

    def parse(self, *args, **kwargs):
        """
        """
        pass

    def parse_expression(self):
        """
        expression : non_assignment_expression
                   | assignment_expression
                   ;
        """
        expression = self.make_non_terminal_tree(ArtParseTreeKind.EXPRESSION)
        self.consume_noise(expression)
        self._lexical_analyzer.take_snapshot()
        non_assignment_expression = self.parse_non_assignment_expression()
        if non_assignment_expression.kind == ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION:
            expression.add_kid(non_assignment_expression)
            self._lexical_analyzer.discard_snapshot()
        else:
            self._lexical_analyzer.rewind_to_snapshot()
            assignment_expression = self.parse_assignment_expression()
            expression.add_kid(assignment_expression)
        return expression

    def parse_non_assignment_expression(self):
        """
        non_assignment_expression : conditional_expression
                                  ;
        """
        non_assignment_expression = self.make_non_terminal_tree(ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION)
        self.consume_noise(non_assignment_expression)
        conditional_expression = self.parse_conditional_expression()
        non_assignment_expression.add_kid(conditional_expression)
        return non_assignment_expression

    def parse_assignment_expression(self):
        """
        """
        assignment_expression = self.make_non_terminal_tree(ArtParseTreeKind.ASSIGNMENT_EXPRESSION)
        return assignment_expression

    def parse_conditional_expression(self):
        """
        conditional_expression : conditional_or_expression
                               | conditional_or_expression '?' expression ':' expression
                               ;
        """
        conditional_expression = self.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_EXPRESSION)
        self.consume_noise(conditional_expression)
        conditional_or_expression = self.parse_conditional_or_expression()
        conditional_expression.add_kid(conditional_or_expression)
        self.consume_noise(conditional_expression)
        if self._lexical_analyzer.token.kind == TokenKind.QUESTION_MARK:
            self.consume_terminal(conditional_expression)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression)
            self.consume_noise(conditional_expression)
            self.accept(TokenKind.COLON, conditional_expression)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression)
        return conditional_expression

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
        erroneous = self.make_non_terminal_tree(ArtParseTreeKind.UNKNOWN)
        return erroneous

    def parse_fully_qualified_identifier(self):
        """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;

        identifier                 : 'identifier'
                                   ;
        """
        result = tree = self.make_non_terminal_tree(ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER)
        stack = deque()
        stack.append(self._lexical_analyzer.token)  # push IDENTIFIER
        self._lexical_analyzer.next_lexeme()
        while not self._lexical_analyzer.eos():
            if self._lexical_analyzer.token.kind == TokenKind.DOT:
                la_token = self._lexical_analyzer.lookahead_lexeme()
                if la_token.kind == TokenKind.IDENTIFIER:
                    stack.append(self._lexical_analyzer.token)  # push DOT
                    stack.append(la_token)  # push IDENTIFIER
                    self._lexical_analyzer.next_lexeme()  # skip DOT
                    self._lexical_analyzer.next_lexeme()  # skip IDENTIFIER
                else:
                    break
            else:
                break
        while stack:
            token = stack.pop()
            if token.kind == TokenKind.DOT:
                kid = self.make_terminal_tree(ArtParseTreeKind.TERMINAL, token)
                tree.papa.insert_kid(kid, 1)
                continue
            if stack:
                fq_kid = self.make_non_terminal_tree(ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER)
                tree.add_kid(fq_kid)
                kid = self.make_terminal_tree(ArtParseTreeKind.IDENTIFIER, token)
                tree.add_kid(kid)
                tree = fq_kid
            else:
                kid = self.make_terminal_tree(ArtParseTreeKind.IDENTIFIER, token)
                tree.add_kid(kid)
        return result

    def consume_literal(self, papa):
        """
        literal : 'integer_number_literal'
                | 'real_number_literal'
                | 'string_literal'
                | 'boolean_literal'
                ;
        """
        match self._lexical_analyzer.token.kind:
            case (TokenKind.INTEGER |
                  TokenKind.REAL |
                  TokenKind.STRING |
                  TokenKind.TRUE |
                  TokenKind.FALSE):
                tree = self.consume_terminal(papa, ArtParseTreeKind.LITERAL)
            case _:
                tree = self.syntax_error(Status.INVALID_TOKEN,
                                         f'Expected literal, found {self._lexical_analyzer.token.kind.name}',
                                         papa)
        return tree

    def consume_assignment_operator(self, papa):
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
                tree = self.consume_terminal(papa, ArtParseTreeKind.ASSIGNMENT_OPERATOR)
            case _:
                tree = self.syntax_error(Status.INVALID_TOKEN,
                                         f'Expected assignment operator, '
                                         f'found {self._lexical_analyzer.token.kind.name}',
                                         papa)
        return tree

    def consume_noise(self, papa):
        """
        """
        while not self._lexical_analyzer.eos():
            if (self._lexical_analyzer.token.kind == TokenKind.WS or
                    self._lexical_analyzer.token.kind == TokenKind.EOL):
                self.consume_terminal(papa)
            elif self._lexical_analyzer.token.kind == TokenKind.INDENT:
                self.consume_terminal(papa, ArtParseTreeKind.INDENT)
            elif self._lexical_analyzer.token.kind == TokenKind.DEDENT:
                self.consume_terminal(papa, ArtParseTreeKind.DEDENT)
            else:
                break

    def consume_terminal(self, papa, tree_kind=ArtParseTreeKind.TERMINAL, advance=True):
        """
        """
        tree = self.make_terminal_tree(tree_kind)
        papa.add_kid(tree)
        if advance:
            self._lexical_analyzer.next_lexeme()
        return tree

    def accept(self, token_kind, papa):
        """
        """
        if self._lexical_analyzer.token.kind == token_kind:
            tree = self.consume_terminal(papa)
        else:
            tree = self.syntax_error(f'Expected token {token_kind.name}, ', Status.INVALID_TOKEN, papa)
        return tree

    def syntax_error(self, error_code, message, papa):
        """
        """
        self._diagnostics.add(Status(f'{message}, at {self._lexical_analyzer.get_content_position()}',
                                     'art parser',
                                     error_code))
        tree = self.make_non_terminal_tree(ArtParseTreeKind.UNKNOWN)
        papa.add_kid(tree)
        return tree

    def make_terminal_tree(self, kind, token=None):
        """
        """
        return ParseTreeFactory.make_tree(kind,
                                          self.grammar,
                                          self._lexical_analyzer.token if not token else token)

    def make_non_terminal_tree(self, kind):
        """
        """
        return ParseTreeFactory.make_tree(kind, self.grammar, None)
