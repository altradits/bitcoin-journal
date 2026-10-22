# 01 Hashing: SHA-256 from scratch

Implement `sha256` yourself from FIPS 180-4 (no crypto libraries) and `sha256d` (SHA-256 applied twice).
Bitcoin uses sha256d for txids, block hashes and proof-of-work, so every later exercise depends on this.

Contract (all languages): bytes in, 32 bytes out. `vectors.tsv` has one case per line:
`input_hex <TAB> sha256_hex <TAB> sha256d_hex` (the first line has empty input).

Steps: pad the message (0x80, zeros, 64-bit big-endian bit length), process 64-byte blocks with the
message schedule and 64 round constants, output the eight 32-bit words big-endian.
Cases at 55, 56, 63 and 64 bytes exist because padding bugs hide at block boundaries.

Stretch: RIPEMD-160 from scratch, then hash160 = ripemd160(sha256(x)), used by P2PKH addresses.
