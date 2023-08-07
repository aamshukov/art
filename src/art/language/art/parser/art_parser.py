#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from collections import deque
from art.framework.core.status import Status
from art.framework.frontend.parser.backtracking.\
    recursive_descent.recursive_descent_parser import RecursiveDescentParser
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_result import ParseResult
from art.language.art.ast.art_ast import ArtAst
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind


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
        self.current_expression = ArtParseTreeKind.UNKNOWN  # keep tack of which expression has been parsing
        self.lexer = lexical_analyzer  # primary lexer, but might be switched to another one (import, include, etc.)

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
        self.inc_recursion_level()
        expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.EXPRESSION, self.grammar)
        self.consume_noise(expression)
        primary_expression = self.parse_primary_expression()
        expression.add_kid(primary_expression.tree)
        # self.lexer.take_snapshot()
        # non_assignment_expression = self.parse_non_assignment_expression()
        # if non_assignment_expression.kind == ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION:
        #     expression.add_kid(non_assignment_expression.tree)
        #     self.lexer.discard_snapshot()
        # else:
        #     if (self.current_expression != ArtParseTreeKind.CONDITIONAL_EXPRESSION and  #??
        #             self.current_expression != ArtParseTreeKind.UNKNOWN):
        #         self.lexer.rewind_to_snapshot()
        #         assignment_expression = self.parse_assignment_expression()
        #         expression.add_kid(assignment_expression.tree)
        self.current_expression = ArtParseTreeKind.EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, expression)

    def parse_non_assignment_expression(self):
        """
        non_assignment_expression : conditional_expression
                                  ;
        """
        non_assignment_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION,
                                                                  self.grammar)
        self.consume_noise(non_assignment_expression)
        conditional_expression = self.parse_conditional_expression()
        non_assignment_expression.add_kid(conditional_expression.tree)
        self.current_expression = ArtParseTreeKind.NON_ASSIGNMENT_EXPRESSION
        return ParseResult(ParseResult.Status.OK, non_assignment_expression)

    def parse_assignment_expression(self):
        """
        """
        assignment_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ASSIGNMENT_EXPRESSION, self.grammar)
        self.current_expression = ArtParseTreeKind.ASSIGNMENT_EXPRESSION
        return ParseResult(ParseResult.Status.OK, assignment_expression)

    def parse_conditional_expression(self):
        """
        conditional_expression : conditional_or_expression
                               | conditional_or_expression '?' expression ':' expression
                               ;
        """
        conditional_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_EXPRESSION, self.grammar)
        self.consume_noise(conditional_expression)
        conditional_or_expression = self.parse_conditional_or_expression()
        conditional_expression.add_kid(conditional_or_expression.tree)
        self.consume_noise(conditional_expression)
        if self.lexer.token.kind == TokenKind.QUESTION_MARK:
            self.consume_terminal(conditional_expression)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression.tree)
            self.consume_noise(conditional_expression)
            self.accept(conditional_expression, TokenKind.COLON)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression.tree)
        self.current_expression = ArtParseTreeKind.CONDITIONAL_EXPRESSION
        return ParseResult(ParseResult.Status.OK, conditional_expression)

    def parse_unary_expression(self):
        """
        """
        self.current_expression = ArtParseTreeKind.UNARY_EXPRESSION

    def parse_primary_expression(self):
        """
        primary_expression : literal
                           | identifier type_argument_seq_opt
                           | member_access
                           | array_element_access
                           | invocation_expression
                           | post_increment_expression
                           | post_decrement_expression
                           | object_creation_expression
                          #| array_creation_expression
                           | parenthesized_expression
                           ;
        """
        self.inc_recursion_level()
        primary_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.PRIMARY_EXPRESSION, self.grammar)
        punctuator = False  #??
        invocation = False
        while True:
            self.consume_noise(primary_expression)
            if self.lexer.token.kind == TokenKind.IDENTIFIER:
                self.accept(primary_expression, TokenKind.IDENTIFIER)
                type_argument_seq_opt = self.parse_type_argument_seq_opt()
                if type_argument_seq_opt.status != ParseResult.Status.OPTIONAL:
                    primary_expression.add_kid(type_argument_seq_opt.tree)
                invocation = True
            elif self.literal():
                self.parse_literal(primary_expression)
                invocation = True
            elif self.lexer.token.kind == TokenKind.DOT:
                self.consume_terminal(primary_expression)
                invocation = False
            elif self.lexer.token.kind == TokenKind.LEFT_PARENTHESIS:
                self.accept(primary_expression, TokenKind.LEFT_PARENTHESIS)
                if invocation:
                    arguments_opt = self.parse_arguments_opt()
                    if arguments_opt.status != ParseResult.Status.OPTIONAL:
                        primary_expression.add_kid(arguments_opt.tree)
                else:
                    expression = self.parse_expression()
                    primary_expression.add_kid(expression.tree)
                self.consume_noise(primary_expression)
                self.accept(primary_expression, TokenKind.RIGHT_PARENTHESIS)
                invocation = False
            elif self.lexer.token.kind == TokenKind.LEFT_SQUARE_BRACKET:
                self.consume_terminal(primary_expression)
                arguments = self.parse_arguments()
                primary_expression.add_kid(arguments.tree)
                self.consume_noise(primary_expression)
                self.accept(primary_expression, TokenKind.RIGHT_SQUARE_BRACKET)
                invocation = True
            elif self.lexer.token.kind == TokenKind.LEFT_CURLY_BRACKET:
                self.consume_terminal(primary_expression)
                arguments_opt = self.parse_arguments_opt()
                if arguments_opt.status != ParseResult.Status.OPTIONAL:
                    primary_expression.add_kid(arguments_opt.tree)
                self.consume_noise(primary_expression)
                self.accept(primary_expression, TokenKind.RIGHT_CURLY_BRACKET)
                invocation = False
            elif self.lexer.token.kind == TokenKind.INCREMENT:
                self.consume_terminal(primary_expression)
                invocation = False
            elif self.lexer.token.kind == TokenKind.DECREMENT:
                self.consume_terminal(primary_expression)
                invocation = False
            else:
                break
        self.current_expression = ArtParseTreeKind.PRIMARY_EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, primary_expression)

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
        erroneous = ArtAst.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_OR_EXPRESSION,
                                                  self.grammar)
        self.current_expression = ArtParseTreeKind.CONDITIONAL_OR_EXPRESSION
        return erroneous

    def parse_type(self):
        """
        TYPE : integral_type array_type_rank_specifier_opt
             | type_name array_type_rank_specifier_opt
             | type_parameter array_type_rank_specifier_opt
             ;
        """  # noqa
        self.inc_recursion_level()
        type_tree = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE, self.grammar)
        self.consume_noise(type_tree)
        if self.integral_type():
            self.consume_terminal(type_tree, ArtParseTreeKind.INTEGRAL_TYPE)
        else:
            if self.lexer.token.kind == TokenKind.IDENTIFIER:
                la_token = self.lexer.lookahead_lexeme(skip=[TokenKind.WS,
                                                             TokenKind.EOL,
                                                             TokenKind.INDENT,
                                                             TokenKind.DEDENT,
                                                             TokenKind.CORRUPTED_DEDENT])
                if la_token.kind == TokenKind.LESS_THAN_SIGN or la_token.kind == TokenKind.DOT:
                    type_name = self.parse_type_name()
                    type_tree.add_kid(type_name.tree)
                else:
                    type_parameter = self.parse_type_parameter()
                    type_tree.add_kid(type_parameter.tree)
            else:
                erroneous = self.syntax_error(type_tree,
                                              Status.INVALID_TOKEN,
                                              f'Expected IDENTIFIER and . or <, found '
                                              f'{self.lexer.token.kind.name}')
        array_type_rank_specifier_opt = self.parse_array_type_rank_specifier_opt()
        if array_type_rank_specifier_opt.status != ParseResult.Status.OPTIONAL:
            type_tree.add_kid(array_type_rank_specifier_opt.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_tree)

    def parse_type_name(self):
        """
        type_name : fully_qualified_identifier
                  ;
        """  # noqa
        self.inc_recursion_level()
        type_name = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_NAME, self.grammar)
        self.consume_noise(type_name)
        fully_qualified_identifier = self.parse_fully_qualified_identifier()
        type_name.add_kid(fully_qualified_identifier.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_name)

    def parse_type_parameter_seq_opt(self):
        """
        type_parameter_seq_opt : type_parameter_seq
                               | ε
                               ;
        """  # noqa
        self.inc_recursion_level()
        type_parameter_seq_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETER_SEQ_OPT, self.grammar)
        self.consume_noise(type_parameter_seq_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if self.lexer.token.kind == TokenKind.LESS_THAN_SIGN:
            type_parameter_seq = self.type_parameter_seq()
            type_parameter_seq_opt.add_kid(type_parameter_seq.tree)
            result = ParseResult(ParseResult.Status.OK, type_parameter_seq_opt)
        self.dec_recursion_level()
        return result

    def parse_type_parameter_seq(self):
        """
        type_parameter_seq : '<' type_parameters '>'
                           ;
        """  # noqa
        self.inc_recursion_level()
        type_parameters_seq = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETER_SEQ, self.grammar)
        self.consume_noise(type_parameter_seq)
        self.accept(type_parameters_seq, TokenKind.LESS_THAN_SIGN)
        type_parameters = self.parse_type_parameters()
        type_parameters_seq.add_kid(type_parameters.tree)
        self.consume_noise(type_parameter_seq)
        self.accept(type_parameters_seq, TokenKind.GREATER_THAN_SIGN)
        self.dec_recursion_level()
        return ParseResult(status, type_parameters_seq)

    def parse_type_parameters(self):
        """
        type_parameters : type_parameter
                        | type_parameters ',' type_parameter
                        ;
        """  # noqa
        self.inc_recursion_level()
        type_parameters = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETERS, self.grammar)
        self.consume_noise(type_parameters)
        type_parameter = self.parse_type_parameter()
        type_parameters.add_kid(type_parameter.tree)
        self.consume_noise(type_parameters)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(type_parameters)
            type_parameter = self.parse_type_argument()
            type_parameters.add_kid(type_parameter.tree)
            self.consume_noise(type_parameters)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_parameters)

    def parse_type_parameter(self):
        """
        type_parameter : identifier
                       ;
        """  # noqa
        self.inc_recursion_level()
        type_parameter = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETER, self.grammar)
        self.consume_noise(type_parameter)
        self.accept(type_parameter, TokenKind.IDENTIFIER)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_parameter)

    def parse_type_argument_seq_opt(self):
        """
        type_argument_seq_opt : type_argument_seq
                              | ε
                              ;
        """  # noqa
        self.inc_recursion_level()
        type_argument_seq_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT_SEQ_OPT, self.grammar)
        self.consume_noise(type_argument_seq_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if self.lexer.token.kind == TokenKind.LESS_THAN_SIGN:
            type_argument_seq = self.parse_type_argument_seq()
            type_argument_seq_opt.add_kid(type_argument_seq.tree)
            result = ParseResult(ParseResult.Status.OK, type_argument_seq_opt)
        self.dec_recursion_level()
        return result

    def parse_type_argument_seq(self):
        """
        type_argument_seq : '<' type_arguments '>'
                          ;
        """  # noqa
        self.inc_recursion_level()
        type_argument_seq = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT_SEQ, self.grammar)
        self.consume_noise(type_argument_seq)
        self.accept(type_argument_seq, TokenKind.LESS_THAN_SIGN)
        type_arguments = self.parse_type_arguments()
        type_argument_seq.add_kid(type_arguments.tree)
        self.consume_noise(type_argument_seq)
        self.accept(type_argument_seq, TokenKind.GREATER_THAN_SIGN)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_argument_seq)

    def parse_type_arguments(self):
        """
        type_arguments : type_argument
                       | type_arguments ',' type_argument
                       ;
        """  # noqa
        self.inc_recursion_level()
        type_arguments = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENTS, self.grammar)
        self.consume_noise(type_arguments)
        type_argument = self.parse_type_argument()
        type_arguments.add_kid(type_argument.tree)
        self.consume_noise(type_arguments)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(type_arguments)
            type_argument = self.parse_type_argument()
            type_arguments.add_kid(type_argument.tree)
            self.consume_noise(type_arguments)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_arguments)

    def parse_type_argument(self):
        """
        type_argument : TYPE
                      ;
        """  # noqa
        self.inc_recursion_level()
        type_argument = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT, self.grammar)
        self.consume_noise(type_argument)
        type_tree = self.parse_type()
        type_argument.add_kid(type_tree.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_argument)

    def parse_array_type_rank_specifier_opt(self):
        """
        array_type_rank_specifier_opt : array_type_rank_specifier
                                      | ε
                                      ;
        """  # noqa
        self.inc_recursion_level()
        array_type_rank_specifier_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER_OPT,
                                                                      self.grammar)
        self.consume_noise(array_type_rank_specifier_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if self.lexer.token.kind == TokenKind.LEFT_SQUARE_BRACKET:
            array_type_rank_specifier = self.parse_array_type_rank_specifier()
            array_type_rank_specifier_opt.add_kid(array_type_rank_specifier.tree)
            result = ParseResult(ParseResult.Status.OK, array_type_rank_specifier_opt)
        self.dec_recursion_level()
        return result

    def parse_array_type_rank_specifier(self):
        """
        array_type_rank_specifier : '[' array_type_ranks_opt ']'
                                  ;
        """
        self.inc_recursion_level()
        array_type_rank_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER,
                                                                  self.grammar)
        self.consume_noise(array_type_rank_specifier)
        self.accept(array_type_rank_specifier, TokenKind.LEFT_SQUARE_BRACKET)
        array_type_ranks = self.parse_array_type_ranks()
        array_type_rank_specifier.add_kid(array_type_ranks.tree)
        self.consume_noise(array_type_rank_specifier)
        self.accept(array_type_rank_specifier, TokenKind.RIGHT_SQUARE_BRACKET)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_type_rank_specifier)

    def parse_array_type_ranks(self):
        """
        array_type_ranks : ','
                         | array_type_ranks ','
                         ;
        """
        self.inc_recursion_level()
        array_type_ranks = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_RANKS, self.grammar)
        self.consume_noise(array_type_ranks)
        ranks = 1
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(array_type_ranks)
            self.consume_noise(array_type_ranks)
            ranks += 1
        array_type_ranks.attributes['ranks'] = ranks
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_type_ranks)

    def parse_array_type_specifier(self):
        """
        array_type_specifier : '[' array_dimensions ']' array_modifiers_opt
                             ;
        """  # noqa
        self.inc_recursion_level()
        array_type_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SPECIFIER, self.grammar)
        self.consume_noise(array_type_specifier)
        self.accept(array_type_specifier, TokenKind.LEFT_SQUARE_BRACKET)
        array_dimensions = self.parse_array_dimensions()
        array_type_specifier.add_kid(array_dimensions.tree)
        self.consume_noise(array_type_specifier)
        self.accept(array_type_specifier, TokenKind.RIGHT_SQUARE_BRACKET)
        array_modifiers_opt = self.parse_array_modifiers_opt()
        if array_modifiers_opt.status != ParseResult.Status.OPTIONAL:
            array_type_specifier.add_kid(array_modifiers_opt.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_type_specifier)

    def parse_array_dimensions(self):
        """
        array_dimensions : array_dimension
                         | array_dimensions ',' array_dimension
                         ;
        """  # noqa
        self.inc_recursion_level()
        array_dimensions = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_DIMENSIONS, self.grammar)
        self.consume_noise(array_dimensions)
        array_dimension = self.parse_array_dimension()
        array_dimensions.add_kid(array_dimension.tree)
        self.consume_noise(array_dimensions)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(array_dimensions)
            array_dimension = self.parse_array_dimension()
            array_dimensions.add_kid(array_dimension.tree)
            self.consume_noise(array_dimensions)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_dimensions)

    def parse_array_dimension(self):
        """
        array_dimension : array_upper_bound
                        | array_lower_bound '..' array_upper_bound
                        ;
        """  # noqa
        self.inc_recursion_level()
        array_dimension = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_DIMENSION, self.grammar)
        self.consume_noise(array_dimension)
        array_bound = self.parse_array_lower_bound()
        array_dimension.add_kid(array_bound.tree)
        self.consume_noise(array_dimension)
        if self.lexer.token.kind == TokenKind.RANGE:
            self.consume_terminal(array_dimension)
            self.consume_noise(array_dimension)
            array_bound = self.parse_array_upper_bound()
            array_dimension.add_kid(array_bound.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_dimension)

    def parse_array_lower_bound(self):
        """
        array_lower_bound : array_bound_expression
                          ;
        """
        self.inc_recursion_level()
        array_lower_bound = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_LOWER_BOUND, self.grammar)
        self.consume_noise(array_lower_bound)
        array_bound_expression = self.parse_array_bound_expression()
        array_lower_bound.add_kid(array_bound_expression.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_lower_bound)

    def parse_array_upper_bound(self):
        """
        array_upper_bound : array_bound_expression
                          ;
        """
        self.inc_recursion_level()
        array_upper_bound = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_UPPER_BOUND, self.grammar)
        self.consume_noise(array_upper_bound)
        array_bound_expression = self.parse_array_bound_expression()
        array_upper_bound.add_kid(array_bound_expression.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_upper_bound)

    def parse_array_bound_expression(self):
        """
        array_bound_expression : non_assignment_expression
                               ;
        """
        self.inc_recursion_level()
        array_bound_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_BOUND_EXPRESSION, self.grammar)
        self.consume_noise(array_bound_expression)
        non_assignment_expression = self.parse_non_assignment_expression()
        array_bound_expression.add_kid(non_assignment_expression.tree)
        self.current_expression = ArtParseTreeKind.ARRAY_BOUND_EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_bound_expression)

    def parse_array_modifiers_opt(self):
        """
        array_modifiers_opt : array_modifiers
                            | ε
                            ;
        """
        self.inc_recursion_level()
        array_modifiers_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_MODIFIERS_OPT, self.grammar)
        self.consume_noise(array_modifiers_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if self.array_modifier():
            array_modifiers = self.parse_array_modifiers()
            array_modifiers_opt.add_kid(array_modifiers.tree)
            result = ParseResult(ParseResult.Status.OK, array_modifiers_opt)
        self.dec_recursion_level()
        return result

    def parse_array_modifiers(self):
        """
        array_modifiers : array_modifier
                        | array_modifiers ',' array_modifier
                        ;
        """
        self.inc_recursion_level()
        array_modifiers = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_MODIFIERS, self.grammar)
        self.consume_noise(array_modifiers)
        self.accept_multiple(array_modifiers, ArtParser.array_modifiers())
        self.consume_noise(array_modifiers)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(array_modifiers)
            self.consume_noise(array_modifiers)
            self.accept_multiple(array_modifiers, ArtParser.array_modifiers())
            self.consume_noise(array_modifiers)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_modifiers)

    def array_modifier(self):
        """
        array_modifier : 'column'             # column based array specifier
                       | 'row'                # row based array specifier - default
                       | 'jagged'             # array of arrays, possibly of different sizes
                       | 'unchecked'          # unchecked array specifier
                       ;
        """
        match self.lexer.token.kind:
            case (TokenKind.COLUMN_KW |
                  TokenKind.ROW_KW |
                  TokenKind.JAGGED_KW |
                  TokenKind.UNCHECKED_KW):
                return True
            case _:
                return False

    @staticmethod
    def array_modifiers(self):
        """
        """
        return [TokenKind.COLUMN_KW, TokenKind.ROW_KW, TokenKind.JAGGED_KW, TokenKind.UNCHECKED_KW]

    def parse_arguments_opt(self):
        """
        arguments_opt : arguments
                      | ε
                      ;
        """  # noqa
        self.inc_recursion_level()
        arguments_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENTS_OPT, self.grammar)
        self.consume_noise(arguments_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if (self.lexer.token.kind != TokenKind.RIGHT_PARENTHESIS and
                self.lexer.token.kind != TokenKind.RIGHT_CURLY_BRACKET):
            arguments = self.parse_arguments()
            arguments_opt.add_kid(arguments.tree)
            result = ParseResult(ParseResult.Status.OK, arguments_opt)
        self.dec_recursion_level()
        return result

    def parse_arguments(self):
        """
        arguments : argument
                  | arguments ',' argument
                  ;
        """  # noqa
        self.inc_recursion_level()
        arguments = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENTS, self.grammar)
        self.consume_noise(arguments)
        argument = self.parse_argument()
        arguments.add_kid(argument.tree)
        self.consume_noise(arguments)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(arguments)
            argument = self.parse_argument()
            arguments.add_kid(argument.tree)
            self.consume_noise(arguments)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, arguments)

    def parse_argument(self):
        """
        argument : argument_name_opt argument_value
                 ;
        """  # noqa
        self.inc_recursion_level()
        argument = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT, self.grammar)
        self.consume_noise(argument)
        argument_name_opt = self.parse_argument_name_opt()
        if argument_name_opt.status != ParseResult.Status.OPTIONAL:
            argument.add_kid(argument_name_opt.tree)
        argument_value = self.parse_argument_value()
        argument.add_kid(argument_value.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument)

    def parse_argument_name_opt(self):
        """
        argument_name_opt : argument_name
                          | ε
                          ;
        """
        self.inc_recursion_level()
        argument_name_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_NAME_OPT, self.grammar)
        self.consume_noise(argument_name_opt)
        result = ParseResult(ParseResult.Status.OPTIONAL)
        if self.lexer.token.kind == TokenKind.IDENTIFIER:
            la_token = self.lexer.lookahead_lexeme(skip=[TokenKind.WS,
                                                         TokenKind.EOL,
                                                         TokenKind.INDENT,
                                                         TokenKind.DEDENT,
                                                         TokenKind.CORRUPTED_DEDENT])
            if la_token.kind == TokenKind.COLON:
                argument_name = self.parse_argument_name()
                argument_name_opt.add_kid(argument_name.tree)
                result = ParseResult(ParseResult.Status.OK, argument_name_opt)
        self.dec_recursion_level()
        return result

    def parse_argument_name(self):
        """
        argument_name : identifier ':'
                      ;
        """  # noqa
        self.inc_recursion_level()
        argument_name = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_NAME, self.grammar)
        self.consume_noise(argument_name)
        self.accept(argument_name, TokenKind.IDENTIFIER)
        self.consume_noise(argument_name)
        self.accept(argument_name, TokenKind.COLON)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_name)

    def parse_argument_value(self):
        """
        argument_value : expression lazy_opt
                       ;
        """  # noqa
        self.inc_recursion_level()
        argument_value = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUE, self.grammar)
        self.consume_noise(argument_value)
        expression = self.parse_expression()
        argument_value.add_kid(expression.tree)
        self.consume_noise(argument_value)
        if self.lexer.token.kind == TokenKind.LAZY_KW:
            self.consume_terminal(argument_value)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_value)

    def parse_fully_qualified_identifier(self):
        """
        fully_qualified_identifier : identifier type_argument_seq_opt
                                   | fully_qualified_identifier '.' identifier type_argument_seq_opt
                                   ;
        """
        self.inc_recursion_level()
        fq_identifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER, self.grammar)
        self.consume_noise(fq_identifier)
        self.accept(fq_identifier, TokenKind.IDENTIFIER)
        type_argument_seq_opt = self.parse_type_argument_seq_opt()
        if type_argument_seq_opt.status != ParseResult.Status.OPTIONAL:
            fq_identifier.add_kid(type_argument_seq_opt.tree)
        self.consume_noise(fq_identifier)
        while self.lexer.token.kind == TokenKind.DOT:
            self.consume_terminal(fq_identifier)
            self.consume_noise(fq_identifier)
            self.accept(fq_identifier, TokenKind.IDENTIFIER)
            type_argument_seq_opt = self.parse_type_argument_seq_opt()
            if type_argument_seq_opt.status != ParseResult.Status.OPTIONAL:
                fq_identifier.add_kid(type_argument_seq_opt.tree)
            self.consume_noise(fq_identifier)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, fq_identifier)

    def parse_literal(self, papa):
        """
        literal : 'integer_number_literal'
                | 'real_number_literal'
                | 'string_literal'
                | 'boolean_literal'
                ;
        """
        self.inc_recursion_level()
        if self.literal():
            result = self.consume_terminal(papa, ArtParseTreeKind.LITERAL)
        else:
            result = self.syntax_error(papa,
                                       Status.INVALID_TOKEN,
                                       f'Expected literal, found {self.lexer.token.kind.name}')
        self.dec_recursion_level()
        return result

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
        self.inc_recursion_level()
        match self.lexer.token.kind:
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
                result = self.consume_terminal(papa, ArtParseTreeKind.ASSIGNMENT_OPERATOR)
            case _:
                result = self.syntax_error(papa,
                                           Status.INVALID_TOKEN,
                                           f'Expected assignment operator, '
                                           f'found {self.lexer.token.kind.name}')
        self.dec_recursion_level()
        return result

    def integral_type(self):
        """
        integral_type : 'int'
                      | 'integer'
                      | 'real'
                      | 'float'
                      | 'double'
                      | 'decimal'
                      | 'number'
                      | 'bool'
                      | 'boolean'
                      | 'string'
                      ;
        """
        match self.lexer.token.kind:
            case (TokenKind.INTEGER_KW |
                  TokenKind.REAL_KW |
                  TokenKind.BOOLEAN_KW |
                  TokenKind.STRING_KW):
                return True
            case _:
                return False

    def literal(self):
        """
        """
        match self.lexer.token.kind:
            case (TokenKind.INTEGER |
                  TokenKind.REAL |
                  TokenKind.STRING |
                  TokenKind.TRUE_KW |
                  TokenKind.FALSE_KW):
                return True
            case _:
                return False

    def consume_noise(self, papa):
        """
        """
        while not self.lexer.eos():
            if (self.lexer.token.kind == TokenKind.WS or
                    self.lexer.token.kind == TokenKind.EOL):
                self.consume_terminal(papa)
            elif self.lexer.token.kind == TokenKind.INDENT:
                self.consume_terminal(papa, ArtParseTreeKind.INDENT)
            elif self.lexer.token.kind == TokenKind.DEDENT:
                self.consume_terminal(papa, ArtParseTreeKind.DEDENT)
            elif self.lexer.token.kind == TokenKind.CORRUPTED_DEDENT:
                self.consume_terminal(papa, ArtParseTreeKind.CORRUPTED_DEDENT)
            else:
                break

    def consume_terminal(self,
                         papa,
                         tree_kind=ArtParseTreeKind.TERMINAL,
                         advance=True,
                         token=None,
                         insert_index=-1):
        """
        """
        tree = ArtAst.make_terminal_tree(tree_kind,
                                         self.grammar,
                                         token if token else self.lexer.token)
        if insert_index < 0:
            papa.add_kid(tree)
        else:
            papa.insert_kid(tree, insert_index)
        if advance:
            self.lexer.next_lexeme()
        return ParseResult(ParseResult.Status.OK, tree)

    def accept(self, papa, token_kind):
        """
        """
        if self.lexer.token.kind == token_kind:
            return self.consume_terminal(papa)
        else:
            return self.syntax_error(papa,
                                     Status.INVALID_TOKEN,
                                     f'Expected token {token_kind.name}, ')

    def accept_multiple(self, papa, token_kinds):
        """
        """
        if self.lexer.token.kind in token_kinds:
            return self.consume_terminal(papa)
        else:
            return self.syntax_error(papa,
                                     Status.INVALID_TOKEN,
                                     f'Expected one of {", ".join([v.name for v in token_kinds])}, ')

    def syntax_error(self, papa, error_code, message):
        """
        """
        self.diagnostics.add(Status(f'{message}, at {self.lexer.get_content_position()}',
                                    'art parser',
                                    error_code))
        tree = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ERRONEOUS, self.grammar)
        if papa:
            papa.add_kid(tree)
        return ParseResult(ParseResult.Status.ERROR, tree)

    def skip_tokens(self, papa, kinds):
        """
        """
        while not self.lexer.eos():
            if self.lexer.token.kind in kinds:
                break
            self.consume_terminal(papa)

    @staticmethod
    def build_recovery_synch_set(recovery_tokens,
                                 firsts,
                                 follows):
        """
        A -> α β
        SYNCH(A):
            1. a ∈ FOLLOW(A) => a ∈ SYNCH(A)
            2. place keywords that start statements in SYNCH(A)
            3. add symbols in FIRST(A) to SYNCH(A)
            https://matklad.github.io/2023/05/21/resilient-ll-parsing-tutorial.html
            ... also recursively include ancestor's FOLLOW sets into the recovery set
        """
        result = recovery_tokens
        for first in firsts:
            result += [item.name for sublist in first for item in sublist]
        for follow in follows:
            result += [item.name for sublist in follow for item in sublist]
        result = list(set(result))
        return sorted(result)