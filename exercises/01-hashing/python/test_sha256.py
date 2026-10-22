import pathlib
import unittest

from sha256 import sha256, sha256d

PATH = pathlib.Path(__file__).resolve().parent.parent / "vectors.tsv"
ROWS = [l.split("\t") for l in PATH.read_text().split("\n") if l]


class Vectors(unittest.TestCase):
    def test_vectors(self):
        for h, d1, d2 in ROWS:
            data = bytes.fromhex(h)
            self.assertEqual(sha256(data).hex(), d1, "sha256 " + h[:16])
            self.assertEqual(sha256d(data).hex(), d2, "sha256d " + h[:16])


if __name__ == "__main__":
    unittest.main()
