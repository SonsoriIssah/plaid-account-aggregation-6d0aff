"""Symmetric encryption for tokens at rest. MVP uses an app secret; production
should source the key from a KMS and rotate it."""
from __future__ import annotations

import os

from cryptography.fernet import Fernet


def _cipher() -> Fernet:
    key = os.environ.get("TOKEN_ENC_KEY")
    if not key:
        raise RuntimeError("TOKEN_ENC_KEY is required to encrypt tokens at rest")
    return Fernet(key.encode())


def encrypt(plaintext: str) -> bytes:
    return _cipher().encrypt(plaintext.encode())


def decrypt(ciphertext: bytes) -> str:
    return _cipher().decrypt(ciphertext).decode()
