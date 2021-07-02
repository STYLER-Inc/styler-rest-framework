""" Custom implementation of encryption
"""

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes


def encrypt(key: str, data: str):
    """Encrypts the data string using a key

    The key will be used by PBKDF2 to derive a new key.
    This new key will be used in an AES cipher configured with EAX mode.

    Args:
        key: a secret string
        data: the data string to be encrypted
    Returns:
        A string containing the ciphertext, nonce, tag, and salt used in
        the encryption process.
    """
    if not key:
        raise ValueError("Key is missing")
    if not data:
        raise ValueError("Data is missing")
    salt = get_random_bytes(40)
    derived_key = PBKDF2(key, salt, 16, count=1000, hmac_hash_module=SHA256)
    cipher = AES.new(derived_key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(data.encode())
    return ".".join([x.hex() for x in [ciphertext, cipher.nonce, tag, salt]])


def decrypt(key: bytes, data: str):
    """Decrypts the data string using a key

    Args:
        key: a secret string
        data: the data string to be decrypted
    Returns:
        The decrypted string
    """
    if not key:
        raise ValueError("Key is missing")
    if not data:
        raise ValueError("Data is missing")
    try:
        ciphertext, nonce, tag, salt = [bytes.fromhex(v) for v in data.split(".")]
        derived_key = PBKDF2(key, salt, 16, count=1000, hmac_hash_module=SHA256)
        cipher = AES.new(derived_key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt_and_verify(ciphertext, tag)
        return plaintext.decode("utf-8")
    except Exception as ex:
        raise DecryptError("Error decrypting the data: %s", str(ex))


class DecryptError(Exception):
    """Raised when an error happened when decrypting the data"""
