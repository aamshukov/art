#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
import unittest
from art.framework.core.text import Text
from art.framework.frontend.data_provider.string_data_provider import StringDataProvider
from art.framework.frontend.content.content import Content
from art.framework.frontend.lexical_analyzer.lexical_analyzer import LexicalAnalyzer


class Test(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(Test, self).__init__(*args, **kwargs)

    def test_lexical_analyzer_success(self):
        dp = StringDataProvider('A')
        data = dp.load()
        assert len(data) == 1
        content = Content(0, data, '')
        assert len(data) == content.count
        assert Text.equal(data, content.data)
        lexer = LexicalAnalyzer(0, content)
        assert Text.equal(content.data, lexer.content.data)
        assert content == lexer.content


if __name__ == '__main__':
    """
    """
    unittest.main()
