#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import inspect
import unittest
from art.framework.core.domain_helper import DomainHelper
from art.framework.core.logger import Logger
from art.framework.core.diagnostics import Diagnostics
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_algorithms import GrammarAlgorithms
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind
from art.framework.frontend.parser.parse_context import ParseContext
from art.framework.frontend.parser.parse_domain_helper import ParseTreeDomainHelper
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.language.art.ast.art_ast import ArtAst
from art.language.art.grammar.art_grammar import ArtGrammar
from art.language.art.parser.art_parse_tree_kind import ArtParseTreeKind
from art.language.art.parser.art_parser import ArtParser
from art.language.art.parser.art_tokenizer import ArtTokenizer


class Test(unittest.TestCase):
    syntactic_grammar = """
    # TYPE
    TYPE                                : integral_type array_type_rank_specifier_opt
                                        | type_name array_type_rank_specifier_opt
                                        | type_parameter array_type_rank_specifier_opt
                                        ;

    type_name                           : fully_qualified_identifier
                                        ;

    type_parameter_seq_opt              : type_parameter_seq
                                        | ε
                                        ;

    type_parameter_seq                  : '<' type_parameters '>'
                                        ;

    type_parameters                     : type_parameter                                                                    # type_parameter (',' type_parameter)*
                                        | type_parameters ',' type_parameter
                                        ;

    type_parameter                      : identifier
                                        ;

    type_argument_seq_opt               : type_argument_seq
                                        | ε
                                        ;

    type_argument_seq                   : '<' type_arguments '>'
                                        ;

    type_arguments                      : type_argument                                                                     # type_argument (',' type_argument)*
                                        | type_arguments ',' type_argument
                                        ;

    type_argument                       : TYPE
                                        ;

    array_type_rank_specifier_opt       : array_type_rank_specifier
                                        | ε
                                        ;

    array_type_rank_specifier           : '[' array_type_ranks_opt ']'
                                        ;

    array_type_ranks_opt                : array_type_ranks
                                        | ε
                                        ;

    array_type_ranks                    : ','
                                        | array_type_ranks ','
                                        ;

    array_type_specifier_opt            : array_type_specifier
                                        | ε
                                        ;

    array_type_specifier                : '[' array_dimensions ']' array_modifiers_opt                                      # zero based, checked array, row based, optionally column based and/or unchecked
                                        ;

    array_dimensions                    : array_dimension                                                                   # array_dimension (',' array_dimension)*
                                        | array_dimensions ',' array_dimension                                              # all ',' as a separator of a dimension
                                        ;

    array_dimension                     : array_upper_bound                                                                 # array_lower_bound ('..' array_upper_bound)?  a[2]
                                        | array_lower_bound '..' array_upper_bound                                          # array_lower_bound ('..' array_upper_bound)?  a[1..2]
                                        ;

    array_lower_bound                   : array_bound_expression
                                        ;

    array_upper_bound                   : array_bound_expression
                                        ;

    array_bound_expression              : non_assignment_expression                                                         # must evaluate to compilation time constant integer
                                        ;

    array_modifiers_opt                 : array_modifiers
                                        | ε
                                        ;

    array_modifiers                     : array_modifier
                                        | array_modifiers ',' array_modifier
                                        ;

    array_modifier                      : 'column'                                                                          # column based array specifier
                                        | 'row'                                                                             # row based array specifier - default
                                        | 'jagged'                                                                          # array of arrays, possibly of different sizes
                                        | 'unchecked'                                                                       # unchecked array specifier
                                        ;

    integral_type_opt                   : integral_type
                                        | ε
                                        ;

    integral_type                       : 'int'
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

    # EXPRESSIONS
    expressions                         : expression
                                        | expressions ',' expression
                                        ;

    expression                          : non_assignment_expression
                                        | assignment_expression
                                        ;

    non_assignment_expression           : conditional_expression
                                        ;

    assignment_expression               : unary_expression assignment_operator expression
                                        ;

    unary_expression                    : primary_expression
                                        | '+' unary_expression
                                        | '-' unary_expression
                                        | '!' unary_expression
                                        | '~' unary_expression
                                        | pre_increment_expression                                                          # ++i
                                        | pre_decrement_expression                                                          # --i
                                        ;

    multiplicative_expression           : unary_expression
                                        | multiplicative_expression '*' unary_expression
                                        | multiplicative_expression '/' unary_expression
                                        | multiplicative_expression '%' unary_expression
                                        ;

    additive_expression                 : multiplicative_expression
                                        | additive_expression '+' multiplicative_expression
                                        | additive_expression '-' multiplicative_expression
                                        ;

    shift_expression                    : additive_expression
                                        | shift_expression '<<' additive_expression
                                        | shift_expression '>>' additive_expression                                         # > >
                                        ;

    relational_expression               : shift_expression
                                        | relational_expression '<' shift_expression
                                        | relational_expression 'lt' shift_expression
                                        | relational_expression '>' shift_expression
                                        | relational_expression 'gt' shift_expression
                                        | relational_expression '<=' shift_expression
                                        | relational_expression 'le' shift_expression
                                        | relational_expression '>=' shift_expression
                                        | relational_expression 'ge' shift_expression
                                        | relational_expression 'is' TYPE
                                        ;

    equality_expression                 : relational_expression
                                        | equality_expression '==' relational_expression
                                        | equality_expression 'eq' relational_expression
                                        | equality_expression '!=' relational_expression
                                        | equality_expression 'ne' relational_expression
                                        ;

    and_expression                      : equality_expression
                                        | and_expression '&' equality_expression
                                        ;

    exclusive_or_expression             : and_expression
                                        | exclusive_or_expression '^' and_expression
                                        ;

    inclusive_or_expression             : exclusive_or_expression
                                        | inclusive_or_expression '|' exclusive_or_expression
                                        ;

    conditional_and_expression          : inclusive_or_expression
                                        | conditional_and_expression '&&' inclusive_or_expression
                                        | conditional_and_expression 'and' inclusive_or_expression
                                        ;

    conditional_or_expression           : conditional_and_expression
                                        | conditional_or_expression '||' conditional_and_expression
                                        | conditional_or_expression 'or' conditional_and_expression
                                        ;

    primary_expression                  : literal                                                                           # 5, 3.14, 'text', true
                                        | identifier type_argument_seq_opt
                                        | member_access                                                                     # Foo.name, foo.name
                                        | array_element_access                                                              # array[0]
                                        | invocation_expression                                                             # foo(...)
                                        | post_increment_expression                                                         # i++
                                        | post_decrement_expression                                                         # i--
                                        | object_creation_expression
    #                                    | array_creation_expression
                                        | parenthesized_expression                                                          # '(' expression ')'
                                        ;

    conditional_expression              : conditional_or_expression
                                        | conditional_or_expression '?' expression ':' expression
                                        ;

    member_access                       : primary_expression '.' identifier type_argument_seq_opt                           # geo.point<T>, point<real>
                                        ;

    invocation_expression               : primary_expression '(' arguments_opt ')'
                                        ;

    pre_increment_expression            : '++' unary_expression
                                        ;

    pre_decrement_expression            : '--' unary_expression
                                        ;

    post_increment_expression           : primary_expression '++'
                                        ;

    post_decrement_expression           : primary_expression '--'
                                        ;

    object_creation_expression          : TYPE '{' arguments_opt '}'
                                        ;

    parenthesized_expression            : '(' expression ')'
                                        ;

    array_element_access                : primary_expression '[' arguments ']'                                              # except array creation
                                        ;

    arguments_opt                       : arguments
                                        | ε
                                        ;

    arguments                           : argument
                                        | arguments ',' argument
                                        ;

    argument                            : argument_name_opt argument_value
                                        ;

    argument_name_opt                   : argument_name
                                        | ε
                                        ;

    argument_name                       : identifier ':'
                                        ;

    argument_value                      : expression lazy_opt                                                               # lazy parameters evaluation only in invocation_expression
                                        ;

    lazy_opt                            : 'lazy'                                                                            # lazy parameters evaluation
                                        | ε
                                        ;

    assignment_operator                 : '='
                                        | '+='
                                        | '-='
                                        | '*='
                                        | '/='
                                        | '%='
                                        | '&='
                                        | '|='
                                        | '^='
                                        | '<<='
                                        | '>>='                                                                             # > >=
                                        ;

    fully_qualified_identifier          : identifier type_argument_seq_opt                                                  # A<T>
                                        | fully_qualified_identifier '.' identifier type_argument_seq_opt                   # A<T>.B<U>.C<A<B<U>>>
                                        ;

    identifiers                         : identifier
                                        | identifiers ',' identifier
                                        ;

    identifier                          : 'identifier'
                                        ;

    literal                             : 'integer_number_literal'
                                        | 'real_number_literal'
                                        | 'boolean_literal'                                                                 # true false
                                        | 'string_literal'
                                        ;

    terminal                            : 'terminal'                                                                        # wrapper for terminals
                                        ;

    INDENT                              : 'indent'
                                        ;

    DEDENT                              : 'dedent'
                                        ;

    """  # noqa
    grammar = None

    def __init__(self, *args, **kwargs):
        """
        """
        super(Test, self).__init__(*args, **kwargs)

    @staticmethod
    def dump_rules_la(grammar, logger, k=1):
        logger.info('Rules LA')
        for rule in grammar.rules:
            if 'PRIMARY_EXPRESSION' in rule.name:
                pass
            la = GrammarAlgorithms.build_la_set_rule(grammar, rule, k)
            la_str = f'{rule.name}: {GrammarSymbol.sets_to_string(la)}'
            logger.info(la_str)

    @classmethod
    def setUp(cls):
        DomainHelper.increase_recursion_limit()
        if not cls.grammar:
            k = 1
            logger = Logger(path=r'd:\tmp\art', mode='w')
            grammar = ArtGrammar(logger=logger)
            grammar.load(Test.syntactic_grammar)
            # GrammarAlgorithms.build_first_set(grammar, k)
            # GrammarAlgorithms.build_follow_set(grammar, k)
            # GrammarAlgorithms.build_la_set(grammar, k)
            # decorated_grammar = grammar.decorate()
            # logger.info(decorated_grammar)
            # decorated_pool = grammar.decorate_pool()
            # logger.info(decorated_pool)
            # Test.dump_rules_la(grammar, logger, k)
            cls.grammar = grammar

    @staticmethod
    def get_dot_filepath(filename):
        return rf'd:\tmp\art\{filename}.png'

    @staticmethod
    def get_parser(program):
        dp = StringDataProvider(program)
        data = dp.load()
        content = Content(data, '')
        content.build_line_map()
        statistics = Statistics()
        diagnostics = Diagnostics()
        tokenizer = ArtTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        context = ParseContext()
        parser = ArtParser(context, lexer, Test.grammar, statistics, diagnostics)
        return parser

    def test_expression_1_success(self):
        program = """
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        # tree = parser.parse_expression()
        # ParseTreeDomainHelper.generate_graphviz(tree, Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        assert parser.diagnostics.status

    def test_primary_expression_1_success(self):
        program = """
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        pm_expr = parser.parse_primary_expression()
        ParseTreeDomainHelper.generate_graphviz(pm_expr.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        assert parser.diagnostics.status

    def test_primary_expression_2_success(self):
        programs = ['1', 'false', 'true', 'a', 'e . f . g', 'a [1 ]', 'a [ 1] . b [ 2 ] . c [ 3 ]']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_primary_expression_3_success(self):
        program = """
        A<T>.B<U>.C<A<B<X>>>
        """
        parser = Test.get_parser(program)
        parser.lexical_analyzer.next_lexeme()
        pm_expr = parser.parse_primary_expression()
        ParseTreeDomainHelper.generate_graphviz(pm_expr.tree,
                                                Test.get_dot_filepath(inspect.currentframe().f_code.co_name))
        assert parser.diagnostics.status

    def test_primary_expression_4_success(self):
        programs = ['a.bar()', 'foo ( )', 'foo(1)']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_primary_expression_5_success(self):
        programs = ['Point { }', 'Point{5,6,7}']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_primary_expression_6_success(self):
        programs = ['a [U -- ] ++ ', '1++', 'false--', 'true ++', 'a ++', 'e -- . f ++. g++', 'a [ d ++ ]']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status

    def test_primary_expression_7_success(self):
        programs = ['()', '( 2 )', '( ( 3))', '(( ( 4 )))', '((foo( ) ) )']
        for k, program in enumerate(programs):
            parser = Test.get_parser(program)
            parser.lexical_analyzer.next_lexeme()
            pm_expr = parser.parse_primary_expression()
            ParseTreeDomainHelper.\
                generate_graphviz(pm_expr.tree, Test.get_dot_filepath(f'{inspect.currentframe().f_code.co_name}_{k}'))
            assert parser.diagnostics.status
