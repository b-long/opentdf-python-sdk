"""Mock SDK components for testing."""

from otdf_python.sdk import KAS, SDK


class MockKAS(KAS):
    """Mock KAS implementation for testing."""

    def get_public_key(self, kas_info):
        """Return mock public key."""
        return "mock-public-key"

    def get_ec_public_key(self, kas_info, curve):
        """Return mock EC public key."""
        return "mock-ec-public-key"

    def unwrap(self, key_access, policy, session_key_type):
        """Return mock unwrapped key."""
        return b"mock-unwrapped-key"

    def unwrap_nanotdf(self, curve, header, kas_url):
        """Return mock unwrapped NanoTDF key."""
        return b"mock-unwrapped-nanotdf"

    def get_key_cache(self):
        """Return mock key cache."""
        return None


class MockServices(SDK.Services):
    """Mock SDK services for testing."""

    def kas(self):
        """Return mock KAS instance."""
        return MockKAS()


def test_sdk_instantiation():
    """Test SDK instantiation with mock services."""
    services = MockServices()
    sdk = SDK(services=services)
    assert sdk.get_services() is services
    assert sdk.get_services().kas().get_public_key(None) == "mock-public-key"
    assert sdk.get_services().kas().unwrap(None, "", None) == b"mock-unwrapped-key"
