#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Lempel Ziv Welch (LZW) compression model """
from art.framework.core.compression.model import Model


class LzwModel(Model):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()
        self.codes = dict()  # string:int
