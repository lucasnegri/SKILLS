#!/usr/bin/env python3
"""Task intake helper for the N4 Studio workspace.

  intake.py clients                      list client folders + the ticket codes seen in them
  intake.py resolve "<text>"             guess client, task id and title from a ticket paste or short line
  intake.py find <client> <id>           print existing task folders for that id (duplicate check)
  intake.py create <client> <id> "<title>"   create the task folder (prints its path)

<id> is a number like 10700 (or T10700 / #T10700), or "adhoc".
Standard library only.
"""
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(os.environ.get("N4_ROOT", Path.home() / "Documents/Projects/N4 Studio"))
CODE_RE = re.compile(r"^\s*([A-Z]{3,5})\s*\|\s*(.+?)\s*$", re.M)
ID_RE = re.compile(r"#?\[?T\s?(\d{4,6})\b")
ADHOC_RE = re.compile(r"#?T?ad\s?-?hoc", re.I)


def client_dirs():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith("."))


def codes_for(client: Path):
    codes = set()
    ctxs = list(client.glob("*/foundation/context.md")) + list(client.glob("*/context.md"))
    for ctx in ctxs:
        try:
            head = ctx.read_text(errors="ignore")[:2000]
        except OSError:
            continue
        for m in CODE_RE.finditer(head):
            codes.add(m.group(1))
    return sorted(codes)


def cmd_clients():
    out = [{"client": c.name, "codes": codes_for(c)} for c in client_dirs()]
    print(json.dumps(out, indent=1))


def norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def cmd_resolve(text):
    code_m = CODE_RE.search(text)
    id_m = ID_RE.search(text)
    code = code_m.group(1) if code_m else None
    title = code_m.group(2) if code_m else None
    task_id = id_m.group(1) if id_m else ("adhoc" if ADHOC_RE.search(text) else None)

    matches = []
    for c in client_dirs():
        reason = None
        if code and code in codes_for(c):
            reason = f"code {code}"
        elif norm(c.name) and norm(c.name) in norm(text):
            reason = "name in text"
        elif code and norm(c.name).startswith(code.lower()[:4]):
            reason = f"name starts like {code}"
        if reason:
            matches.append({"client": c.name, "reason": reason})
    print(json.dumps({"code": code, "id": task_id, "title": title, "clients": matches}, indent=1))


def parse_id(raw):
    if ADHOC_RE.fullmatch(raw.strip()) or raw.strip().lower() == "adhoc":
        return "adhoc"
    m = re.search(r"(\d{4,6})", raw)
    if not m:
        sys.exit(f"Bad task id: {raw!r}")
    return m.group(1)


def client_path(name):
    p = ROOT / name
    if not p.is_dir():
        cands = [c.name for c in client_dirs() if norm(c.name) == norm(name)]
        if len(cands) == 1:
            return ROOT / cands[0]
        sys.exit(f"No client folder {name!r} in {ROOT}")
    return p


def existing(client: Path, task_id):
    if task_id == "adhoc":
        return []
    return [str(p) for p in client.iterdir() if p.is_dir() and re.search(rf"T\s?{task_id}\b", p.name)]


def cmd_find(client, raw_id):
    print(json.dumps(existing(client_path(client), parse_id(raw_id)), indent=1))


def clean_title(title):
    title = CODE_RE.sub(lambda m: m.group(2), title).strip()  # drop "CODE |" prefix
    title = title.replace("/", ":")                          # Finder shows ":" as "/"
    title = re.sub(r"\s+", " ", title).strip(" -")
    return title


def cmd_create(client, raw_id, title):
    c = client_path(client)
    task_id = parse_id(raw_id)
    dupes = existing(c, task_id)
    if dupes:
        print(json.dumps({"exists": dupes}))
        return
    prefix = "#ADHoc" if task_id == "adhoc" else f"#T{task_id}"
    folder = c / f"{prefix} - {clean_title(title)}"
    if folder.exists():
        print(json.dumps({"exists": [str(folder)]}))
        return
    folder.mkdir()
    for sub in ("foundation", "development", "reference"):
        (folder / sub).mkdir()
    print(json.dumps({"created": str(folder), "context": str(folder / "foundation" / "context.md")}))


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "clients":
        cmd_clients()
    elif a[0] == "resolve" and len(a) == 2:
        cmd_resolve(a[1] if a[1] != "-" else sys.stdin.read())
    elif a[0] == "find" and len(a) == 3:
        cmd_find(a[1], a[2])
    elif a[0] == "create" and len(a) == 4:
        cmd_create(a[1], a[2], a[3])
    else:
        sys.exit(__doc__)
