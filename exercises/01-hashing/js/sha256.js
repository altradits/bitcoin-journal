// Return the 32-byte SHA-256 digest of data (Uint8Array). Implement FIPS 180-4 yourself.
export function sha256(data) {
  throw new Error("not implemented");
}

export function sha256d(data) {
  return sha256(sha256(data));
}
