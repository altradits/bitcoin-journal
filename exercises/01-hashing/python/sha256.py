def sha256(data: bytes) -> bytes:
    """Return the 32-byte SHA-256 digest of data. Implement FIPS 180-4 yourself."""
    raise NotImplementedError


def sha256d(data: bytes) -> bytes:
    return sha256(sha256(data))
