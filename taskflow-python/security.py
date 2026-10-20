"""Password hashing with Python's standard library (no passwords are ever stored as plain text)."""
import hashlib
import hmac
import os

ITERATIONS = 200_000


def hash_password(password):
    """Returns 'salt$hash' (both hex). A random salt means equal passwords get different hashes."""
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"{salt.hex()}${digest.hex()}"


def verify_password(password, stored):
    try:
        salt_hex, digest_hex = stored.split("$")
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return hmac.compare_digest(actual, expected)
