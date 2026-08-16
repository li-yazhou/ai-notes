#!/usr/bin/env python3
"""Full validation of a digest document against the source database.

Hard issues (exit 1): link ID missing from DB; date column != API published.
Soft issues (print for manual review): display-title / DB-title mismatch; duplicate IDs.

Usage:
  python3 validate.py --doc <digest.md> --db /tmp/arxiv2605/out/filtered.json --month 2605
"""
import argparse, json, re, sys

ap = argparse.ArgumentParser()
ap.add_argument("--doc", required=True)
ap.add_argument("--db", required=True)
ap.add_argument("--month", required=True)
args = ap.parse_args()

doc = open(args.doc).read()
db = {p["id"]: p for p in json.load(open(args.db))}


def norm(t):
    return re.sub(r"[^a-z0-9]", "", t.lower())


rows = re.findall(r"\| \[([^\]]+)\]\(https://arxiv\.org/abs/(" + args.month + r"\.\d{4,5})\) \| (\d{2}-\d{2}) \|", doc)
hard, soft = 0, 0
for title, pid, date in rows:
    src = db.get(pid)
    if not src:
        print(f"HARD MISSING {pid} | {title}")
        hard += 1
        continue
    if src["published"][5:] != date:
        print(f"HARD DATE {pid} doc={date} vs api={src['published']}")
        hard += 1
    a, b = norm(title), norm(src["title"])
    if not (b.startswith(a[:16]) or a.startswith(b[:16]) or a[:16] in b or b[:16] in a):
        print(f"SOFT TITLE {pid} | doc: {title[:55]} || api: {src['title'][:55]}")
        soft += 1

from collections import Counter
dups = {k: v for k, v in Counter(re.findall(r"abs/(" + args.month + r"\.\d{4,5})", doc)).items() if v > 1}
print(f"\nduplicate IDs ({len(dups)}): {sorted(dups)}  <- 只允许来自「本月必读」复引")
print(f"rows checked: {len(rows)} | hard issues: {hard} | soft (title) issues: {soft}")
sys.exit(1 if hard else 0)
