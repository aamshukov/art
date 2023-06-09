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
from art.framework.frontend.grammar.grammar_symbol_kind import GrammarSymbolKind
from art.framework.frontend.grammar.grammar_tokenizer import GrammarTokenizer
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from art.framework.frontend.statistics.statistics import Statistics
from art.framework.frontend.token.token_kind import TokenKind


class Grammar(Base):
    """
    Context Free Grammar
    """
    def __init__(self, name='', logger=None):
        """
        """
        super().__init__()
        self._name = name
        self._logger = logger
        self._rules = list()
        self._pool = dict()  # name:symbol mapping
        self._pool['ε'] = GrammarSymbol(0, 'ε', GrammarSymbolKind.EPSILON)
        self._pool['λ'] = self._pool['ε']

    @property
    def name(self):
        """
        """
        return self._name

    @property
    @lru_cache
    def start(self):
        """
        Return start symbol of the grammar.
        """
        assert self._rules, 'Rules must not be empty.'
        return self._rules[0].lhs

    @property
    def rules(self):
        """
        """
        return self._rules

    @property
    def pool(self):
        """
        """
        return self._pool

    @property
    def epsilon(self):
        """
        """
        return self._pool['ε']

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
        content = Content(0, data, 'grammar-lexer')
        content.build_line_map()
        diagnostics = Diagnostics()
        statistics = Statistics()
        tokenizer = GrammarTokenizer(0, content, statistics, diagnostics)
        lexer = LexicalAnalyzer(0, tokenizer, statistics, diagnostics)
        lhs = None
        rhs = list()
        while not lexer.eos():
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
                case TokenKind.STRING:
                    rhs.append(token.literal)
                case TokenKind.SINGLE_LINE_COMMENT:
                    pass
                case TokenKind.EOL:
                    if lhs:
                        self.assemble_rule(lhs, rhs)
                        rhs.clear()
                case _:
                    pass

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

    def get_symbol(self, name):
        """
        """
        normalized_name = Grammar.normalize_symbol_name(name)
        if normalized_name in self._pool:
            result = self._pool[normalized_name]
        else:
            stype = Grammar.get_symbol_type(name)
            result = GrammarSymbol(len(self._pool) + 1, normalized_name, stype)
            if stype == GrammarSymbolKind.NON_TERMINAL:
                normalized_name = normalized_name.upper()
            self._pool[normalized_name] = result
        return result

    def get_non_terminal(self, name):
        """
        """
        result = None
        normalized_name = Grammar.normalize_symbol_name(name)
        if normalized_name in self._pool:
            result = self._pool[normalized_name]
            if result.terminal:
                result = None
        return result

    def assemble_rule(self, lhs_name, rhs_names):
        """
       """
        rule = GrammarRule(len(self._rules) + 1, '')
        rule.lhs = self.get_symbol(lhs_name)
        rule.lhs.rules.append(rule)
        for rhs_name in rhs_names:
            rule.rhs.append(self.get_symbol(rhs_name))
        rhs = [s.name for s in rule.rhs]
        rule.name = f"{rule.lhs.name}  ->  {'  '.join(rhs)}"
        self._rules.append(rule)

    def decorate(self):
        """
        """
        result = ""
        lhs = GrammarSymbol(0, '')
        for rule in self._rules:
            if lhs != rule.lhs:
                lhs = rule.lhs
                result += '\n'
            result += f'{rule.decorate()}\n'
        return result
