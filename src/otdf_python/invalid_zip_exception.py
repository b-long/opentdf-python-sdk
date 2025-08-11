class InvalidZipException(Exception):
    """
    Raised when a ZIP file is invalid or corrupted.
    Based on Java implementation.
    """

    def __init__(self, message: str):
        super().__init__(message)
