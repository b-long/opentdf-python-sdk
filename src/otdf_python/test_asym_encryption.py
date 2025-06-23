from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from otdf_python.asym_encryption import AsymEncryption
from otdf_python.asym_decryption import AsymDecryption

def generate_rsa_keypair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    ).decode()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    return private_key, public_key, private_pem, public_pem

def test_asym_encryption_decryption():
    private_key, public_key, private_pem, public_pem = generate_rsa_keypair()
    encryptor = AsymEncryption(public_key_pem=public_pem)
    decryptor = AsymDecryption(private_key_pem=private_pem)
    message = b"test message for encryption"
    encrypted = encryptor.encrypt(message)
    decrypted = decryptor.decrypt(encrypted)
    assert decrypted == message
