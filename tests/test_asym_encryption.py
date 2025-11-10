from otdf_python.asym_crypto import AsymDecryption, AsymEncryption
from tests.mock_crypto import generate_rsa_keypair


def test_asym_encryption_decryption():
    private_pem, public_pem = generate_rsa_keypair()
    encryptor = AsymEncryption(public_key_pem=public_pem)
    decryptor = AsymDecryption(private_key_pem=private_pem)
    message = b"test message for encryption"
    encrypted = encryptor.encrypt(message)
    decrypted = decryptor.decrypt(encrypted)
    assert decrypted == message
