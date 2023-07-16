#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Token factory """
from copy import deepcopy

from art.framework.core.base import Base
from art.framework.frontend.token.token import Token
from art.framework.frontend.token.token_kind import TokenKind


class TokenFactory(Base):
    """
    """
    UNKNOWN_TOKEN = Token(TokenKind.UNKNOWN)

    def __init__(self):
        """
        """
        super().__init__()

    @staticmethod
    def create(kind, source='', version='1.0'):
        """
        """
        return Token(kind=kind,
                     source=source,
                     version=version)

    @staticmethod
    def unknown_token():
        """
        """
        return deepcopy(TokenFactory.UNKNOWN_TOKEN)
