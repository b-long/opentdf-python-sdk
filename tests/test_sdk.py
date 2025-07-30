"""
Basic tests for the Python SDK class port.
"""

from otdf_python.sdk import SDK


class DummyServices(SDK.Services):
    def close(self):
        self.closed = True

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def test_sdk_init_and_close():
    services = DummyServices()
    sdk = SDK(services)
    assert sdk.get_services() is services
    assert sdk.get_trust_manager() is None
    assert sdk.get_auth_interceptor() is None
    assert sdk.get_platform_services_client() is None
    assert sdk.get_platform_url() is None
    # Test context manager exit calls close
    with SDK(services):
        pass
    # Optionally, check if close was called if you want


def test_split_key_exception():
    try:
        raise SDK.SplitKeyException("split key error")
    except SDK.SplitKeyException:
        pass


def test_data_size_not_supported():
    try:
        raise SDK.DataSizeNotSupported("too large")
    except SDK.DataSizeNotSupported:
        pass


def test_kas_info_missing():
    try:
        raise SDK.KasInfoMissing("kas info missing")
    except SDK.KasInfoMissing:
        pass


def test_kas_public_key_missing():
    try:
        raise SDK.KasPublicKeyMissing("kas pubkey missing")
    except SDK.KasPublicKeyMissing:
        pass


def test_tamper_exception():
    try:
        raise SDK.TamperException("tamper")
    except SDK.TamperException:
        pass


def test_root_signature_validation_exception():
    try:
        raise SDK.RootSignatureValidationException("root sig")
    except SDK.RootSignatureValidationException:
        pass


def test_segment_signature_mismatch():
    try:
        raise SDK.SegmentSignatureMismatch("seg sig")
    except SDK.SegmentSignatureMismatch:
        pass


def test_kas_bad_request_exception():
    try:
        raise SDK.KasBadRequestException("kas bad req")
    except SDK.KasBadRequestException:
        pass


def test_kas_allowlist_exception():
    try:
        raise SDK.KasAllowlistException("kas allowlist")
    except SDK.KasAllowlistException:
        pass


def test_assertion_exception():
    try:
        raise SDK.AssertionException("assertion", "id123")
    except SDK.AssertionException:
        pass
