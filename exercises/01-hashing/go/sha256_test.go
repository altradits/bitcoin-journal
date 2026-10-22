package drill

import (
	"encoding/hex"
	"os"
	"strings"
	"testing"
)

func TestVectors(t *testing.T) {
	raw, err := os.ReadFile("../vectors.tsv")
	if err != nil {
		t.Fatal(err)
	}
	for _, line := range strings.Split(strings.TrimRight(string(raw), "\n"), "\n") {
		f := strings.Split(line, "\t")
		in, _ := hex.DecodeString(f[0])
		a, b := Sha256(in), Sha256d(in)
		if hex.EncodeToString(a[:]) != f[1] {
			t.Errorf("sha256 mismatch for input %.16s", f[0])
		}
		if hex.EncodeToString(b[:]) != f[2] {
			t.Errorf("sha256d mismatch for input %.16s", f[0])
		}
	}
}
