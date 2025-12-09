"""Unit tests for TokenSource."""

import time
from unittest.mock import MagicMock, patch

from otdf_python.token_source import TokenSource


def test_token_source_returns_token_and_caches():
    """Test TokenSource returns token and caches it."""
    with patch("httpx.post") as mock_post:
        mock_resp = MagicMock()
        mock_resp.json.return_value = {"access_token": "abc", "expires_in": 100}
        mock_resp.raise_for_status.return_value = None
        mock_post.return_value = mock_resp

        ts = TokenSource("http://token", "id", "secret")
        token1 = ts()
        assert token1 == "abc"
        # Should use cache
        token2 = ts()
        assert token2 == "abc"
        assert mock_post.call_count == 1


@patch("httpx.post")
def test_token_source_refreshes_token(mock_post):
    """Test TokenSource refreshes expired token."""
    mock_resp1 = MagicMock()
    mock_resp1.json.return_value = {"access_token": "abc", "expires_in": 1}
    mock_resp1.raise_for_status.return_value = None
    mock_resp2 = MagicMock()
    mock_resp2.json.return_value = {"access_token": "def", "expires_in": 100}
    mock_resp2.raise_for_status.return_value = None
    mock_post.side_effect = [mock_resp1, mock_resp2]

    ts = TokenSource("http://token", "id", "secret")
    token1 = ts()
    time.sleep(2)
    token2 = ts()
    assert token1 == "abc"
    assert token2 == "def"
