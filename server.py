#!/usr/bin/env python3
"""Bitcoin Drill server.

  python3 server.py --repo ~/bitcoin-journal --push
  then open http://localhost:8000

Every answer you submit is appended to <repo>/drill-log/YYYY-MM-DD.md and
committed with git. With --push, commits are pushed to your remote shortly
after the last answer (uses your normal git credentials; no tokens in the app).
"""
import argparse, datetime, http.server, json, pathlib, subprocess, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument("--repo", default=str(ROOT / "journal"), help="path to your git repo clone")
ap.add_argument("--port", type=int, default=8000)
ap.add_argument("--push", action="store_true", help="git push after commits")
A = ap.parse_args()

REPO = pathlib.Path(A.repo).expanduser().resolve()
DB = REPO / "progress.json"
LOG = REPO / "drill-log"
timer = None


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, text=True, timeout=120)


def clean(s, n=200):
    return " ".join(str(s or "").split())[:n]


def commit(msg):
    r = git("commit", "-m", clean(msg, 100))
    if r.returncode == 0 and A.push:
        schedule_push()
    return {"ok": r.returncode == 0, "error": (r.stderr or r.stdout).strip()[:300] if r.returncode else ""}


def schedule_push():
    global timer
    if timer:
        timer.cancel()
    timer = threading.Timer(15, lambda: git("push"))
    timer.daemon = True
    timer.start()


def record(d):
    now = datetime.datetime.now()
    LOG.mkdir(exist_ok=True)
    f = LOG / f"{now:%Y-%m-%d}.md"
    if not f.exists():
        f.write_text(f"# Drill log {now:%Y-%m-%d}\n\n")
    mark = "PASS" if d.get("ok") else ("TIMEOUT" if d.get("timeout") else "MISS")
    unit, q = clean(d.get("unit"), 60), clean(d.get("q"))
    given = clean(d.get("given")) or "(no answer)"
    with f.open("a") as h:
        h.write(f"- {now:%H:%M:%S} [{mark}] {unit} / {clean(d.get('stage'), 30)}: {q} -> {given}\n")
    git("add", "-A", "--", "drill-log")
    return commit(f"drill: {mark} {unit} - {q[:50]}")


def save_progress(body):
    DB.write_bytes(body)
    git("add", "-A", "--", "progress.json")
    return commit("drill: progress update")


def streak():
    days = git("log", "--format=%ad", "--date=short").stdout.split()
    today = datetime.date.today()
    d = today if today.isoformat() in days else today - datetime.timedelta(days=1)
    n = 0
    while d.isoformat() in days:
        n += 1
        d -= datetime.timedelta(days=1)
    remote = git("remote", "get-url", "origin").stdout.strip()
    return {"streak": n, "today": days.count(today.isoformat()), "total": len(days), "remote": remote}


def extra_units():
    out = []
    for p in sorted((ROOT / "curriculum").glob("*.json")):
        out += json.loads(p.read_text())
    return out


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=str(ROOT), **k)

    def _json(self, obj):
        b = (obj if isinstance(obj, str) else json.dumps(obj)).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path == "/api/progress":
            return self._json(DB.read_text() if DB.exists() else "{}")
        if self.path == "/api/streak":
            return self._json(streak())
        if self.path == "/api/extra":
            return self._json(extra_units())
        super().do_GET()

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        if n > 20000 or self.path not in ("/api/progress", "/api/answer"):
            return self.send_error(400)
        body = self.rfile.read(n)
        try:
            data = json.loads(body)
        except ValueError:
            return self.send_error(400)
        self._json(save_progress(body) if self.path == "/api/progress" else record(data))


if __name__ == "__main__":
    if not REPO.exists():
        REPO.mkdir(parents=True)
        subprocess.run(["git", "-C", str(REPO), "init"], check=True)
    if git("rev-parse", "--is-inside-work-tree").stdout.strip() != "true":
        sys.exit(f"{REPO} is not a git repository. Clone your repo first, or pass --repo.")
    print(f"Bitcoin Drill at http://localhost:{A.port}\nCommitting to {REPO}" + (" (auto-push on)" if A.push else " (no push)"))
    http.server.ThreadingHTTPServer(("127.0.0.1", A.port), Handler).serve_forever()
