import os
from pydantic import BaseModel, constr
from base64 import b64decode, b64encode

from app.config import get_app_settings
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

settings = get_app_settings()

class Plaintext(BaseModel):
    plaintext: constr(max_length=settings.max_plaintext_size)

class Ciphertext(BaseModel):
    ciphertext: str

class Challenge(BaseModel):
    iv: str
    ciphertext: str

class CtrPlaintext(BaseModel):
    plaintext: str

class CtrModeCiphertext(Ciphertext):
    nonce: str

class PublicKey(BaseModel):
    key: str

class SignedPublicKey(PublicKey):
    signature: str

class RSAandDHParams(PublicKey):
    dh_params: str


def derive_key(key_seed: str) -> bytes:
    """Derives encryption/decryption key from the given key_seed.
    Uses modern key derivation function (KDF) scrypt.
    """
    kdf = Scrypt(
        salt=b'',
        length=32,
        n=2**14,
        r=8,
        p=1,
    )
    key = kdf.derive(key_seed.encode())
    return key


def encrypt_challenge(key: bytes, challenge: str) -> Challenge:
    """Encrypts challenge in CBC mode using the provided key.
    """
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(challenge.encode())
    padded_data += padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data)
    ciphertext += encryptor.finalize()

    encoded_iv = b64encode(iv)
    encoded_ciphertext = b64encode(ciphertext)
    return Challenge(iv=encoded_iv, ciphertext=encoded_ciphertext)


def decrypt_challenge(key: bytes, challenge: Challenge) -> str:
    """Decrypts encrypted challenge; reveals a password that can be
    used to unlock the next task/challenge.
    """
    iv = b64decode(challenge.iv)
    ciphertext = b64decode(challenge.ciphertext)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    plaintext += decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext)
    plaintext += unpadder.finalize()
    return plaintext.decode()


def ecb_encrypt(key: bytes, plaintext: str) -> str:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode())
    padded_data += padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.ECB())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data)
    ciphertext += encryptor.finalize()

    encoded_ciphertext = b64encode(ciphertext)
    return Ciphertext(ciphertext=encoded_ciphertext)


def ecb_decrypt(key: bytes, ciphertext: str) -> str:
    ciphertext = b64decode(ciphertext)

    cipher = Cipher(algorithms.AES(key), modes.ECB())
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    plaintext += decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(plaintext)
    plaintext += unpadder.finalize()
    return plaintext.decode()


def cbc_encrypt(key: bytes, plaintext: str, iv: bytes = None) -> Challenge:
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext.encode())
    padded_data += padder.finalize()

    if not iv:
        iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data)
    ciphertext += encryptor.finalize()

    encoded_iv = b64encode(iv)
    encoded_ciphertext = b64encode(ciphertext)
    return Challenge(iv=encoded_iv, ciphertext=encoded_ciphertext)


def cbc_decrypt(key: bytes, challenge: Challenge) -> str:
    return decrypt_challenge(key=key, challenge=challenge)


def ctr_encrypt(key: bytes, plaintext: str, nonce: bytes = None) -> CtrModeCiphertext:
    if not nonce:
        nonce = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(plaintext.encode())
    ciphertext += encryptor.finalize()

    encoded_nonce = b64encode(nonce)
    encoded_ciphertext = b64encode(ciphertext)
    return CtrModeCiphertext(nonce=encoded_nonce, ciphertext=encoded_ciphertext)


def ctr_decrypt(key: bytes, ciphertext: CtrModeCiphertext) -> str:
    nonce = b64decode(ciphertext.nonce)
    ciphertext = b64decode(ciphertext.ciphertext)

    cipher = Cipher(algorithms.AES(key), modes.CTR(nonce))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext)
    plaintext += decryptor.finalize()
    return plaintext.decode()
