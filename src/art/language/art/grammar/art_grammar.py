# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Art Context Free Grammar """
from art.framework.core.diagnostics import Diagnostics
from art.framework.core.text import Text
from art.framework.frontend.content.content import Content
from art.framework.frontend.grammar.grammar import Grammar
from art.framework.frontend.grammar.grammar_rule import GrammarRule
from art.framework.frontend.grammar.grammar_symbol_factory import GrammarSymbolFactory
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind
from art.framework.frontend.grammar.grammar_tokenizer import GrammarTokenizer
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class ArtGrammar(Grammar):
    """
    Art Context Free Grammar
    """
    def __init__(self, name='', logger=None):
        """
        """
        super().__init__(name, logger)
        self.keywords = TokenKind.get_keywords()

    def load(self, data_provider):
        """
        """
        data = data_provider.load()
        content = Content(data, 'grammar-lexer')
        content.build_line_map()
        diagnostics = Diagnostics()
        statistics = Statistics()
        tokenizer = GrammarTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        lexer.take_snapshot()
        while not lexer.eos():  # populate pool
            token = lexer.next_lexeme()
            match token.kind:
                case TokenKind.IDENTIFIER:
                    self.get_symbol(token.literal)
        lexer.rewind_to_snapshot()
        lhs = None
        rhs = list()
        while not lexer.eos():  # build grammar
            token = lexer.next_lexeme()
            match token.kind:
                case TokenKind.IDENTIFIER:
                    if not lhs:
                        lhs = token.literal
                    else:
                        rhs.append(token.literal)
                case TokenKind.COLON:
                    pass
                case TokenKind.BITWISE_OR:
                    pass
                case TokenKind.SEMICOLON:
                    lhs = None
                    rhs.clear()
                case TokenKind.STRING_KW | TokenKind.STRING:
                    rhs.append(token.literal)
                case TokenKind.SINGLE_LINE_COMMENT:
                    pass
                case TokenKind.EOL:
                    if lhs and rhs:
                        self.assemble_rule(lhs, rhs)
                        rhs.clear()
                case _:
                    pass

    def assemble_rule(self, lhs_name, rhs_names):
        """
        """
        rule = GrammarRule(len(self.rules) + 1, '')
        rule.lhs = self.get_symbol(lhs_name)
        rule.lhs.rules.append(rule)
        for rhs_name in rhs_names:
            rule.rhs.append(self.get_symbol(rhs_name))
        rhs = [s.name for s in rule.rhs]
        rule.name = f"{rule.lhs.name}  ->  {'  '.join(rhs)}"
        self.rules.append(rule)

    def get_symbol(self, name):
        """
        """
        normalized_name = ArtGrammar.normalize_symbol_name(name)
        stype = ArtGrammar.get_symbol_type(name)
        if stype == GrammarSymbolKind.NON_TERMINAL:
            normalized_name = normalized_name.upper()
        if normalized_name in self.pool:
            result = self.pool[normalized_name]
        else:
            result = GrammarSymbolFactory.create(normalized_name,
                                                 stype,
                                                 self.token_from_name(normalized_name))
            self.pool[normalized_name] = result
        return result

    @staticmethod
    def normalize_symbol_name(name):
        """
        """
        name = name.strip()
        if name.startswith("'"):
            name = name[1:-1].strip()
        return name

    @staticmethod
    def get_symbol_type(name):
        """
        """
        name = name.strip()
        if name.startswith("'"):
            result = GrammarSymbolKind.TERMINAL
        elif Text.epsilon(name):
            result = GrammarSymbolKind.EPSILON
        else:
            result = GrammarSymbolKind.NON_TERMINAL
        return result

    def lookup_symbol(self, name):
        """
        """
        normalized_name = ArtGrammar.normalize_symbol_name(name)
        return self.pool[normalized_name]

    def token_from_name(self, name):
        """
        """
        if name in self.keywords:
            return self.keywords[name]
        match name:
            case 'ε':
                return TokenKind.EPSILON
            case 'terminal':
                return TokenKind.TERMINAL
            case 'identifier':
                return TokenKind.IDENTIFIER
            case 'indent':
                return TokenKind.INDENT
            case 'dedent':
                return TokenKind.DEDENT
            case 'integer_number_literal':
                return TokenKind.INTEGER
            case 'real_number_literal':
                return TokenKind.REAL
            case 'boolean_literal':
                return TokenKind.BOOLEAN
            case 'string_literal':
                return TokenKind.STRING
            case '(':
                return TokenKind.LEFT_PARENTHESIS
            case ')':
                return TokenKind.RIGHT_PARENTHESIS
            case '[':
                return TokenKind.LEFT_SQUARE_BRACKET
            case ']':
                return TokenKind.RIGHT_SQUARE_BRACKET
            case '{':
                return TokenKind.LEFT_CURLY_BRACKET
            case '}':
                return TokenKind.RIGHT_CURLY_BRACKET
            case '.':
                return TokenKind.DOT
            case '..':
                return TokenKind.RANGE
            case '...':
                return TokenKind.ELLIPSES
            case ':':
                return TokenKind.COLON
            case '::':
                return TokenKind.COLONS
            case ';':
                return TokenKind.SEMICOLON
            case ',':
                return TokenKind.COMMA
            case '?':
                return TokenKind.QUESTION_MARK
            case '@':
                return TokenKind.COMMERCIAL_AT
            case '`':
                return TokenKind.GRAVE_ACCENT
            case '\\':
                return TokenKind.BACK_SLASH
            case '=':
                return TokenKind.EQUALS_SIGN
            case '==':
                return TokenKind.EQUAL
            case '!=':
                return TokenKind.NOT_EQUAL
            case '!':
                return TokenKind.EXCLAMATION_MARK
            case '<':
                return TokenKind.LESS_THAN_SIGN
            case '<=':
                return TokenKind.LESS_THAN_OR_EQUAL
            case '<<':
                return TokenKind.SHIFT_LEFT
            case '<<=':
                return TokenKind.SHIFT_LEFT_ASSIGNMENT
            case '>':
                return TokenKind.GREATER_THAN_SIGN
            case '>=':
                return TokenKind.GREATER_THAN_OR_EQUAL
            case '>>':
                return TokenKind.SHIFT_RIGHT
            case '>>=':
                return TokenKind.SHIFT_RIGHT_ASSIGNMENT
            case '<=>':
                return TokenKind.SPACESHIP
            case '+':
                return TokenKind.PLUS_SIGN
            case '++':
                return TokenKind.INCREMENT
            case '+=':
                return TokenKind.ADD_ASSIGNMENT
            case '-':
                return TokenKind.HYPHEN_MINUS
            case '--':
                return TokenKind.DECREMENT
            case '-=':
                return TokenKind.SUB_ASSIGNMENT
            case '->':
                return TokenKind.ARROW
            case '=>':
                return TokenKind.DOUBLE_ARROW
            case '*':
                return TokenKind.ASTERISK
            case '*=':
                return TokenKind.MUL_ASSIGNMENT
            case '/':
                return TokenKind.FORWARD_SLASH
            case '/=':
                return TokenKind.DIV_ASSIGNMENT
            case '%':
                return TokenKind.PERCENT_SIGN
            case '%=':
                return TokenKind.MOD_ASSIGNMENT
            case '&':
                return TokenKind.BITWISE_AND
            case '&=':
                return TokenKind.BITWISE_AND_ASSIGNMENT
            case '|':
                return TokenKind.BITWISE_OR
            case '|=':
                return TokenKind.BITWISE_OR_ASSIGNMENT
            case '^':
                return TokenKind.BITWISE_XOR
            case '^=':
                return TokenKind.BITWISE_XOR_ASSIGNMENT
            case '~':
                return TokenKind.BITWISE_NOT
            case '~=':
                return TokenKind.BITWISE_NOT_ASSIGNMENT
            case _:
                return TokenKind.UNKNOWN
