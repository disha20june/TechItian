import os
import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


# 32-byte encryption key
SECRET_KEY = os.getenv("DOCUMENT_ENCRYPTION_KEY")

if not SECRET_KEY:
    SECRET_KEY = AESGCM.generate_key(bit_length=256)


def encrypt_document(data):
    """
    Document data ko encrypt karta hai.
    """

    if isinstance(data, str):
        data = data.encode("utf-8")

    aesgcm = AESGCM(SECRET_KEY)

    nonce = os.urandom(12)

    encrypted_data = aesgcm.encrypt(
        nonce,
        data,
        None
    )

    return base64.b64encode(
        nonce + encrypted_data
    ).decode("utf-8")


def decrypt_document(encrypted_data):
    """
    Encrypted document data ko decrypt karta hai.
    """

    try:
        decoded_data = base64.b64decode(
            encrypted_data
        )

        nonce = decoded_data[:12]
        ciphertext = decoded_data[12:]

        aesgcm = AESGCM(SECRET_KEY)

        decrypted_data = aesgcm.decrypt(
            nonce,
            ciphertext,
            None
        )

        return decrypted_data

    except Exception:
        return None