#! /usr/bin/env python3
# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Configuration """
from art.framework.core.domain.base import Base
from art.framework.core.patterns.singleton.singleton import singleton


class Configurator(Base):
    """
    """
    def __init__(self):
        """
        """
        super().__init__()


# from yaml import load_all
# try:
#     from yaml import CLoader as Loader
# except ImportError:
#     from yaml import Loader
#
# import logging
# from domain_helper import strings_equal
# from singleton import singleton
#
#
@singleton
class Configurator:
    """
    Configuration manager
    """
#     def __init__(self):
#         self._db_host = 'localhost'
#         self._db_port = 33054
#         self._db_name = 'ffmpeg'
#         self._db_table = 'appcommand'
#         self._db_user = None
#         self._db_password = ''
#         self._db_config = None
#         self._log_level = logging.INFO
#         self._log_dir = None
#
#     @property
#     def db_host(self):
#         return self._db_host
#
#     @db_host.setter
#     def db_host(self, value):
#         self._db_host = value
#
#     @property
#     def db_port(self):
#         return self._db_port
#
#     @db_port.setter
#     def db_port(self, value):
#         self._db_port = value
#
#     @property
#     def db_name(self):
#         return self._db_name
#
#     @db_name.setter
#     def db_name(self, value):
#         self._db_name = value
#
#     @property
#     def db_table(self):
#         return self._db_table
#
#     @db_table.setter
#     def db_table(self, value):
#         self._db_table = value
#
#     @property
#     def db_user(self):
#         return self._db_user
#
#     @db_user.setter
#     def db_user(self, value):
#         self._db_user = value
#
#     @property
#     def db_password(self):
#         return self._db_password
#
#     @db_password.setter
#     def db_password(self, value):
#         self._db_password = value
#
#     @property
#     def db_config(self):
#         return self._db_config
#
#     @db_config.setter
#     def db_config(self, value):
#         self._db_config = value
#
#     @property
#     def log_level(self):
#         return self._log_level
#
#     @log_level.setter
#     def log_level(self, value):
#         self._log_level = value
#
#     @property
#     def log_dir(self):
#         return self._log_dir
#
#     @log_dir.setter
#     def log_dir(self, value):
#         self._log_dir = value
#
#
# def read_configuration(db_config):
#     """
#     :param db_config:
#     :return:
#     """
#     db_host = None
#     db_port = None
#     db_name = None
#     db_table = None
#     db_user = None
#     db_password = None
#
#     log_level = None
#     log_dir = None
#
#     with open(db_config, "r") as stream:
#         docs = load_all(stream)
#         for doc in docs:
#             if 'parameters' in doc:
#                 for _, content in doc.items():
#                     for k, v in content.items():
#                         if strings_equal(k, 'database_host') and v is not None:
#                             db_host = v
#                         elif strings_equal(k, 'database_port') and v is not None:
#                             db_port = int(v)
#                         if strings_equal(k, 'database_name') and v is not None:
#                             db_name = v
#                         if strings_equal(k, 'database_table') and v is not None:
#                             db_table = v
#                         elif strings_equal(k, 'database_user') and v is not None:
#                             db_user = v
#                         elif strings_equal(k, 'database_password') and v is not None:
#                             db_password = v
#                         elif strings_equal(k, 'log_level') and v is not None:
#                             log_level = v
#                         elif strings_equal(k, 'log_dir') and v is not None:
#                             log_dir = v
#
#     return db_host, db_port, db_name, db_table, db_user, db_password, log_level, log_dir
#
#
# def initialize_configurator(db_host, db_port, db_name, db_table, db_user, db_password, db_config, log_level, log_dir):
#     db_host_cfg, db_port_cfg, db_name_cfg, db_table_cfg, db_user_cfg, db_password_cfg, log_level_cfg, log_dir_cfg =\
#         read_configuration(db_config)
#
#     def select(items):
#         try:
#             return next(item for item in items if item is not None and item)
#         except StopIteration:
#             return None
#
#     Configurator().db_host = select([db_host, db_host_cfg, Configurator().db_host])
#     Configurator().db_port = select([db_port, db_port_cfg, Configurator().db_port])
#     Configurator().db_name = select([db_name, db_name_cfg, Configurator().db_name])
#     Configurator().db_table = select([db_table, db_table_cfg, Configurator().db_table])
#     Configurator().db_user = select([db_user, db_user_cfg, Configurator().db_user])
#     Configurator().db_password = select([db_password, db_password_cfg, Configurator().db_password]) or ''
#     Configurator().log_level = select([log_level, log_level_cfg, Configurator().log_level]) or logging.INFO
#     Configurator().log_dir = select([log_dir, log_dir_cfg, Configurator().log_dir])
#     Configurator().db_config = db_config
#     if not Configurator().db_host:
#         raise ValueError('Host must be specified.')
#     if not Configurator().db_name:
#         raise ValueError('Database name must be specified.')
#     if not Configurator().db_table:
#         raise ValueError('Table name must be specified.')
#     if not Configurator().db_user:
#         raise ValueError('User must be specified.')
#     if not Configurator().log_dir:
#         raise ValueError('Log dir must be specified.')
