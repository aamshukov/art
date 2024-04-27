#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" System status code values """
from enum import Flag


class SystemCode(Flag):
    NoError = 0
    SystemSuccessCode = NoError
    SystemErrorCode = -1
