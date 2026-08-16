#!/usr/bin/env python3
"""Fetch one month of arXiv papers via Atom API with pagination.

Usage:
  python3 fetch.py --month 2605 [--out /tmp/arxiv2605] [--queries queries.txt]

queries.txt: one arXiv API query expression per line (WITHOUT the date filter).
Default queries are the AI-Agent topic set proven on 2604/2606.
"""
import argparse, calendar, json, os, re, time, urllib.parse, urllib.request, xml.etree.ElementTree as ET

NS = {"a": "http://www.w3.org/2005/Atom", "os": "http://a9.com/-/spec/opensearch/1.1/"}

DEFAULT_QUERIES = {
    "agent": '(all:"agent" OR all:"agents" OR all:"agentic" OR all:"multiagent" OR all:"multi-agent")',
    "suppl": '(all:"MCP" OR all:"sub-agent" OR all:"subagent" OR all:"skill library" OR all:"agent skill" OR all:"agent skills" OR all:"harness" OR all:"context engineering" OR all:"prompt engineering")',
    "coding": '(all:"SWE-bench" OR all:"coding agent" OR all:"coding agents" OR all:"code agent" OR all:"code agents" OR all:"software engineering agent" OR all:"autonomous coding")',
}


def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "ai-notes-digest/0.2 (mailto:local@example.com)"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            print(f"    retry {i+1}: {e}", flush=True)
            time.sleep(10 * (i + 1))
    raise RuntimeError(f"failed: {url}")


def fetch_query(name, expr, date, out):
    all_entries, start, total = {}, 0, None
    while True:
        q = f"{date} AND {expr}"
        url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q, safe="")
               + f"&start={start}&max_results=100&sortBy=submittedDate&sortOrder=ascending")
        root = ET.fromstring(fetch(url))
        if total is None:
            total = int(root.find("os:totalResults", NS).text)
            print(f"[{name}] total={total}", flush=True)
        entries = root.findall("a:entry", NS)
        if not entries:
            break
        for e in entries:
            eid = e.find("a:id", NS).text
            base = eid.rsplit("/abs/", 1)[-1].split("v")[0]
            all_entries[base] = {
                "id": base,
                "published": e.find("a:published", NS).text[:10],
                "updated": e.find("a:updated", NS).text[:10],
                "title": re.sub(r"\s+", " ", e.find("a:title", NS).text).strip(),
                "summary": re.sub(r"\s+", " ", e.find("a:summary", NS).text).strip(),
                "cats": [c.attrib["term"] for c in e.findall("a:category", NS)],
                "primary": e.find("a:arxiv:primary_category", NS).attrib["term"] if e.find("a:arxiv:primary_category", NS) is not None else "",
                "authors": [a.find("a:name", NS).text for a in e.findall("a:author", NS)][:6],
            }
        start += 100
        if start >= total:
            break
        time.sleep(3)
    with open(f"{out}/{name}.json", "w") as f:
        json.dump(list(all_entries.values()), f, ensure_ascii=False)
    print(f"[{name}] saved {len(all_entries)}", flush=True)
    return all_entries


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="YYMM, e.g. 2605")
    ap.add_argument("--out", default=None)
    ap.add_argument("--queries", default=None, help="file with one query expression per line")
    args = ap.parse_args()

    out = args.out or f"/tmp/arxiv{args.month}"
    os.makedirs(f"{out}/raw", exist_ok=True)
    os.makedirs(f"{out}/out", exist_ok=True)

    year, mm = "20" + args.month[:2], args.month[2:]
    last = calendar.monthrange(int(year), int(mm))[1]
    date = f"submittedDate:[{year}{mm}010000 TO {year}{mm}{last:02d}2359]"

    if args.queries:
        queries = {}
        for i, line in enumerate(open(args.queries)):
            line = line.strip()
            if line and not line.startswith("#"):
                queries[f"q{i+1}"] = line
    else:
        queries = DEFAULT_QUERIES

    merged = {}
    for name, expr in queries.items():
        for k, v in fetch_query(name, expr, date, f"{out}/out").items():
            merged.setdefault(k, v)
    with open(f"{out}/out/merged.json", "w") as f:
        json.dump(list(merged.values()), f, ensure_ascii=False)
    print(f"[merged] {len(merged)} unique papers")


if __name__ == "__main__":
    main()
