from dataclasses import dataclass, field, asdict
from typing import Any
import json

@dataclass
class ManifestSegment:
    hash: str
    segment_size: int
    encrypted_segment_size: int

@dataclass
class ManifestRootSignature:
    algorithm: str
    signature: str

@dataclass
class ManifestIntegrityInformation:
    root_signature: ManifestRootSignature
    segment_hash_alg: str
    segment_size_default: int
    encrypted_segment_size_default: int
    segments: list[ManifestSegment]

@dataclass
class ManifestPolicyBinding:
    alg: str
    hash: str

@dataclass
class ManifestKeyAccess:
    key_type: str
    url: str
    protocol: str
    wrapped_key: str
    policy_binding: Any
    encrypted_metadata: str | None = None
    kid: str | None = None
    sid: str | None = None
    schema_version: str | None = None
    ephemeral_public_key: str | None = None

@dataclass
class ManifestMethod:
    algorithm: str
    iv: str
    is_streamable: bool | None = None

@dataclass
class ManifestEncryptionInformation:
    key_access_type: str
    policy: str
    key_access_obj: list[ManifestKeyAccess]
    method: ManifestMethod
    integrity_information: ManifestIntegrityInformation

@dataclass
class ManifestPayload:
    type: str
    url: str
    protocol: str
    mime_type: str
    is_encrypted: bool

@dataclass
class ManifestBinding:
    method: str
    signature: str

@dataclass
class ManifestAssertion:
    id: str
    type: str
    scope: str
    applies_to_state: str
    statement: Any
    binding: ManifestBinding | None = None

@dataclass
class Manifest:
    tdf_version: str | None = None
    encryption_information: ManifestEncryptionInformation | None = None
    payload: ManifestPayload | None = None
    assertions: list[ManifestAssertion] = field(default_factory=list)

    def to_json(self) -> str:
        return json.dumps(asdict(self), default=str)

    @staticmethod
    def from_json(data: str) -> 'Manifest':
        d = json.loads(data)
        # Recursively instantiate nested dataclasses
        def _payload(p):
            return ManifestPayload(**p) if p else None
        def _segment(s):
            return ManifestSegment(**s)
        def _root_sig(rs):
            return ManifestRootSignature(**rs)
        def _integrity(i):
            return ManifestIntegrityInformation(
                root_signature=_root_sig(i['root_signature']),
                segment_hash_alg=i['segment_hash_alg'],
                segment_size_default=i['segment_size_default'],
                encrypted_segment_size_default=i['encrypted_segment_size_default'],
                segments=[_segment(s) for s in i['segments']],
            )
        def _method(m):
            return ManifestMethod(**m)
        def _key_access(k):
            return ManifestKeyAccess(**k)
        def _enc_info(e):
            return ManifestEncryptionInformation(
                key_access_type=e['key_access_type'],
                policy=e['policy'],
                key_access_obj=[_key_access(k) for k in e['key_access_obj']],
                method=_method(e['method']),
                integrity_information=_integrity(e['integrity_information']),
            )
        def _binding(b):
            return ManifestBinding(**b) if b else None
        def _assertion(a):
            return ManifestAssertion(
                id=a['id'],
                type=a['type'],
                scope=a['scope'],
                applies_to_state=a['applies_to_state'],
                statement=a['statement'],
                binding=_binding(a.get('binding')),
            )
        return Manifest(
            tdf_version=d.get('tdf_version'),
            encryption_information=_enc_info(d['encryption_information']) if d.get('encryption_information') else None,
            payload=_payload(d['payload']) if d.get('payload') else None,
            assertions=[_assertion(a) for a in d.get('assertions', [])],
        )
