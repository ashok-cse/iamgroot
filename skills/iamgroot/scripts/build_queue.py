#!/usr/bin/env python3
"""Turn chosen roles from hits.json into the batched queue that the apply-jobs workflow reads.

    python3 scripts/build_queue.py profile/jobs/hits.json profile/jobs/queue.json \
        --batch A=12,40,63 --batch B=7,19 --market Germany="berlin|germany|munich" --market UK="london|united kingdom"

Keep one role per company across all batches: many employers cap applications per candidate.
Rows already in the tracker (--tracker) are refused, so a role is never queued twice.
"""
import argparse
import csv
import json
import re


def apply_url(j):
    u = j["url"]
    if j.get("apply"):  # a portal listing that names the employer's own application page
        return j["apply"]
    if j["ats"] == "ashby":
        return u.rstrip("/") + "/application"
    if j["ats"] == "lever":
        return u.rstrip("/") + "/apply"
    if j["ats"] == "greenhouse":
        m = re.search(r"(?:jobs/|gh_jid=)(\d+)", u)
        # the embed URL opens the form top-level even when the company site wraps it in an iframe
        return f"https://job-boards.greenhouse.io/embed/job_app?for={j['company']}&token={m.group(1)}" if m else u
    return u


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hits")
    ap.add_argument("out")
    ap.add_argument("--batch", action="append", required=True, metavar="ID=i,j,k")
    ap.add_argument("--market", action="append", default=[], metavar="NAME=regex")
    ap.add_argument("--tracker", help="tracker CSV; roles whose Job URL is already there are refused")
    a = ap.parse_args()
    hits = json.load(open(a.hits, encoding="utf-8"))
    markets = [(m.split("=", 1)[0], re.compile(m.split("=", 1)[1], re.I)) for m in a.market]
    tracked = set()
    if a.tracker:
        with open(a.tracker, newline="", encoding="utf-8") as f:
            tracked = {r["Job URL"] for r in csv.DictReader(f)}
    queue, companies = {}, {}
    for spec in a.batch:
        bid, idxs = spec.split("=", 1)
        queue[bid] = []
        for i in map(int, idxs.split(",")):
            j = hits[i]
            if j["url"] in tracked:
                raise SystemExit(f"[{i}] {j['company']} | {j['title']} is already in the tracker")
            if j["company"] in companies:
                raise SystemExit(f"[{i}] second role for {j['company']} (first: [{companies[j['company']]}])")
            companies[j["company"]] = i
            gh = re.search(r"(?:jobs/|gh_jid=)(\d+)", j["url"]) if j["ats"] == "greenhouse" else None
            queue[bid].append({
                "id": i, "company": j["company"], "position": j["title"].strip(), "location": j["location"],
                "ats": j["ats"], "markets_listed": [n for n, rx in markets if rx.search(j["location"])],
                "job_url": j["url"], "application_url": apply_url(j),
                "greenhouse_board": j["company"] if gh else "", "greenhouse_job_id": gh.group(1) if gh else "",
                "compensation": j.get("comp", ""), "job_description": j["text"][:6000],
            })
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=1)
    for bid, jobs in queue.items():
        print(bid, len(jobs), "|", "; ".join(f"{x['company']}: {x['position'][:36]}" for x in jobs))
    print("total", sum(len(v) for v in queue.values()))


if __name__ == "__main__":
    main()
