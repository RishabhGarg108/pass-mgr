import hashlib
import os
from binascii import hexlify, unhexlify
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

 # Given a secret_key, this generates a crypto key
 # using `PBKDF2` with SHA256 and 1000 iterations.
 # If no salt is given, a new one is generated.
 # The return value is an tuple of `(key, salt)`.
def generateKey(secret_key, salt=None):
    if salt is None:
        salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", secret_key.encode("utf8"), salt, 1000)
    return (key, salt)

# Does an AES encryption of the plaintext.
# Returns an encrypted string combining salt, nonce and the ciphertext.
def encrypt(secret_key, plaintext):
    key, salt = generateKey(secret_key)
    aes = AESGCM(key)
    nonce = os.urandom(16)

    # Converting string plaintext to its binary form.
    plaintext = plaintext.encode("utf8")
    ciphertext = aes.encrypt(nonce, plaintext, None)
    return f"{hexlify(salt).decode('utf8')}-{hexlify(nonce).decode('utf8')}-{hexlify(ciphertext).decode('utf8')}"


# Symmetric decryptor - requires the same secret key to encrypt
# and decrypt the password.
def decrypt(secret_key, ciphertext):
    salt, nonce, ciphertext = map(unhexlify, ciphertext.split("-"))
    key, _ = generateKey(secret_key, salt)
    aes = AESGCM(key)

    plaintext = aes.decrypt(nonce, ciphertext, None)
    return plaintext.decode("utf8")
