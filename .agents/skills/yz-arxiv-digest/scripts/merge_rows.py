#!/usr/bin/env python3
"""Merge rows-*.md classification outputs into per-dimension curated files.

Usage:
  python3 merge_rows.py --month 2605 [--dims "self-evolve,memory,tool,..."]
"""
import argparse, glob, json, os, re
from collections import Counter

ap = argparse.ArgumentParser()
ap.add_argument("--month", required=True)
ap.add_argument("--dims", default="self-evolve,memory,tool,mcp,skill,subagent,engineering,coding,eval,planning,safety,multiagent,webgui,domain")
args = ap.parse_args()

OUT = f"/tmp/arxiv{args.month}/out"
CUR = f"/tmp/arxiv{args.month}/curated"
os.makedirs(CUR, exist_ok=True)

row_re = re.compile(r"^\|\s*(" + args.month + r"\.\d{4,5})\s*\|\s*(\d{2}-\d{2})\s*\|\s*(.+?)\s*\|\s*(\S+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*$")

papers, dupes = {}, 0
for path in sorted(glob.glob(f"{OUT}/rows-*.md")):
    for line in open(path):
        m = row_re.match(line.strip())
        if not m:
            continue
        pid, date, title, dim, tags, note = m.groups()
        if "drop/" in tags.lower() or dim.lower().startswith("drop"):
            continue
        title = title.strip()
        if pid in papers:
            dupes += 1
            continue
        papers[pid] = {"id": pid, "date": date, "title": title, "dim": dim,
                       "tags": tags.replace("`", "").strip(), "note": note.strip()}

print(f"merged unique KEEP: {len(papers)} (dupes skipped: {dupes})")
dims = Counter(p["dim"] for p in papers.values())
print("dimension counts:", json.dumps(dims, ensure_ascii=False))

filtered = {p["id"]: p for p in json.load(open(f"{OUT}/filtered.json"))}
mismatch = 0
for pid, p in papers.items():
    src = filtered.get(pid)
    if src and src["published"][5:] != p["date"]:
        p["date"] = src["published"][5:]  # prefer API date over subagent typo
        mismatch += 1
print(f"date fixes from API: {mismatch}; missing from filtered.json: {sum(1 for pid in papers if pid not in filtered)}")

order = args.dims.split(",")
for dim in order:
    rows = sorted((p for p in papers.values() if p["dim"] == dim), key=lambda x: (x["date"], x["id"]), reverse=True)
    if not rows:
        continue
    with open(f"{CUR}/{dim}.md", "w") as f:
        f.write(f"# {dim}（{len(rows)} 篇）\n\n")
        for p in rows:
            f.write(f"| {p['id']} | {p['date']} | {p['title']} | {p['tags']} | {p['note']} |\n")
print("per-dimension files written to", CUR)
json.dump(list(papers.values()), open(f"{OUT}/merged_rows.json", "w"), ensure_ascii=False)
