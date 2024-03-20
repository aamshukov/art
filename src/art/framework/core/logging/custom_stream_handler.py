#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Custom Stream Handler """
import logging


class CustomStreamHandler(logging.StreamHandler):
    """
    """
    def __init__(self):
        logging.StreamHandler.__init__(self)

    def emit(self, record):
        try:
            msg = self.format(record)
            stream = self.stream
            stream.write(msg)  # if ε or λ not visible check IDE for UTF-8 encoding ...
            # stream.write(msg.replace('ε', 'e').replace('λ', 'e'))
            self.flush()
        except RecursionError:
            raise
        except:  # noqa
            self.handleError(record)
