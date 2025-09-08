from otdf_python.sdk import (
    KAS,
    SDK,
    AttributesServiceClientInterface,
    AuthorizationServiceClientInterface,
    KeyAccessServerRegistryServiceClientInterface,
    NamespaceServiceClientInterface,
    ResourceMappingServiceClientInterface,
    SubjectMappingServiceClientInterface,
)


class MockKAS(KAS):
    def get_public_key(self, kas_info):
        return "mock-public-key"

    def get_ec_public_key(self, kas_info, curve):
        return "mock-ec-public-key"

    def unwrap(self, key_access, policy, session_key_type):
        return b"mock-unwrapped-key"

    def unwrap_nanotdf(self, curve, header, kas_url):
        return b"mock-unwrapped-nanotdf"

    def get_key_cache(self):
        return None


class MockServices(SDK.Services):
    def attributes(self):
        return AttributesServiceClientInterface()

    def namespaces(self):
        return NamespaceServiceClientInterface()

    def subject_mappings(self):
        return SubjectMappingServiceClientInterface()

    def resource_mappings(self):
        return ResourceMappingServiceClientInterface()

    def authorization(self):
        return AuthorizationServiceClientInterface()

    def kas_registry(self):
        return KeyAccessServerRegistryServiceClientInterface()

    def kas(self):
        return MockKAS()


def test_sdk_instantiation():
    services = MockServices()
    sdk = SDK(services=services)
    assert sdk.get_services() is services
    assert sdk.get_services().kas().get_public_key(None) == "mock-public-key"
    assert sdk.get_services().kas().unwrap(None, "", None) == b"mock-unwrapped-key"
