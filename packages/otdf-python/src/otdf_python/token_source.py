"""TokenSource: Handles OAuth2 token acquisition and caching."""

import time

import httpx


class TokenSource:
    """OAuth2 token source for authentication."""

    def __init__(self, token_url, client_id, client_secret):
        """Initialize token source."""
        self.token_url = token_url
        self.client_id = client_id
        self.client_secret = client_secret
        self._token = None
        self._expires_at = 0

    def __call__(self):
        now = time.time()
        if self._token and now < self._expires_at - 60:
            return self._token
        resp = httpx.post(
            self.token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": self.client_id,
                "client_secret": self.client_secret,
            },
        )
        resp.raise_for_status()
        data = resp.json()
        self._token = data["access_token"]
        self._expires_at = now + data.get("expires_in", 3600)
        return self._token
