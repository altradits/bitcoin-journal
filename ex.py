#!/usr/bin/env python3
"""Developer-track helper.

  python3 ex.py start 01 go   --repo ~/bitcoin-journal
  python3 ex.py check 01 go   --repo ~/bitcoin-journal [--push]

`start` copies the exercise (spec, vectors, and the ONE language you pick) into your repo.
`check` runs the tests and commits your work only if they are green.
"""
import argparse, os, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent / "exercises"
CMD = {"python": ["python3", "-m", "unittest"], "go": ["go", "test", "./..."],
       "rust": ["cargo", "test"], "cpp": ["make", "test"], "js": ["node", "--test"]}
ap = argparse.ArgumentParser()
ap.add_argument("action", choices=["start", "check"])
ap.add_argument("num")
ap.add_argument("lang", choices=CMD)
ap.add_argument("--repo", default=os.environ.get("BITCOIN_JOURNAL", ""))
ap.add_argument("--push", action="store_true")
a = ap.parse_args()
if not a.repo:
    sys.exit("Pass --repo or set BITCOIN_JOURNAL")
repo = pathlib.Path(a.repo).expanduser().resolve()
src = next(HERE.glob(f"{a.num}-*"), None)
if not src:
    sys.exit(f"No exercise {a.num} in {HERE}")
dst = repo / "exercises" / src.name
git = lambda *x: subprocess.run(["git", "-C", str(repo), *x], capture_output=True, text=True)

if a.action == "start":
    if (dst / a.lang).exists():
        sys.exit(f"Already started: {dst / a.lang}")
    dst.mkdir(parents=True, exist_ok=True)
    for f in ("README.md", "vectors.tsv"):
        if not (dst / f).exists():
            shutil.copy(src / f, dst / f)
    shutil.copytree(src / a.lang, dst / a.lang)
    print(f"Started. Read {dst / 'README.md'}, then work in {dst / a.lang}")
else:
    if not (dst / a.lang).exists():
        sys.exit("Run `start` first.")
    if subprocess.run(CMD[a.lang], cwd=dst / a.lang).returncode:
        sys.exit("Tests are red. Nothing committed. Fix it and run check again.")
    git("add", "-A", "--", str(dst))
    c = git("commit", "-m", f"ex {a.num} ({a.lang}): tests green, {src.name}")
    print(c.stdout.strip() or c.stderr.strip() or "Committed.")
    if c.returncode == 0 and a.push:
        print(git("push").stderr.strip() or "Pushed.")
