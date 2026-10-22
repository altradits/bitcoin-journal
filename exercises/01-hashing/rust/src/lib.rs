/// Return the SHA-256 digest of `data`. Implement FIPS 180-4 yourself.
pub fn sha256(_data: &[u8]) -> [u8; 32] {
    todo!("implement SHA-256")
}

pub fn sha256d(data: &[u8]) -> [u8; 32] {
    sha256(&sha256(data))
}
