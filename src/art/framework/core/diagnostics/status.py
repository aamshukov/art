# -*- encoding: utf-8 -*-
# UI Lab Inc. Arthur Amshukov
#
""" Status """
from art.framework.core.domain.base import Base
from art.framework.core.utils.time import Time


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
    INVALID_INT_LITERAL     = 129 | ERROR_MASK      # noqa
    INVALID_REAL_LITERAL    = 130 | ERROR_MASK      # noqa
    STATUS_DEPRECATED       = 131 | WARNING_MASK    # noqa
    INVALID_UNICODE_ESCAPE  = 132 | ERROR_MASK      # noqa
    INVALID_ESCAPE          = 133 | ERROR_MASK      # noqa
    INVALID_CHARACTER       = 134 | ERROR_MASK      # noqa
    INVALID_STRING_LITERAL  = 135 | ERROR_MASK      # noqa
    INVALID_TOKEN           = 136 | ERROR_MASK      # noqa
    INVALID_CLOSING_PAREN   = 137 | ERROR_MASK      # noqa
    INVALID_ARRAY_ELEMENTS  = 138 | ERROR_MASK      # noqa
    UNEXPEXTED_EOS          = 139 | ERROR_MASK      # noqa

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
        super().__init__()
        self.text = text
        self.contributor = contributor
        self.custom_code = custom_code
        self.system_code = system_code
        self.library_code = library_code
        self.correlation_id = correlation_id
        self.timestamp = Time.timestamp()
