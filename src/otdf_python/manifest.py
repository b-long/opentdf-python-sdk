"""TDF manifest representation and serialization."""

import json
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ManifestSegment:
    """Encrypted segment information in TDF manifest."""

    hash: str
    segmentSize: int
    encryptedSegmentSize: int


@dataclass
class ManifestRootSignature:
    """Root signature for manifest integrity."""

    alg: str
    sig: str


@dataclass
class ManifestIntegrityInformation:
    """Manifest integrity information with signatures and hashes."""

    rootSignature: ManifestRootSignature
    segmentHashAlg: str
    segmentSizeDefault: int
    encryptedSegmentSizeDefault: int
    segments: list[ManifestSegment]


@dataclass
class ManifestPolicyBinding:
    """Policy binding with algorithm and hash."""

    alg: str
    hash: str


@dataclass
class ManifestKeyAccess:
    """Key access information in manifest."""

    type: str
    url: str
    protocol: str
    wrappedKey: str
    policyBinding: Any = None
    encryptedMetadata: str | None = None
    kid: str | None = None
    sid: str | None = None
    schemaVersion: str | None = None
    ephemeralPublicKey: str | None = None


@dataclass
class ManifestMethod:
    """Encryption method information in manifest."""

    algorithm: str
    iv: str
    isStreamable: bool | None = None


@dataclass
class ManifestEncryptionInformation:
    """Encryption information in TDF manifest."""

    type: str
    policy: str
    keyAccess: list[ManifestKeyAccess]
    method: ManifestMethod
    integrityInformation: ManifestIntegrityInformation


@dataclass
class ManifestPayload:
    """Payload information in TDF manifest."""

    type: str
    url: str
    protocol: str
    mimeType: str
    isEncrypted: bool


@dataclass
class ManifestBinding:
    """Assertion binding information."""

    method: str
    signature: str


@dataclass
class ManifestAssertion:
    """TDF assertion in manifest."""

    id: str
    type: str
    scope: str
    appliesTo_state: str
    statement: Any
    binding: ManifestBinding | None = None


@dataclass
class Manifest:
    """TDF manifest with encryption and payload information."""

    schemaVersion: str | None = None
    encryptionInformation: ManifestEncryptionInformation | None = None
    payload: ManifestPayload | None = None
    assertions: list[ManifestAssertion] = field(default_factory=list)

    def _remove_none_values_and_empty_lists(self, obj):
        """Recursively remove None values and empty lists from dictionaries and lists."""
        if isinstance(obj, dict):
            cleaned = {}
            for k, v in obj.items():
                if v is not None:
                    # For 'assertions' field, exclude if it's an empty list
                    if k == "assertions" and isinstance(v, list) and len(v) == 0:
                        continue
                    cleaned[k] = self._remove_none_values_and_empty_lists(v)
            return cleaned
        elif isinstance(obj, list):
            return [
                self._remove_none_values_and_empty_lists(item)
                for item in obj
                if item is not None
            ]
        else:
            return obj

    def to_json(self) -> str:
        # Create manifest dict with fields ordered to match otdfctl expectations
        # Order: encryptionInformation, payload, schemaVersion, assertions
        manifest_dict = {}

        # Add fields in the order expected by otdfctl
        if self.encryptionInformation is not None:
            manifest_dict["encryptionInformation"] = asdict(self.encryptionInformation)

        if self.payload is not None:
            manifest_dict["payload"] = asdict(self.payload)

        if self.schemaVersion is not None:
            manifest_dict["schemaVersion"] = self.schemaVersion

        if self.assertions and len(self.assertions) > 0:
            manifest_dict["assertions"] = [
                asdict(assertion) for assertion in self.assertions
            ]

        cleaned_dict = self._remove_none_values_and_empty_lists(manifest_dict)
        return json.dumps(cleaned_dict, default=str)

    @staticmethod
    def from_json(data: str) -> "Manifest":
        d = json.loads(data)

        # Recursively instantiate nested dataclasses
        def _payload(p):
            return ManifestPayload(**p) if p else None

        def _segment(s):
            return ManifestSegment(**s)

        def _root_sig(rs):
            return ManifestRootSignature(**rs)

        def _integrity(i):
            # Handle both snake_case and camelCase fields
            # TODO: This can probably be simplified to only camelCase
            return ManifestIntegrityInformation(
                rootSignature=_root_sig(
                    i.get("rootSignature", i.get("root_signature"))
                ),
                segmentHashAlg=i.get("segmentHashAlg", i.get("segment_hash_alg")),
                segmentSizeDefault=i.get(
                    "segmentSizeDefault", i.get("segment_size_default")
                ),
                encryptedSegmentSizeDefault=i.get(
                    "encryptedSegmentSizeDefault",
                    i.get("encrypted_segment_size_default"),
                ),
                segments=[_segment(s) for s in i["segments"]],
            )

        def _method(m):
            return ManifestMethod(**m)

        def _key_access(k):
            return ManifestKeyAccess(**k)

        def _enc_info(e):
            # Handle both snake_case and camelCase fields
            # TODO: This can probably be simplified to only camelCase
            return ManifestEncryptionInformation(
                type=e.get("type", e.get("key_access_type", "split")),
                policy=e["policy"],
                keyAccess=[
                    _key_access(k)
                    for k in e.get("keyAccess", e.get("key_access_obj", []))
                ],
                method=_method(e["method"]),
                integrityInformation=_integrity(
                    e.get("integrityInformation", e.get("integrity_information"))
                ),
            )

        def _binding(b):
            return ManifestBinding(**b) if b else None

        def _assertion(a):
            return ManifestAssertion(
                id=a["id"],
                type=a["type"],
                scope=a["scope"],
                appliesTo_state=a.get("appliesTo_state", a.get("applies_to_state")),
                statement=a["statement"],
                binding=_binding(a.get("binding")),
            )

        return Manifest(
            schemaVersion=d.get("schemaVersion", d.get("tdf_version")),
            encryptionInformation=_enc_info(
                d.get("encryptionInformation", d.get("encryption_information"))
            )
            if d.get("encryptionInformation") or d.get("encryption_information")
            else None,
            payload=_payload(d["payload"]) if d.get("payload") else None,
            assertions=[_assertion(a) for a in d.get("assertions", [])],
        )
