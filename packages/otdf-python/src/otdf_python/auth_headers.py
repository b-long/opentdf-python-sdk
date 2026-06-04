"""Authentication header management."""

from dataclasses import dataclass


@dataclass
class AuthHeaders:
    """Represents authentication headers used in token-based authorization.
    This class holds authorization and DPoP (Demonstrating Proof of Possession) headers
    that are used in token-based API requests.
    """

    auth_header: str
    dpop_header: str = ""

    def get_auth_header(self) -> str:
        """Get the authorization header."""
        return self.auth_header

    def get_dpop_header(self) -> str:
        """Get the DPoP header."""
        return self.dpop_header

    def to_dict(self) -> dict[str, str]:
        """Convert authentication headers to a dictionary for use with HTTP clients.

        Returns:
            Dictionary with 'Authorization' header and optionally 'DPoP' header

        """
        headers = {"Authorization": self.auth_header}
        if self.dpop_header:
            headers["DPoP"] = self.dpop_header
        return headers
