from dataclasses import dataclass


@dataclass
class AuthHeaders:
    """
    Represents authentication headers used in token-based authorization.
    This class holds authorization and DPoP (Demonstrating Proof of Possession) headers
    that are used in token-based API requests.
    """

    auth_header: str
    dpop_header: str

    def get_auth_header(self) -> str:
        """Returns the authorization header."""
        return self.auth_header

    def get_dpop_header(self) -> str:
        """Returns the DPoP header."""
        return self.dpop_header
