#!/usr/bin/env python3
"""Filter merged arXiv papers and emit batch review files.

Usage:
  python3 filter_batch.py --month 2605 [--batch 110]
                          [--cats "cs.AI,cs.CL,..."]
                          [--signal "(LLMs?|large language|...)"]
"""
import argparse, json, os, re

ap = argparse.ArgumentParser()
ap.add_argument("--month", required=True)
ap.add_argument("--batch", type=int, default=110)
ap.add_argument("--cats", default="cs.AI,cs.CL,cs.SE,cs.LG,cs.MA,cs.CR,stat.ML,cs.HC,cs.CY,cs.IR,cs.PL,cs.OS,cs.NI,cs.DC,cs.SI")
ap.add_argument("--signal", default=r"(LLMs?|large language|language model|GPT-|Claude|Gemini|Qwen|LLaMA|DeepSeek|foundation model|MCP|Model Context Protocol|agentic)")
args = ap.parse_args()

OUT = f"/tmp/arxiv{args.month}/out"
BATCH_DIR = f"/tmp/arxiv{args.month}/batches"
os.makedirs(BATCH_DIR, exist_ok=True)

ALLOW_CATS = set(args.cats.split(","))
LLM_SIG = re.compile(args.signal, re.I)

papers = json.load(open(f"{OUT}/merged.json"))
print(f"merged: {len(papers)}")

kept, drop_id, drop_cat, drop_sig = [], 0, 0, 0
for p in papers:
    if not p["id"].startswith(args.month):
        drop_id += 1
        continue
    cats = set(p["cats"]) | {p["primary"]}
    if not (cats & ALLOW_CATS):
        drop_cat += 1
        continue
    if not LLM_SIG.search(p["title"] + " " + p["summary"]):
        drop_sig += 1
        continue
    kept.append(p)

print(f"kept after filter: {len(kept)} (dropped: wrong-month id={drop_id}, cat={drop_cat}, no-signal={drop_sig})")
kept.sort(key=lambda p: (p["published"], p["id"]))

n_batches = (len(kept) + args.batch - 1) // args.batch
for i in range(n_batches):
    chunk = kept[i * args.batch:(i + 1) * args.batch]
    with open(f"{BATCH_DIR}/batch-{i+1:02d}.md", "w") as f:
        f.write(f"# Batch {i+1}/{n_batches}（{chunk[0]['published']} ~ {chunk[-1]['published']}，共 {len(chunk)} 篇）\n\n")
        for j, p in enumerate(chunk, 1):
            cats = ",".join(p["cats"][:4])
            abstract = p["summary"][:900] + ("…" if len(p["summary"]) > 900 else "")
            f.write(f"### {j}. {p['id']} | {p['published']} | {cats}\n{p['title']}\n\n{abstract}\n\n")
print(f"wrote {n_batches} batch files to {BATCH_DIR}")
json.dump(kept, open(f"{OUT}/filtered.json", "w"), ensure_ascii=False)
