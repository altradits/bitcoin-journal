import test from "node:test";
import assert from "node:assert";
import fs from "node:fs";
import { sha256, sha256d } from "./sha256.js";

const rows = fs.readFileSync(new URL("../vectors.tsv", import.meta.url), "utf8")
  .split("\n").filter(Boolean).map((l) => l.split("\t"));

test("vectors", () => {
  for (const [h, a, b] of rows) {
    const d = Buffer.from(h, "hex");
    assert.equal(Buffer.from(sha256(d)).toString("hex"), a, "sha256 " + h.slice(0, 16));
    assert.equal(Buffer.from(sha256d(d)).toString("hex"), b, "sha256d " + h.slice(0, 16));
  }
});
