class SDKException(Exception):
    def __init__(self, message, reason=None):
        super().__init__(message)
        self.reason = reason


class AutoConfigureException(SDKException):
    def __init__(self, message, cause=None):
        super().__init__(message, cause)


class KASBadRequestException(SDKException):
    """Thrown when the KAS returns a bad request response or other client request errors."""

    def __init__(self, message):
        super().__init__(message)
