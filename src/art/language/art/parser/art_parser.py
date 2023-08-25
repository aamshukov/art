#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art parser """
from collections import deque
from collections import namedtuple
from art.framework.core.status import Status
from art.framework.frontend.parser.backtracking.\
    recursive_descent.recursive_descent_parser import RecursiveDescentParser
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_result import ParseResult
from art.language.art.ast.art_ast import ArtAst
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind
from art.language.art.parser.art_syntax_kind import ArtSyntaxKind
from art.framework.core.domain_helper import profile


class ArtParser(RecursiveDescentParser):
    """
    """
    MatchResult = namedtuple('MatchResult', 'matched token eos')

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
        #self.kind = ArtSyntaxKind.UNKNOWN  # keep tack of which syntax construction has been parsing
        self.breadcrumbs = deque()  # keep tack of syntax constructions have been parsed
        self.lexer = lexical_analyzer  # primary lexer, but might be switched to another one (import, include, etc.)

    def parse(self, *args, **kwargs):
        """
        """
        pass

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
                la_token = self.lookahead_lexeme()
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
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.LESS_THAN_SIGN)
        if match_result.matched and not match_result.eos:
            type_parameter_seq_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PARAMETER_SEQ_OPT,
                                                                   self.grammar)
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
        identifier = self.parse_identifier()
        type_parameter.add_kid(identifier.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_parameter)

    def parse_type_argument_seq_opt(self):
        """
        type_argument_seq_opt : type_argument_seq
                              | ε
                              ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.LESS_THAN_SIGN)
        if match_result.matched and not match_result.eos:
            type_argument_seq_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT_SEQ_OPT, self.grammar)
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
        type_argument : type_argument_union
                      ;
        """  # noqa
        self.inc_recursion_level()
        type_argument = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT, self.grammar)
        self.consume_noise(type_argument)
        type_argument_union = self.parse_type_argument_union()
        type_argument.add_kid(type_argument_union.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_argument)

    def parse_type_argument_union(self):
        """
        type_argument_union : TYPE
                            | type_argument_union '|' TYPE
                            ;
        """  # noqa
        self.inc_recursion_level()
        type_argument_union = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ARGUMENT_UNION, self.grammar)
        self.consume_noise(type_argument_union)
        type = self.parse_type()
        type_argument_union.add_kid(type.tree)
        self.consume_noise(type_argument_union)
        while self.lexer.token.kind == TokenKind.BITWISE_OR:
            self.consume_terminal(type_argument_union)
            type = self.parse_type()
            type_argument_union.add_kid(type.tree)
            self.consume_noise(type_argument_union)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_argument_union)

    def parse_type_alias(self):
        """
        type_alias : 'type' identifier ':' type_argument_union
                   ;
        """  # noqa
        self.inc_recursion_level()
        type_alias = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_ALIAS, self.grammar)
        self.consume_noise(type_alias)
        self.accept(type_alias, TokenKind.TYPE_KW)
        identifier = self.parse_identifier()
        type_alias.add_kid(identifier.tree)
        self.consume_noise(type_alias)
        self.accept(type_alias, TokenKind.COLON)
        type_argument_union = self.parse_type_argument_union()
        type_alias.add_kid(type_argument_union.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_alias)

    def parse_type_predicate(self):
        """
        type_predicate : type_name 'is' TYPE
                       ;
        """  # noqa
        self.inc_recursion_level()
        type_predicate = ArtAst.make_non_terminal_tree(ArtParseTreeKind.TYPE_PREDICATE, self.grammar)
        self.consume_noise(type_predicate)
        type_name = self.parse_type_name()
        type_predicate.add_kid(type_name.tree)
        self.consume_noise(type_predicate)
        self.accept(type_predicate, TokenKind.IS_KW)
        type = self.parse_type()
        type_predicate.add_kid(type.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, type_predicate)

    def parse_array_type_rank_specifier_opt(self):
        """
        array_type_rank_specifier_opt : array_type_rank_specifier
                                      | ε
                                      ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.LEFT_SQUARE_BRACKET)
        if match_result.matched and not match_result.eos:
            array_type_rank_specifier_opt = ArtAst.make_non_terminal_tree(
                ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER_OPT,
                self.grammar)
            array_type_rank_specifier = self.parse_array_type_rank_specifier()
            array_type_rank_specifier_opt.add_kid(array_type_rank_specifier.tree)
            result = ParseResult(ParseResult.Status.OK, array_type_rank_specifier_opt)
        self.dec_recursion_level()
        return result

    def parse_array_type_rank_specifier(self):
        """
        array_type_rank_specifier : '[' array_type_ranks_opt ']'
                                  ;
        """  # noqa
        self.inc_recursion_level()
        array_type_rank_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_RANK_SPECIFIER,
                                                                  self.grammar)
        self.consume_noise(array_type_rank_specifier)
        self.accept(array_type_rank_specifier, TokenKind.LEFT_SQUARE_BRACKET)
        array_type_ranks_opt = self.parse_array_type_ranks_opt()
        if array_type_ranks_opt.status != ParseResult.Status.OPTIONAL:
            array_type_rank_specifier.add_kid(array_type_ranks_opt.tree)
        self.consume_noise(array_type_rank_specifier)
        self.accept(array_type_rank_specifier, TokenKind.RIGHT_SQUARE_BRACKET)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_type_rank_specifier)

    def parse_array_type_ranks_opt(self):
        """
        array_type_ranks_opt : array_type_ranks
                             | ε
                             ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.RIGHT_SQUARE_BRACKET)
        if not match_result.matched and not match_result.eos:
            array_type_ranks_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_RANKS_OPT, self.grammar)
            parse_array_type_ranks = self.parse_array_type_ranks()
            array_type_ranks_opt.add_kid(parse_array_type_ranks.tree)
            result = ParseResult(ParseResult.Status.OK, array_type_ranks_opt)
        self.dec_recursion_level()
        return result

    def parse_array_type_ranks(self):
        """
        array_type_ranks : ','
                         | array_type_ranks ','
                         ;
        """  # noqa
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

    def parse_array_type_specifier_opt(self):
        """
        array_type_specifier_opt : array_type_specifier
                                 | ε
                                 ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.LEFT_SQUARE_BRACKET)
        if match_result.matched and not match_result.eos:
            array_type_specifier_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_SPECIFIER_OPT,
                                                                     self.grammar)
            array_type_specifier = self.parse_array_type_specifier()
            array_type_specifier_opt.add_kid(array_type_specifier.tree)
            result = ParseResult(ParseResult.Status.OK, array_type_specifier_opt)
        self.dec_recursion_level()
        return result

    def parse_array_type_specifier(self):
        """
        array_type_specifier : '[' array_modifiers_opt array_dimensions ']'
                             ;
        """  # noqa
        self.inc_recursion_level()
        array_type_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_TYPE_SPECIFIER, self.grammar)
        array_modifiers_opt = self.parse_array_modifiers_opt()
        if array_modifiers_opt.status != ParseResult.Status.OPTIONAL:
            array_type_specifier.add_kid(array_modifiers_opt.tree)
        array_dimensions = self.parse_array_dimensions()
        array_type_specifier.add_kid(array_dimensions.tree)
        self.consume_noise(array_type_specifier)
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
            array_bound = self.parse_array_upper_bound()
            array_dimension.add_kid(array_bound.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_dimension)

    def parse_array_lower_bound(self):
        """
        array_lower_bound : array_bound_expression
                          ;
        """  # noqa
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
        """  # noqa
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
        """  # noqa
        self.inc_recursion_level()
        array_bound_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_BOUND_EXPRESSION, self.grammar)
        self.consume_noise(array_bound_expression)
        non_assignment_expression = self.parse_non_assignment_expression()
        array_bound_expression.add_kid(non_assignment_expression.tree)
        #self.kind = ArtSyntaxKind.ARRAY_BOUND_EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_bound_expression)

    def parse_array_modifiers_opt(self):
        """
        array_modifiers_opt : array_modifiers ':'
                            | ε
                            ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(*ArtParser.array_modifiers())
        if match_result.matched and not match_result.eos:
            array_modifiers_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_MODIFIERS_OPT, self.grammar)
            array_modifiers = self.parse_array_modifiers()
            array_modifiers_opt.add_kid(array_modifiers.tree)
            self.consume_noise(array_modifiers_opt)
            self.accept(array_modifiers_opt, TokenKind.COLON)
            result = ParseResult(ParseResult.Status.OK, array_modifiers_opt)
        self.dec_recursion_level()
        return result

    def parse_array_modifiers(self):
        """
        array_modifiers : array_modifier
                        | array_modifiers array_modifier
                        ;
        """  # noqa
        self.inc_recursion_level()
        array_modifiers = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_MODIFIERS, self.grammar)
        self.consume_noise(array_modifiers)
        while self.array_modifier():
            self.consume_terminal(array_modifiers)
            self.consume_noise(array_modifiers)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_modifiers)

    def array_modifier(self):
        """
        array_modifier : 'column'
                       | 'row'
                       | 'jagged'
                       | 'sparse'
                       | 'unchecked'
                       | 'dynamic'
                       ;
        """  # noqa
        match self.lexer.token.kind:
            case (TokenKind.COLUMN_KW |
                  TokenKind.ROW_KW |
                  TokenKind.JAGGED_KW |
                  TokenKind.SPARSE_KW |
                  TokenKind.UNCHECKED_KW |
                  TokenKind.DYNAMIC_KW):
                return True
            case _:
                return False

    @staticmethod
    def array_modifiers():
        """
        array_modifier : 'column'
                       | 'row'
                       | 'jagged'
                       | 'sparse'
                       | 'unchecked'
                       | 'dynamic'
                       ;
        """  # noqa
        return [TokenKind.COLUMN_KW,
                TokenKind.ROW_KW,
                TokenKind.JAGGED_KW,
                TokenKind.SPARSE_KW,
                TokenKind.UNCHECKED_KW,
                TokenKind.DYNAMIC_KW]

    def parse_array_slicing_specifier(self):
        """
        array_slicing_specifier : '[' array_slice_specifier_opt ':' array_slice_specifier_opt array_slicing_step_opt ']'
                                ;
        [:] [1:] [:1] [1:1] [1::] [:1:] [::1] [1:1:] [1::1] [:1:1] [1:1:1]
        """  # noqa
        self.inc_recursion_level()
        array_slicing_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SLICING_SPECIFIER, self.grammar)
        array_slice_specifier_opt = self.parse_array_slice_specifier_opt()
        if array_slice_specifier_opt.status != ParseResult.Status.OPTIONAL:
            array_slicing_specifier.add_kid(array_slice_specifier_opt.tree)
        self.consume_noise(array_slicing_specifier)
        self.accept(array_slicing_specifier, TokenKind.COLON)
        array_slice_specifier_opt = self.parse_array_slice_specifier_opt()
        if array_slice_specifier_opt.status != ParseResult.Status.OPTIONAL:
            array_slicing_specifier.add_kid(array_slice_specifier_opt.tree)
        array_slicing_step_opt = self.parse_array_slicing_step_opt()
        if array_slicing_step_opt.status != ParseResult.Status.OPTIONAL:
            array_slicing_specifier.add_kid(array_slicing_step_opt.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_slicing_specifier)

    def parse_array_slice_specifier_opt(self):
        """
        array_slice_specifier_opt : array_slice_specifier
                                  | ε
                                  ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.INTEGER_KW,
                                  TokenKind.REAL_KW,
                                  TokenKind.BOOLEAN_KW,
                                  TokenKind.TRUE_KW,
                                  TokenKind.FALSE_KW,
                                  TokenKind.STRING_KW,
                                  TokenKind.IDENTIFIER,
                                  TokenKind.INTEGER,
                                  TokenKind.REAL,
                                  TokenKind.BOOLEAN,
                                  TokenKind.STRING,
                                  TokenKind.PLUS_SIGN,
                                  TokenKind.HYPHEN_MINUS,
                                  TokenKind.BITWISE_NOT,
                                  TokenKind.NEG_KW,
                                  TokenKind.LEFT_PARENTHESIS,
                                  TokenKind.EXCLAMATION_MARK,
                                  TokenKind.NOT_KW,
                                  TokenKind.INCREMENT,
                                  TokenKind.DECREMENT)
        if match_result.matched and not match_result.eos:
            array_slice_specifier_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SLICE_SPECIFIER_OPT,
                                                                      self.grammar)
            array_slice_specifier = self.parse_array_slice_specifier()
            array_slice_specifier_opt.add_kid(array_slice_specifier.tree)
            result = ParseResult(ParseResult.Status.OK, array_slice_specifier_opt)
        self.dec_recursion_level()
        return result

    def parse_array_slice_specifier(self):
        """
        array_slice_specifier : non_assignment_expression
                              ;
        """  # noqa
        self.inc_recursion_level()
        array_slice_specifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SLICE_SPECIFIER, self.grammar)
        self.consume_noise(array_slice_specifier)
        non_assignment_expression = self.parse_non_assignment_expression()
        array_slice_specifier.add_kid(non_assignment_expression.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_slice_specifier)

    def parse_array_slicing_step_opt(self):
        """
        array_slicing_step_opt : array_slicing_step
                               | ε
                               ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.COLON)
        if match_result.matched and not match_result.eos:
            array_slicing_step_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SLICING_STEP_OPT,
                                                                   self.grammar)
            self.consume_noise(array_slicing_step_opt)
            array_slicing_step = self.parse_array_slicing_step()
            array_slicing_step_opt.add_kid(array_slicing_step.tree)
            result = ParseResult(ParseResult.Status.OK, array_slicing_step_opt)
        self.dec_recursion_level()
        return result

    def parse_array_slicing_step(self):
        """
        array_slicing_step : ':' array_slice_specifier_opt
                           ;
        """  # noqa
        self.inc_recursion_level()
        array_slicing_step = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_SLICING_STEP, self.grammar)
        self.consume_noise(array_slicing_step)
        self.accept(array_slicing_step, TokenKind.COLON)
        array_slice_specifier_opt = self.parse_array_slice_specifier_opt()
        if array_slice_specifier_opt.status != ParseResult.Status.OPTIONAL:
            array_slicing_step.add_kid(array_slice_specifier_opt.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_slicing_step)

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
        """  # noqa
        match self.lexer.token.kind:
            case (TokenKind.INTEGER_KW |
                  TokenKind.REAL_KW |
                  TokenKind.BOOLEAN_KW |
                  TokenKind.STRING_KW):
                return True
            case _:
                return False

    def parse_expression(self):
        """
        expression : conditional_expression
                   ;
        """  # noqa
        self.inc_recursion_level()
        expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.EXPRESSION, self.grammar)
        self.consume_noise(expression)
        conditional_expression = self.parse_conditional_expression()
        expression.add_kid(conditional_expression.tree)
        self.kind = ArtSyntaxKind.EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, expression)

    def parse_conditional_expression(self):
        """
        conditional_expression : conditional_or_expression
                               | conditional_or_expression '?' expression ':' expression
                               ;
        """  # noqa
        conditional_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_EXPRESSION, self.grammar)
        self.consume_noise(conditional_expression)
        conditional_or_expression = self.parse_conditional_or_expression()
        conditional_expression.add_kid(conditional_or_expression.tree)
        self.consume_noise(conditional_expression)
        while self.lexer.token.kind == TokenKind.QUESTION_MARK:
            self.consume_terminal(conditional_expression)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression.tree)
            self.consume_noise(conditional_expression)
            self.accept(conditional_expression, TokenKind.COLON)
            self.consume_noise(conditional_expression)
            expression = self.parse_expression()
            conditional_expression.add_kid(expression.tree)
        self.kind = ArtSyntaxKind.CONDITIONAL_EXPRESSION
        return ParseResult(ParseResult.Status.OK, conditional_expression)

    def parse_unary_expression(self):
        """
        unary_expression : primary_expression
                         | '+' unary_expression
                         | '-' unary_expression
                         | '!' unary_expression
                         | 'not' unary_expression
                         | '~' unary_expression
                         | pre_increment_expression
                         | pre_decrement_expression
                         ;
        """  # noqa
        unary_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.UNARY_EXPRESSION, self.grammar)
        while True:
            self.consume_noise(unary_expression)
            match self.lexer.token.kind:
                case (TokenKind.PLUS_SIGN |
                      TokenKind.HYPHEN_MINUS |
                      TokenKind.EXCLAMATION_MARK |
                      TokenKind.NOT_KW |
                      TokenKind.BITWISE_NOT |
                      TokenKind.INCREMENT |
                      TokenKind.DECREMENT):
                    self.consume_terminal(unary_expression)
                    unary_expression_postfix = self.parse_unary_expression()
                    unary_expression.add_kid(unary_expression_postfix.tree)
                case _:
                    primary_expression = self.parse_primary_expression()
                    unary_expression.add_kid(primary_expression.tree)
                    break
        self.kind = ArtSyntaxKind.UNARY_EXPRESSION
        return ParseResult(ParseResult.Status.OK, unary_expression)

    def parse_primary_expression(self):
        """
        primary_expression : literal
                           | identifier
                           | member_access
                           | invocation_expression
                           | post_increment_expression
                           | post_decrement_expression
                           | array_literal
                           | array_element_access
                           | array_slicing_expression
                           | object_creation_expression
                           | parenthesized_expression
                           ;
        """  # noqa
        self.inc_recursion_level()
        primary_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.PRIMARY_EXPRESSION, self.grammar)
        primary_expression_parts = list()
        primary_expression_parts.extend(self.consume_noise(primary_expression, link=False))
        # phase I  - parse 'prefix' part of primary expression
        #   primary_expression          : literal
        #                               | identifier
        #                               | array_literal
        #                               | object_literal
        #   member_access               : integral_type ...
        #                               | primary_expression ...
        #   invocation_expression       : primary_expression ...
        #   post_increment_expression   : primary_expression ...
        #   post_decrement_expression   : primary_expression ...
        #   array_element_access        : primary_expression ...
        #   array_slicing_expression    : primary_expression ...
        #   object_creation_expression  : TYPE ...
        #   parenthesized_expression    : '(' expression ')'
        if self.literal():
            primary_expression_parts.append(self.parse_literal(primary_expression, link=False))
        elif self.lexer.token.kind == TokenKind.IDENTIFIER:
            primary_expression_parts.append(self.parse_identifier())
        elif self.integral_type():
            primary_expression_parts.append(self.consume_terminal(primary_expression,
                                                                  ArtParseTreeKind.INTEGRAL_TYPE,
                                                                  link=False))
        elif self.lexer.token.kind == TokenKind.LEFT_PARENTHESIS:
            primary_expression_parts.append(self.parse_parenthesized_expression())
        elif self.lexer.token.kind == TokenKind.LEFT_SQUARE_BRACKET:
            pass  # array_literal
        elif self.lexer.token.kind == TokenKind.LEFT_CURLY_BRACKET:
            pass  # object_literal
            # self.accept(primary_expression, TokenKind.LEFT_CURLY_BRACKET)
            # object_literal = None  #??self.parse_object_literal()
            # primary_expression.add_kid(object_literal.tree)
            # self.consume_noise(primary_expression)
            # self.accept(primary_expression, TokenKind.RIGHT_CURLY_BRACKET)
        else:
            if self.lexer.eos:
                erroneous = self.syntax_error(primary_expression,
                                              Status.INVALID_TOKEN,
                                              f'Expression expected '
                                              f'{self.lexer.token.kind.name}',
                                              link=False)
            else:
                erroneous = self.syntax_error(primary_expression,
                                              Status.INVALID_TOKEN,
                                              f'Expression expected, unexpected EOS '
                                              f'{self.lexer.token.kind.name}',
                                              link=False)
            primary_expression_parts.append(erroneous)
        # phase II  - parse 'postfix' part of primary expression
        #   member_access              : ... '.' identifier type_argument_seq_opt
        #   invocation_expression      : ... '(' arguments_opt ')'
        #   array_element_access       : ... '[' argument_values ']'
        #   array_slicing_expression   : ...  array_slicing_specifier
        #   object_creation_expression : ... '{' arguments_opt '}'
        #                              | ... array_type_specifier '{' array_initializer_opt '}'
        #   post_increment_expression  : ... '++'
        #   post_decrement_expression  : ... '--'
        while True:
            primary_expression_parts.extend(self.consume_noise(primary_expression, link=False))
            if self.lexer.token.kind == TokenKind.DOT:
                member_access = ArtAst.make_non_terminal_tree(ArtParseTreeKind.MEMBER_ACCESS, self.grammar)
                for primary_expression_part in primary_expression_parts:
                    member_access.add_kid(primary_expression_part.tree)
                primary_expression_parts.clear()
                self.consume_terminal(member_access)
                identifier = self.parse_identifier()
                member_access.add_kid(identifier.tree)
                primary_expression_parts.append(ParseResult(ParseResult.Status.OK, member_access))
            elif self.lexer.token.kind == TokenKind.LEFT_PARENTHESIS:
                invocation_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.INVOCATION_EXPRESSION,
                                                                      self.grammar)
                for primary_expression_part in primary_expression_parts:
                    invocation_expression.add_kid(primary_expression_part.tree)
                primary_expression_parts.clear()
                self.accept(invocation_expression, TokenKind.LEFT_PARENTHESIS)
                arguments_opt = self.parse_arguments_opt()
                if arguments_opt.status != ParseResult.Status.OPTIONAL:
                    invocation_expression.add_kid(arguments_opt.tree)
                self.consume_noise(invocation_expression)
                self.accept(invocation_expression, TokenKind.RIGHT_PARENTHESIS)
                primary_expression_parts.append(ParseResult(ParseResult.Status.OK, invocation_expression))
            elif self.lexer.token.kind == TokenKind.LEFT_SQUARE_BRACKET:
                array_elements = self.parse_array_elements()
                for k, primary_expression_part in enumerate(primary_expression_parts):
                    array_elements.tree.insert_kid(primary_expression_part.tree, index=k)
                primary_expression_parts.clear()
                primary_expression_parts.append(array_elements)
            elif self.lexer.token.kind == TokenKind.LEFT_CURLY_BRACKET:
                pass  # object_literal
                # self.consume_terminal(primary_expression)
                # object_literal = None  #?? self.parse_object_literal()
                # primary_expression.add_kid(object_literal.tree)
                # self.consume_noise(primary_expression)
                # self.accept(primary_expression, TokenKind.RIGHT_CURLY_BRACKET)
            elif self.lexer.token.kind == TokenKind.INCREMENT:
                post_increment_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.POST_INCREMENT_EXPRESSION,
                                                                          self.grammar)
                for primary_expression_part in primary_expression_parts:
                    post_increment_expression.add_kid(primary_expression_part.tree)
                primary_expression_parts.clear()
                self.consume_terminal(post_increment_expression)
                primary_expression_parts.append(ParseResult(ParseResult.Status.OK, post_increment_expression))
            elif self.lexer.token.kind == TokenKind.DECREMENT:
                post_decrement_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.POST_DECREMENT_EXPRESSION,
                                                                          self.grammar)
                for primary_expression_part in primary_expression_parts:
                    post_decrement_expression.add_kid(primary_expression_part.tree)
                primary_expression_parts.clear()
                self.consume_terminal(post_decrement_expression)
                primary_expression_parts.append(ParseResult(ParseResult.Status.OK, post_decrement_expression))
            else:
                break
        for primary_expression_part in primary_expression_parts:
            primary_expression.add_kid(primary_expression_part.tree)
        #self.kind = ArtSyntaxKind.PRIMARY_EXPRESSION
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, primary_expression)

    # @profile('Parson build first set...')
    def parse_array_elements(self):
        """
        '[' argument_values ']'
        '[' array_modifiers_opt array_dimensions ']'
        '[' array_slicing_specifier ']'
        """  # noqa
        self.inc_recursion_level()
        array_elements = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARRAY_ELEMENT_ACCESS, self.grammar)
        cached_trees = list()
        cached_trees.extend(self.consume_noise(array_elements, link=False))
        cached_trees.append(self.accept(array_elements, TokenKind.LEFT_SQUARE_BRACKET, link=False))
        match_result = self.match(*ArtParser.array_modifiers())  # might start array specifier
        if match_result.matched and not match_result.eos:
            array_elements = self.parse_array_type_specifier().tree
            for k, cached_tree in enumerate(cached_trees):
                array_elements.insert_kid(cached_tree.tree, index=k)
            cached_trees.clear()
        else:
            match_result = self.match(TokenKind.COLON)  # might start slicing
            if match_result.matched and not match_result.eos:
                array_elements = self.parse_array_slicing_specifier().tree
                for k, cached_tree in enumerate(cached_trees):
                    array_elements.insert_kid(cached_tree.tree, index=k)
                cached_trees.clear()
            else:
                argument_values = self.parse_argument_values_tentative()
                if argument_values.status == ParseResult.Status.BACKTRACK:
                    if argument_values.hint == TokenKind.RANGE:
                        array_elements = self.parse_array_type_specifier().tree
                        for k, cached_tree in enumerate(cached_trees):
                            array_elements.insert_kid(cached_tree.tree, index=k)
                        cached_trees.clear()
                    elif argument_values.hint == TokenKind.COLON:
                        array_elements = self.parse_array_slicing_specifier().tree
                        for k, cached_tree in enumerate(cached_trees):
                            array_elements.insert_kid(cached_tree.tree, index=k)
                        cached_trees.clear()
                    else:
                        cached_trees.append(self.syntax_error(array_elements,
                                                              Status.INVALID_ARRAY_ELEMENTS,
                                                              f'Expected array elements '
                                                              f'{self.lexer.token.kind.name}'))
                else:
                    cached_trees.append(argument_values)
        for cached_tree in cached_trees:
            array_elements.add_kid(cached_tree.tree)
        self.consume_noise(array_elements)
        self.accept(array_elements, TokenKind.RIGHT_SQUARE_BRACKET)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, array_elements)

    def parse_parenthesized_expression(self):
        """
        """  # noqa
        self.inc_recursion_level()
        parenthesized_expression = ArtAst.make_non_terminal_tree(ArtParseTreeKind.PARENTHESIZED_EXPRESSION,
                                                                 self.grammar)
        self.consume_noise(parenthesized_expression)
        self.accept(parenthesized_expression, TokenKind.LEFT_PARENTHESIS)
        expression = self.parse_expression()
        parenthesized_expression.add_kid(expression.tree)
        self.consume_noise(parenthesized_expression)
        self.accept(parenthesized_expression, TokenKind.RIGHT_PARENTHESIS)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, parenthesized_expression)

    def parse_pre_increment_expression(self):
        """
        """  # noqa

    def parse_pre_decrement_expression(self):
        """
        """  # noqa

    def parse_post_increment_expression(self):
        """
        """  # noqa

    def parse_post_decrement_expression(self):
        """
        """  # noqa

    def parse_multiplicative_expression(self):
        """
        """  # noqa

    def parse_additive_expression(self):
        """
        """  # noqa

    def parse_relational_expression(self):
        """
        """  # noqa

    def parse_equality_expression(self):
        """
        """  # noqa

    def parse_and_expression(self):
        """
        """  # noqa

    def parse_exclusive_or_expression(self):
        """
        """  # noqa

    def parse_inclusive_or_expression(self):
        """
        """  # noqa

    def parse_conditional_and_expression(self):
        """
        """  # noqa

    def parse_conditional_or_expression(self):
        """
        """  # noqa
        erroneous = ArtAst.make_non_terminal_tree(ArtParseTreeKind.CONDITIONAL_OR_EXPRESSION,
                                                  self.grammar)
        #self.kind = ArtSyntaxKind.CONDITIONAL_OR_EXPRESSION
        return ParseResult(ParseResult.Status.OK, erroneous)

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
        """  # noqa
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
                result = self.consume_terminal(papa)
            case _:
                result = self.syntax_error(papa,
                                           Status.INVALID_TOKEN,
                                           f'Expected assignment operator, '
                                           f'found {self.lexer.token.kind.name}')
        self.dec_recursion_level()
        return result

    def parse_arguments_opt(self):
        """
        arguments_opt : arguments
                      | ε
                      ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.RIGHT_PARENTHESIS, TokenKind.RIGHT_CURLY_BRACKET)
        if not match_result.matched and not match_result.eos:
            arguments_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENTS_OPT, self.grammar)
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
        argument : argument_name_opt argument_value argument_modifiers_opt
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
        argument_modifiers_opt = self.parse_argument_modifiers_opt()
        if argument_modifiers_opt.status != ParseResult.Status.OPTIONAL:
            argument.add_kid(argument_modifiers_opt.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument)

    def parse_argument_name_opt(self):
        """
        argument_name_opt : argument_name
                          | ε
                          ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.IDENTIFIER)
        if match_result.matched and not match_result.eos:
            argument_name_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_NAME_OPT, self.grammar)
            la_token = self.lookahead_lexeme()
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
        identifier = self.parse_identifier()
        argument_name.add_kid(identifier)
        self.consume_noise(argument_name)
        self.accept(argument_name, TokenKind.COLON)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_name)

    def parse_argument_values(self):
        """
        argument_values : argument_value
                        | argument_values ',' argument_value
                        ;
        """  # noqa
        self.inc_recursion_level()
        argument_values = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUES, self.grammar)
        self.consume_noise(argument_values)
        argument_value = self.parse_argument_value()
        argument_values.add_kid(argument_value.tree)
        self.consume_noise(argument_values)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(argument_values)
            argument_value = self.parse_argument_value()
            argument_values.add_kid(argument_value.tree)
            self.consume_noise(argument_values)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_values)

    def parse_argument_values_tentative(self):
        """
        argument_values : argument_value
                        | argument_values ',' argument_value
                        ;
        """  # noqa
        self.inc_recursion_level()
        status = ParseResult.Status.OK
        hint = TokenKind.UNKNOWN
        self.lexer.snapshot()
        argument_values = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUES, self.grammar)
        self.consume_noise(argument_values)
        argument_value = self.parse_argument_value()
        argument_values.add_kid(argument_value.tree)
        self.consume_noise(argument_values)
        while True:
            if self.lexer.token.kind == TokenKind.COMMA:
                self.consume_terminal(argument_values)
                argument_value = self.parse_argument_value()
                argument_values.add_kid(argument_value.tree)
            elif self.lexer.token.kind == TokenKind.RANGE or self.lexer.token.kind == TokenKind.COLON:
                status = ParseResult.Status.BACKTRACK
                hint = self.lexer.token.kind
                break
            else:
                break
            self.consume_noise(argument_values)
        if status == ParseResult.Status.BACKTRACK:
            self.lexer.rewind()
        else:
            self.lexer.tokenizer.discard()
        self.dec_recursion_level()
        return ParseResult(status, argument_values, hint=hint)

    def parse_argument_value_opt(self):
        """
        argument_value_opt : argument_value
                           | ε
                           ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.STRING,
                                  TokenKind.IDENTIFIER,
                                  TokenKind.REAL,
                                  TokenKind.BOOLEAN_KW,
                                  TokenKind.BOOLEAN,
                                  TokenKind.PLUS_SIGN,
                                  TokenKind.STRING_KW,
                                  TokenKind.INTEGER_KW,
                                  TokenKind.REAL_KW,
                                  TokenKind.EXCLAMATION_MARK,
                                  TokenKind.BITWISE_NOT,
                                  TokenKind.INTEGER,
                                  TokenKind.INCREMENT,
                                  TokenKind.LEFT_PARENTHESIS,
                                  TokenKind.HYPHEN_MINUS,
                                  TokenKind.DECREMENT,
                                  TokenKind.REAL_KW)
        if match_result.matched and not match_result.eos:
            argument_value_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUE_OPT, self.grammar)
            argument_value = self.parse_argument_value()
            argument_value_opt.add_kid(argument_value.tree)
            result = ParseResult(ParseResult.Status.OK, argument_value_opt)
        self.dec_recursion_level()
        return result

    def parse_argument_value(self):
        """
        argument_value : argument_value_union
                       ;
        """  # noqa
        self.inc_recursion_level()
        argument_value = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUE, self.grammar)
        argument_value_union = self.parse_argument_value_union()
        argument_value.add_kid(argument_value_union.tree)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_value)

    def parse_argument_value_union(self):
        """
        argument_value_union : non_assignment_expression
                             | argument_value_union '|' non_assignment_expression
                             ;
        """  # noqa
        self.inc_recursion_level()
        argument_value_union = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_VALUE_UNION, self.grammar)
        self.consume_noise(argument_value_union)
        non_assignment_expression = self.parse_non_assignment_expression()
        argument_value_union.add_kid(non_assignment_expression.tree)
        self.consume_noise(argument_value_union)
        while self.lexer.token.kind == TokenKind.BITWISE_OR:
            self.consume_terminal(argument_value_union)
            non_assignment_expression = self.parse_non_assignment_expression()
            argument_value_union.add_kid(non_assignment_expression.tree)
            self.consume_noise(argument_value_union)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_value_union)

    def parse_argument_modifiers_opt(self):
        """
        argument_modifiers_opt : argument_modifiers
                               | ε
                               ;
        """  # noqa
        self.inc_recursion_level()
        result = ParseResult(ParseResult.Status.OPTIONAL)
        match_result = self.match(TokenKind.LAZY_KW, TokenKind.OPTIONAL_KW)
        if match_result.matched and not match_result.eos:
            argument_modifiers_opt = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_MODIFIERS_OPT,
                                                                   self.grammar)
            argument_modifiers = self.parse_argument_modifierst()
            argument_modifiers_opt.add_kid(argument_modifiers.tree)
            result = ParseResult(ParseResult.Status.OK, argument_modifiers_opt)
        self.dec_recursion_level()
        return result

    def parse_argument_modifiers(self):
        """
        argument_modifiers : argument_modifier
                           | argument_modifiers argument_modifier
                           ;
        """  # noqa
        self.inc_recursion_level()
        argument_modifiers = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ARGUMENT_MODIFIERS, self.grammar)
        self.consume_noise(argument_modifiers)
        while self.argument_modifier():
            self.consume_terminal(argument_modifiers)
            self.consume_noise(argument_modifiers)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, argument_modifiers)

    def argument_modifier(self):
        """
        argument_modifier : 'lazy'
                          | 'lz'
                          | 'opt'
                          | 'optional'
                          ;
        """  # noqa
        match self.lexer.token.kind:
            case (TokenKind.LAZY_KW | TokenKind.OPTIONAL_KW):
                return True
            case _:
                return False

    def parse_fully_qualified_identifier(self):
        """
        fully_qualified_identifier : identifier
                                   | fully_qualified_identifier '.' identifier
                                   ;
        """  # noqa
        self.inc_recursion_level()
        fq_identifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.FULLY_QUALIFIED_IDENTIFIER, self.grammar)
        identifier = self.parse_identifier()
        fq_identifier.add_kid(identifier.tree)
        self.consume_noise(fq_identifier)
        while self.lexer.token.kind == TokenKind.DOT:
            self.consume_terminal(fq_identifier)
            identifier = self.parse_identifier()
            fq_identifier.add_kid(identifier.tree)
            if identifier.status != ParseResult.Status.OK:
                break
            self.consume_noise(fq_identifier)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, fq_identifier)

    def parse_identifiers(self):
        """
        identifiers : identifier
                    | identifiers ',' identifier
                    ;
        """  # noqa
        self.inc_recursion_level()
        identifiers = ArtAst.make_non_terminal_tree(ArtParseTreeKind.IDENTIFIERS, self.grammar)
        identifier = self.parse_identifier()
        identifiers.add_kid(identifier.tree)
        self.consume_noise(identifiers)
        while self.lexer.token.kind == TokenKind.COMMA:
            self.consume_terminal(identifiers)
            identifier = self.parse_identifier()
            identifiers.add_kid(identifier.tree)
            if identifier.status != ParseResult.Status.OK:
                break
            self.consume_noise(identifiers)
        self.dec_recursion_level()
        return ParseResult(ParseResult.Status.OK, identifiers)

    def parse_identifier(self):
        """
        identifier : 'identifier' type_argument_seq_opt
                   ;
        """  # noqa
        self.inc_recursion_level()
        identifier = ArtAst.make_non_terminal_tree(ArtParseTreeKind.IDENTIFIER, self.grammar)
        self.consume_noise(identifier)
        self.accept(identifier, TokenKind.IDENTIFIER, ArtParseTreeKind.TERMINAL)
        type_argument_seq_opt = self.parse_type_argument_seq_opt()
        if type_argument_seq_opt.status != ParseResult.Status.OPTIONAL:
            identifier.add_kid(type_argument_seq_opt.tree)
        self.dec_recursion_level()
        return ParseResult(self.parse_result(ParseResult.Status.OK), identifier)

    def parse_literal(self, papa, link=True):
        """
        literal : 'integer_number_literal'
                | 'real_number_literal'
                | 'string_literal'
                | 'boolean_literal'
                ;
        """  # noqa
        self.inc_recursion_level()
        if self.literal():
            result = self.consume_terminal(papa, ArtParseTreeKind.LITERAL, link=link)
        else:
            result = self.syntax_error(papa,
                                       Status.INVALID_TOKEN,
                                       f'Expected literal, found {self.lexer.token.kind.name}',
                                       link=link)
        self.dec_recursion_level()
        return result

    def literal(self):
        """
        """  # noqa
        match self.lexer.token.kind:
            case (TokenKind.INTEGER |
                  TokenKind.REAL |
                  TokenKind.STRING |
                  TokenKind.TRUE_KW |
                  TokenKind.FALSE_KW):
                return True
            case _:
                return False

    def consume_noise(self, papa, link=True):
        """
        """  # noqa
        results = list()
        while not self.lexer.eos():
            if (self.lexer.token.kind == TokenKind.WS or
                    self.lexer.token.kind == TokenKind.EOL):
                results.append(self.consume_terminal(papa, link=link))
            elif self.lexer.token.kind == TokenKind.INDENT:
                results.append(self.consume_terminal(papa, ArtParseTreeKind.INDENT, link=link))
            elif self.lexer.token.kind == TokenKind.DEDENT:
                results.append(self.consume_terminal(papa, ArtParseTreeKind.DEDENT, link=link))
            elif self.lexer.token.kind == TokenKind.CORRUPTED_DEDENT:
                results.append(self.consume_terminal(papa, ArtParseTreeKind.CORRUPTED_DEDENT, link=link))
            else:
                break
        return results

    def consume_terminal(self,
                         papa,
                         tree_kind=ArtParseTreeKind.TERMINAL,
                         advance=True,
                         token=None,
                         insert_index=-1,
                         link=True):
        """
        """  # noqa
        tree = ArtAst.make_terminal_tree(tree_kind,
                                         self.grammar,
                                         token if token else self.lexer.token)
        if link:
            if insert_index < 0:
                papa.add_kid(tree)
            else:
                papa.insert_kid(tree, insert_index)
        if advance:
            self.lexer.next_lexeme()
        return ParseResult(ParseResult.Status.OK, tree)

    def accept(self,
               papa,
               token_kind,
               tree_kind=ArtParseTreeKind.TERMINAL,
               link=True):
        """
        """  # noqa
        if self.lexer.token.kind == token_kind:
            return self.consume_terminal(papa, tree_kind, link=link)
        else:
            return self.syntax_error(papa,
                                     Status.INVALID_TOKEN,
                                     f'Expected token {token_kind.name}, ',
                                     link=link)

    def accept_multiple(self,
                        papa,
                        token_kinds,
                        tree_kind=ArtParseTreeKind.TERMINAL,
                        link=True):
        """
        """  # noqa
        if self.lexer.token.kind in token_kinds:
            return self.consume_terminal(papa, tree_kind, link=link)
        else:
            return self.syntax_error(papa,
                                     Status.INVALID_TOKEN,
                                     f'Expected one of {", ".join([v.name for v in token_kinds])}, ',
                                     link=link)

    def match(self, *token_kinds):
        """
        """  # noqa
        token = self.lexer.token
        if token.kind in token_kinds:
            result = ArtParser.MatchResult(True, token, token.kind == TokenKind.EOS)
        elif token.kind in [TokenKind.WS,
                            TokenKind.EOL,
                            TokenKind.INDENT,
                            TokenKind.DEDENT,
                            TokenKind.CORRUPTED_DEDENT]:
            la_token = self.lookahead_lexeme()
            result = ArtParser.MatchResult(la_token.kind in token_kinds, la_token, la_token.kind == TokenKind.EOS)
        else:
            result = ArtParser.MatchResult(False, token, token.kind == TokenKind.EOS)
        return result

    def lookahead_lexeme(self, skip=None):
        """
        """  # noqa
        if not skip:
            skip = [TokenKind.WS,
                    TokenKind.EOL,
                    TokenKind.INDENT,
                    TokenKind.DEDENT,
                    TokenKind.CORRUPTED_DEDENT]
        return self.lexer.lookahead_lexeme(skip)

    def syntax_error(self, papa, error_code, message, link=True):
        """
        """  # noqa
        self.diagnostics.add(Status(f'{message}, at {self.lexer.get_content_position()}',
                                    'art parser',
                                    error_code))
        tree = ArtAst.make_non_terminal_tree(ArtParseTreeKind.ERRONEOUS, self.grammar)
        if link and papa:
            papa.add_kid(tree)
        return ParseResult(ParseResult.Status.ERROR, tree)

    def parse_result(self, status):
        """
        """  # noqa
        return status if self.diagnostics.status else ParseResult.Status.ERROR

    def skip_tokens(self, papa, kinds, link=True):
        """
        """  # noqa
        while not self.lexer.eos():
            if self.lexer.token.kind in kinds:
                break
            self.consume_terminal(papa, link=link)
