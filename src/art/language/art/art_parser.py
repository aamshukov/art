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
        self._current_expression = ArtParseTreeKind.UNKNOWN  # keep tack of which expression has been parsing

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
            if (self._current_expression != ArtParseTreeKind.CONDITIONAL_EXPRESSION and  #??
                    self._current_expression != ArtParseTreeKind.UNKNOWN):
                self._lexical_analyzer.rewind_to_snapshot()
                assignment_expression = self.parse_assignment_expression()
                expression.add_kid(assignment_expression)
        self._current_expression = ArtParseTreeKind.EXPRESSION
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
        self._current_expression = ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION
        return non_assignment_expression

    def parse_assignment_expression(self):
        """
        """
        assignment_expression = self.make_non_terminal_tree(ArtParseTreeKind.ASSIGNMENT_EXPRESSION)
        self._current_expression = ArtParseTreeKind.ASSIGNMENT_EXPRESSION
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
        self._current_expression = ArtParseTreeKind.CONDITIONAL_EXPRESSION
        return conditional_expression

    def parse_unary_expression(self):
        """
        """
        self._current_expression = ArtParseTreeKind.UNARY_EXPRESSION

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
        erroneous = self.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_OR_EXPRESSION)
        self._current_expression = ArtParseTreeKind.CONDITIONAL_OR_EXPRESSION
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

    def parse_literal(self, papa):
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

    def parse_assignment_operator(self, papa):
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

    def parse_type(self):
        """
        TYPE : integral_type array_type_specifier_opt
             | type_name array_type_specifier_opt
             | type_parameter
             ;
        """  # noqa
        type_tree = self.make_non_terminal_tree(ArtParseTreeKind.TYPE)
        self.consume_noise(type_tree)
        if self.integral_type():
            self.consume_terminal(type_tree)
        else:
            type_name = self.parse_type_name()
            type_tree.add_kid(type_name)
        self.consume_noise(type_tree)
        if self._lexical_analyzer.token.kind == TokenKind.LESS_THAN_SIGN:
            array_type_specifier = self.parse_array_type_specifier()
            type_tree.add_kid(array_type_specifier)
        return type_tree

    def parse_type_name(self):
        """
        type_name : identifier type_argument_seq_opt                          # A<T>
                  | type_name '.' identifier type_argument_seq_opt            # A<T>.B<U>.C<A<B<U>>>
                  ;
        """  # noqa
        type_name = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_NAME)
        self.consume_noise(type_name)
        self.consume_terminal(type_name, ArtParseTreeKind.IDENTIFIER)
        self.consume_noise(type_name)
        if self._lexical_analyzer.token.kind == TokenKind.LESS_THAN_SIGN:
            type_parameter_seq = self.parse_type_parameter_seq()
            type_name.add_kid(type_parameter_seq)
        while self._lexical_analyzer.token.kind == TokenKind.DOT:
            self.consume_noise(type_name)
            self.consume_terminal(type_name, ArtParseTreeKind.IDENTIFIER)
            self.consume_noise(type_name)
            if self._lexical_analyzer.token.kind == TokenKind.LESS_THAN_SIGN:
                type_parameter_seq = self.parse_type_parameter_seq()
                type_name.add_kid(type_parameter_seq)
            self.consume_noise(type_name)
        return type_name

    def parse_type_parameter_seq(self):
        """
        type_parameter_seq : '<' type_parameters '>'
                           ;
        """  # noqa
        type_parameters_seq = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETERS_SEQ)
        self.accept(TokenKind.LESS_THAN_SIGN, type_parameters_seq)
        type_parameters = self.parse_type_parameters()
        type_parameters_seq.add_kid(type_parameters)
        self.accept(TokenKind.GREATER_THAN_SIGN, type_parameters_seq)
        return type_parameters_seq

    def parse_type_parameters(self):
        """
        type_parameters : type_parameter        # type_parameter (',' type_parameter)*
                        | type_parameters ',' type_parameter
                        ;
        """  # noqa
        type_parameters = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETERS)
        self.consume_noise(type_parameters)
        type_parameter = self.parse_type_parameter()
        type_parameters.add_kid(type_parameter)
        self.consume_noise(type_parameters)
        while self._lexical_analyzer.token.kind == TokenKind.COMMA:
            self.consume_terminal(type_parameters)
            type_parameter = self.parse_type_argument()
            type_parameters.add_kid(type_parameter)
            self.consume_noise(type_parameters)
        return type_parameters

    def parse_type_parameter(self):
        """
        type_parameter : identifier
                       ;
        """  # noqa
        type_parameter = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT)
        self.consume_noise(type_parameter)
        self.consume_terminal(type_parameter, ArtParseTreeKind.IDENTIFIER)
        return type_parameter

    def parse_type_argument_seq(self):
        """
        type_argument_seq : '<' type_arguments '>'
                          ;
        """  # noqa
        type_arguments_seq = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENTS_SEQ)
        self.accept(TokenKind.LESS_THAN_SIGN, type_arguments_seq)
        type_arguments = self.parse_type_arguments()
        type_arguments_seq.add_kid(type_arguments)
        self.accept(TokenKind.GREATER_THAN_SIGN, type_arguments_seq)
        return type_arguments_seq

    def parse_type_arguments(self):
        """
        type_arguments : type_argument                     # type_argument (',' type_argument)*
                       | type_arguments ',' type_argument
                       ;
        """  # noqa
        type_arguments = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENTS)
        self.consume_noise(type_arguments)
        type_argument = self.parse_type_argument()
        type_arguments.add_kid(type_argument)
        self.consume_noise(type_arguments)
        while self._lexical_analyzer.token.kind == TokenKind.COMMA:
            self.consume_terminal(type_arguments)
            type_argument = self.parse_type_argument()
            type_arguments.add_kid(type_argument)
            self.consume_noise(type_arguments)
        return type_arguments

    def parse_type_argument(self):
        """
        type_argument : TYPE
                      ;
        """  # noqa
        type_argument = self.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT)
        type_tree = self.parse_type()
        type_argument.add_kid(type_tree)
        return type_argument

    def parse_array_type_specifier(self):
        """
        array_type_specifier : '[' array_dimensions ']' array_modifiers_opt     # zero based, checked array, row based, optionally column based and/or unchecked
                             ;
        """  # noqa
        array_type_specifier = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SPECIFIER)
        self.accept(TokenKind.LEFT_SQUARE_BRACKET, array_type_specifier)
        array_dimensions = self.parse_array_dimensions()
        array_type_specifier.add_kid(array_dimensions)
        self.accept(TokenKind.RIGHT_SQUARE_BRACKET, array_type_specifier)
        array_modifiers = self.parse_array_modifiers()
        array_type_specifier.add_kid(array_modifiers)
        return array_type_specifier

    def parse_array_dimensions(self):
        """
        array_dimensions : array_dimension                          # array_dimension (',' array_dimension)*
                         | array_dimensions ',' array_dimension
                         ;
        """  # noqa
        array_dimensions = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_DIMENSIONS)
        self.consume_noise(array_dimensions)
        array_dimension = self.parse_array_dimension()
        array_dimensions.add_kid(array_dimension)
        self.consume_noise(array_dimensions)
        while self._lexical_analyzer.token.kind == TokenKind.COMMA:
            self.consume_terminal(array_dimensions)
            array_dimension = self.parse_array_dimension()
            array_dimensions.add_kid(array_dimension)
            self.consume_noise(array_dimensions)
        return array_dimensions

    def parse_array_dimension(self):
        """
        array_dimension : array_upper_bound
                        | array_lower_bound '..' array_upper_bound   # array_lower_bound ('..' array_upper_bound)?
                        ;
        """  # noqa
        array_dimension = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_DIMENSION)
        array_bound = self.parse_array_lower_bound()
        array_dimension.add_kid(array_bound)
        self.consume_noise(array_dimension)
        if self._lexical_analyzer.token.kind == TokenKind.RANGE:
            self.consume_terminal(array_dimension)
            self.consume_noise(array_dimension)
            array_bound = self.parse_array_upper_bound()
            array_dimension.add_kid(array_bound)
        return array_dimension

    def parse_array_lower_bound(self):
        """
        array_lower_bound : array_bound_expression
                          ;
        """
        array_lower_bound = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_LOWER_BOUND)
        array_bound_expression = self.parse_array_bound_expression()
        array_lower_bound.add_kid(array_bound_expression)
        return array_lower_bound

    def parse_array_upper_bound(self):
        """
        array_upper_bound : array_bound_expression
                          ;
        """
        array_upper_bound = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_UPPER_BOUND)
        array_bound_expression = self.parse_array_bound_expression()
        array_upper_bound.add_kid(array_bound_expression)
        return array_upper_bound

    def parse_array_bound_expression(self):
        """
        array_bound_expression : non_assignment_expression  # must evaluate to compilation
                               ;                            # time constant integer
        """
        array_bound_expression = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_BOUND_EXPRESSION)
        non_assignment_expression = self.parse_non_assignment_expression()
        array_bound_expression.add_kid(non_assignment_expression)
        self._current_expression = ArtParseTreeKind.ARRAY_BOUND_EXPRESSION
        return array_bound_expression

    def parse_array_modifiers(self):
        """
        array_modifiers : array_modifier
                        | array_modifiers ',' array_modifier
                        ;
        """
        array_modifiers = self.make_non_terminal_tree(ArtParseTreeKind.ARRAY_MODIFIERS)
        self.consume_noise(array_modifiers)
        while self.array_modifier():
            self.consume_terminal(array_modifiers)
            self.consume_noise(array_modifiers)
            if self._lexical_analyzer.token.kind == TokenKind.COMMA:
                self.consume_terminal(array_modifiers)
            else:
                break
            self.consume_noise(array_modifiers)
        return array_modifiers

    def array_modifier(self):
        """
        array_modifier : 'column'             # column based array specifier
                       | 'row'                # row based array specifier - default
                       | 'jagged'             # array of arrays, possibly of different sizes
                       | 'unchecked'          # unchecked array specifier
                       ;
        """
        match self._lexical_analyzer.token.kind:
            case (TokenKind.COLUMN_KW |
                  TokenKind.ROW_KW |
                  TokenKind.JAGGED_KW |
                  TokenKind.UNCHECKED_KW):
                return True
            case _:
                return False

    def integral_type(self):
        """
        integral_type : 'integer'
                      | 'int'
                      | 'real'
                      | 'string'
                      | 'boolean'
                      | 'bool'
                      ;
        """
        match self._lexical_analyzer.token.kind:
            case (TokenKind.INTEGER_KW |
                  TokenKind.REAL_KW |
                  TokenKind.STRING_KW |
                  TokenKind.BOOLEAN_KW):
                return True
            case _:
                return False

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
