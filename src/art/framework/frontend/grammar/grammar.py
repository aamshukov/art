# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Context Free Grammar """
import os
from functools import lru_cache
from art.framework.core.base import Base
from art.framework.core.diagnostics import Diagnostics
from art.framework.core.text import Text
from art.framework.frontend.content.content import Content
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.grammar.grammar_rule import GrammarRule
from art.framework.frontend.grammar.grammar_symbol import GrammarSymbol
from art.framework.frontend.grammar.grammar_symbol_factory import GrammarSymbolFactory
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind
from art.framework.frontend.grammar.grammar_tokenizer import GrammarTokenizer
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.lexical_analyzer.tokenizer.token_kind import TokenKind


class Grammar(Base):
    """
    Context Free Grammar
    """
    def __init__(self, name='', logger=None):
        """
        """
        super().__init__()
        self.name = name
        self.logger = logger
        self.rules = list()
        self.pool = dict()  # name:symbol mapping
        self.pool['ε'] = GrammarSymbolFactory.epsilon_symbol()
        self.pool['λ'] = GrammarSymbolFactory.epsilon_symbol()
        self.pool[GrammarSymbolFactory.UNKNOWN_SYMBOL.name] = GrammarSymbolFactory.unknown_symbol()

    @property
    @lru_cache
    def start(self):
        """
        Return start symbol of the grammar.
        """
        assert self.rules, 'Rules must not be empty.'
        return self.rules[0].lhs

    @property
    def epsilon(self):
        """
        """
        return self.pool['ε']

    def load_file(self, filepath):
        """
        """
        with open(os.path.abspath(filepath), 'r') as stream:
            content = stream.read()
            return self.load(content)

    def load(self, content):
        """
        """
        dp = StringDataProvider(content)
        data = dp.load()
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
                    if lhs:
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
        normalized_name = Grammar.normalize_symbol_name(name)
        stype = Grammar.get_symbol_type(name)
        if stype == GrammarSymbolKind.NON_TERMINAL:
            normalized_name = normalized_name.upper()
        if normalized_name in self.pool:
            result = self.pool[normalized_name]
        else:
            result = GrammarSymbolFactory.create(normalized_name, stype)
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
        normalized_name = Grammar.normalize_symbol_name(name)
        return self.pool[normalized_name]

    def decorate(self):
        """
        """
        result = ""
        lhs = GrammarSymbol(0, '')
        for rule in self.rules:
            if lhs != rule.lhs:
                lhs = rule.lhs
                result += '\n'
            result += f'{rule.decorate()}\n'
        return result

    def decorate_pool(self):
        """
        """
        result = ""
        for symbol in self.pool.values():
            result = f'{result}{symbol.decorate(full=True)}\n'
        return result
