# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Status """
from art.framework.core.diagnostics.code import Code
from art.framework.core.diagnostics.system_code import SystemCode
from art.framework.core.domain.base import Base
from art.framework.core.utils.time import Time


class Status(Base):
    """
    """
    def __init__(self,
                 messages=None,
                 details=None,
                 contributor=None,
                 custom_code=Code.Success,         # application specific code
                 system_code=SystemCode.NoError,   # specific OS error, like WindowsError.ERROR
                 library_code=SystemCode.NoError,  # specific Python library code
                 correlation_id=0,  # must be used in threaded environment
                 timestamp=None):
        """
        """
        super().__init__()
        self.messages = messages
        self.details = details
        self.contributor = contributor
        self.custom_code = custom_code
        self.system_code = system_code
        self.library_code = library_code
        self.correlation_id = correlation_id
        self.timestamp = Time.timestamp() if timestamp is None else timestamp
