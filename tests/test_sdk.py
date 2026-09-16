"""Basic tests for the Python SDK class."""

import io
import json
import zipfile

import pytest
from otdf_python.sdk import SDK


class DummyServices(SDK.Services):
    """Dummy SDK services for testing."""

    def close(self):
        """Close the services."""
        self.closed = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""


def test_sdk_init_and_close():
    """Test SDK initialization and close."""
    services = DummyServices()
    sdk = SDK(services)
    assert sdk.get_services() is services
    assert sdk.get_platform_url() is None
    # Test context manager exit calls close
    with SDK(services):
        pass
    assert services.closed


def test_split_key_exception():
    """Test SDK SplitKeyException."""
    with pytest.raises(SDK.SplitKeyException, match="split key error"):
        raise SDK.SplitKeyException("split key error")


def test_data_size_not_supported():
    """Test SDK DataSizeNotSupported exception."""
    with pytest.raises(SDK.DataSizeNotSupported, match="too large"):
        raise SDK.DataSizeNotSupported("too large")


def test_kas_info_missing():
    """Test SDK KasInfoMissing exception."""
    with pytest.raises(SDK.KasInfoMissing, match="kas info missing"):
        raise SDK.KasInfoMissing("kas info missing")


def test_kas_public_key_missing():
    """Test SDK KasPublicKeyMissing exception."""
    with pytest.raises(SDK.KasPublicKeyMissing, match="kas pubkey missing"):
        raise SDK.KasPublicKeyMissing("kas pubkey missing")


def test_tamper_exception():
    """Test SDK TamperException prefixes message with [tamper detected]."""
    with pytest.raises(SDK.TamperException, match=r"\[tamper detected\] tamper"):
        raise SDK.TamperException("tamper")


def test_root_signature_validation_exception():
    """Test SDK RootSignatureValidationException includes tamper prefix."""
    with pytest.raises(
        SDK.RootSignatureValidationException, match=r"\[tamper detected\] root sig"
    ):
        raise SDK.RootSignatureValidationException("root sig")


def test_segment_signature_mismatch():
    """Test SDK SegmentSignatureMismatch includes tamper prefix."""
    with pytest.raises(
        SDK.SegmentSignatureMismatch, match=r"\[tamper detected\] seg sig"
    ):
        raise SDK.SegmentSignatureMismatch("seg sig")


def test_kas_bad_request_exception():
    """Test SDK KasBadRequestException."""
    with pytest.raises(SDK.KasBadRequestException, match="kas bad req"):
        raise SDK.KasBadRequestException("kas bad req")


def test_kas_allowlist_exception_custom_message():
    """Test SDK KasAllowlistException with explicit message."""
    with pytest.raises(SDK.KasAllowlistException, match="kas allowlist"):
        raise SDK.KasAllowlistException(
            "http://kas.example.com", message="kas allowlist"
        )


def test_kas_allowlist_exception_auto_message():
    """Test SDK KasAllowlistException auto-generates message from url and origins."""
    exc = SDK.KasAllowlistException(
        "http://kas.example.com", allowed_origins={"http://allowed.com"}
    )
    assert exc.url == "http://kas.example.com"
    assert "http://kas.example.com" in str(exc)
    assert "http://allowed.com" in str(exc)


def test_assertion_exception():
    """Test SDK AssertionException stores assertion_id."""
    exc = SDK.AssertionException("assertion failed", "id123")
    assert str(exc) == "assertion failed"
    assert exc.assertion_id == "id123"

    with pytest.raises(SDK.AssertionException, match="assertion failed"):
        raise SDK.AssertionException("assertion failed", "id123")


def _zip_with(entries: dict[str, bytes]) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        for name, content in entries.items():
            z.writestr(name, content)
    return buf.getvalue()


def test_is_tdf_accepts_spec_layout():
    manifest = json.dumps({"payload": {"url": "0.payload"}}).encode()
    assert SDK.is_tdf(_zip_with({"manifest.json": manifest, "0.payload": b"x"}))


def test_is_tdf_accepts_legacy_layout():
    manifest = json.dumps({"payload": {"url": "0.payload"}}).encode()
    assert SDK.is_tdf(_zip_with({"0.manifest.json": manifest, "0.payload": b"x"}))


def test_is_tdf_accepts_extra_entries_and_custom_payload_name():
    manifest = json.dumps({"payload": {"url": "blob"}}).encode()
    assert SDK.is_tdf(
        _zip_with({"manifest.json": manifest, "blob": b"x", "extra.txt": b"y"})
    )


def test_is_tdf_rejects_missing_payload_entry():
    manifest = json.dumps({"payload": {"url": "blob"}}).encode()
    assert not SDK.is_tdf(_zip_with({"manifest.json": manifest, "0.payload": b"x"}))
