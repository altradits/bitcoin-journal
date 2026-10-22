package drill

// Sha256 returns the SHA-256 digest of data. Implement FIPS 180-4 yourself.
func Sha256(data []byte) [32]byte {
	panic("not implemented")
}

func Sha256d(data []byte) [32]byte {
	a := Sha256(data)
	return Sha256(a[:])
}
