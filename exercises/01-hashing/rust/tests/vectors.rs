use drill::{sha256, sha256d};

fn unhex(s: &str) -> Vec<u8> {
    (0..s.len() / 2).map(|i| u8::from_str_radix(&s[2 * i..2 * i + 2], 16).unwrap()).collect()
}
fn hex(b: &[u8]) -> String {
    b.iter().map(|x| format!("{:02x}", x)).collect()
}

#[test]
fn vectors() {
    for line in include_str!("../../vectors.tsv").lines().filter(|l| !l.is_empty()) {
        let f: Vec<&str> = line.split('\t').collect();
        let d = unhex(f[0]);
        let tag = &f[0][..f[0].len().min(16)];
        assert_eq!(hex(&sha256(&d)), f[1], "sha256 {}", tag);
        assert_eq!(hex(&sha256d(&d)), f[2], "sha256d {}", tag);
    }
}
