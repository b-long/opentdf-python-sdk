"""SDK-specific exception classes."""


class SDKException(Exception):
    """Base SDK exception class."""

    def __init__(self, message, reason=None):
        """Initialize exception."""
        super().__init__(message)
        self.reason = reason


class AutoConfigureException(SDKException):
    """Exception for SDK auto-configuration failures."""

    def __init__(self, message, cause=None):
        """Initialize exception."""
        super().__init__(message, cause)


class KASBadRequestException(SDKException):
    """Exception for KAS bad request or client errors."""

    def __init__(self, message):
        """Initialize exception."""
        super().__init__(message)
