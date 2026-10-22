# Developer track: build it to understand it

Learn Me A Bitcoin's author learns by writing his own tools first. Do the same, in any language.
One folder per exercise: `exercises/NN-name/` with a test using a published test vector.
Commit only when the test is green: `ex NN: <what works now>`.

01 Hashing: sha256, double sha256, hash160 (tests against known digests)
02 Base58Check and WIF encode/decode (https://learnmeabitcoin.com/technical/wif)
03 Private key to compressed public key on secp256k1 (https://learnmeabitcoin.com/technical/private-key)
04 Legacy P2PKH address from a public key
05 BIP39 mnemonic to seed, then BIP32 child derivation, checked against BIP32 test vector 1
   (https://learnmeabitcoin.com/technical/mnemonic, https://learnmeabitcoin.com/technical/extended-keys)
06 Parse a raw transaction hex by hand (varints, inputs, outputs) and compute its txid
07 ECDSA sign and verify; build and broadcast a P2PKH spend on regtest
   (https://learnmeabitcoin.com/technical/keys/signature/)
08 A tiny Script interpreter: P2PKH, then multisig (https://learnmeabitcoin.com/technical/script)
09 PSBT creator and updater (https://learnmeabitcoin.com/technical/transaction/psbt/)
10 Block header hash, proof-of-work check, Merkle root
11 P2WPKH sighash (https://learnmeabitcoin.com/technical/upgrades/segregated-witness/), then Taproot key path
   (https://learnmeabitcoin.com/technical/upgrades/taproot/)
12 Capstone: first real PR to a project from the Btrust Resource Hub, following its cheat sheets

## Running the track
Pick your language per exercise (python, go, rust, cpp, js). You can switch languages between exercises.

    python3 ex.py start 01 go --repo ~/bitcoin-journal
    python3 ex.py check 01 go --repo ~/bitcoin-journal --push

`check` commits only when the tests are green, so every exercise commit is proof of work.
Exercise 01 is ready; later ones will be added to `exercises/` in order.
