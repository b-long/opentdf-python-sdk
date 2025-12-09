"""Basic tests for the Python SDK class."""

from otdf_python.sdk import SDK


class DummyServices(SDK.Services):
    """Dummy SDK services for testing."""

    def close(self):
        """Close the services."""
        self.closed = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context manager."""
        pass


def test_sdk_init_and_close():
    """Test SDK initialization and close."""
    services = DummyServices()
    sdk = SDK(services)
    assert sdk.get_services() is services
    assert sdk.get_platform_url() is None
    # Test context manager exit calls close
    with SDK(services):
        pass
    # Optionally, check if close was called if you want


def test_split_key_exception():
    """Test SDK SplitKeyException."""
    try:
        raise SDK.SplitKeyException("split key error")
    except SDK.SplitKeyException:
        pass


def test_data_size_not_supported():
    """Test SDK DataSizeNotSupported exception."""
    try:
        raise SDK.DataSizeNotSupported("too large")
    except SDK.DataSizeNotSupported:
        pass


def test_kas_info_missing():
    """Test SDK KasInfoMissing exception."""
    try:
        raise SDK.KasInfoMissing("kas info missing")
    except SDK.KasInfoMissing:
        pass


def test_kas_public_key_missing():
    """Test SDK KasPublicKeyMissing exception."""
    try:
        raise SDK.KasPublicKeyMissing("kas pubkey missing")
    except SDK.KasPublicKeyMissing:
        pass


def test_tamper_exception():
    """Test SDK TamperException."""
    try:
        raise SDK.TamperException("tamper")
    except SDK.TamperException:
        pass


def test_root_signature_validation_exception():
    """Test SDK RootSignatureValidationException."""
    try:
        raise SDK.RootSignatureValidationException("root sig")
    except SDK.RootSignatureValidationException:
        pass


def test_segment_signature_mismatch():
    """Test SDK SegmentSignatureMismatch exception."""
    try:
        raise SDK.SegmentSignatureMismatch("seg sig")
    except SDK.SegmentSignatureMismatch:
        pass


def test_kas_bad_request_exception():
    """Test SDK KasBadRequestException."""
    try:
        raise SDK.KasBadRequestException("kas bad req")
    except SDK.KasBadRequestException:
        pass


def test_kas_allowlist_exception():
    """Test SDK KasAllowlistException."""
    try:
        raise SDK.KasAllowlistException("kas allowlist")
    except SDK.KasAllowlistException:
        pass


def test_assertion_exception():
    """Test SDK AssertionException."""
    try:
        raise SDK.AssertionException("assertion", "id123")
    except SDK.AssertionException:
        pass
