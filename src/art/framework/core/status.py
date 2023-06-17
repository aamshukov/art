# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Status """
import datetime
from art.framework.core.base import Base


class Status(Base):
    """
    """
    NO_ERROR = 0
    SYSTEM_SUCCESS_CODE = NO_ERROR
    SYSTEM_ERROR_CODE = -1

    SUCCESS_MASK     = 0x0000_0000_0000_0000  # noqa
    INFO_MASK        = 0x0001_0000_0000_0000  # noqa
    WARNING_MASK     = 0x0010_0000_0000_0000  # noqa
    ERROR_MASK       = 0x0100_0000_0000_0000  # noqa
    FATAL_ERROR_MASK = 0x1000_0000_0000_0000  # noqa

    SUCCESS                 = 1 | SUCCESS_MASK      # noqa
    INFO                    = 2 | INFO_MASK         # noqa
    WARNING                 = 3 | WARNING_MASK      # noqa
    ERROR                   = 0 | ERROR_MASK        # noqa
    FATAL_ERROR             = 0 | FATAL_ERROR_MASK  # noqa
    INVALID_LITERAL         = 128 | ERROR_MASK      # noqa
    STATUS_DEPRECATED       = 129 | WARNING_MASK    # noqa
    INVALID_UNICODE_ESCAPE  = 130 | ERROR_MASK      # noqa

    def __init__(self,
                 text,  # description
                 contributor,
                 custom_code=SUCCESS,
                 system_code=SYSTEM_SUCCESS_CODE,  # specific OS error, like WindowsError.winerror
                 library_code=NO_ERROR,  # specific Python library code
                 correlation_id=0  # must be used in threaded environment
                 ):
        """
        """
        self._text = text
        self._contributor = contributor
        self._custom_code = custom_code
        self._system_code = system_code
        self._library_code = library_code
        self._correlation_id = correlation_id
        self._timestamp = datetime.datetime.now().timestamp()

    @property
    def text(self):
        """
        """
        return self._text

    @property
    def contributor(self):
        """
        """
        return self._contributor

    @property
    def custom_code(self):
        """
        """
        return self._custom_code

    @property
    def system_code(self):
        """
        """
        return self._system_code

    @property
    def library_code(self):
        """
        """
        return self._library_code

    @property
    def correlation_id(self):
        """
        """
        return self._correlation_id

    @property
    def timestamp(self):
        """
        """
        return self._timestamp
