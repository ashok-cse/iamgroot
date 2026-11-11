#!/usr/bin/env python3
"""Scan public ATS job boards (Greenhouse, Lever, Ashby) and keep the roles that match a search config.

    python3 scripts/discover_jobs.py --config profile/search.json --out profile/jobs/hits.json

Only anonymous GET requests are made; no candidate data is sent.

The config is a JSON file (see search.example.json):
    boards         list of company board slugs to try on every ATS
    include_title  regex a job title must match
    exclude_title  regex that removes a title (seniority, unrelated functions)
    locations      regex a job location must match
"""
import argparse
import html
import json
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

TAG = re.compile(r"<[^>]+>")
UA = {"User-Agent": "Mozilla/5.0 (job-board-reader)", "Accept": "application/json"}


def get(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8", "replace"))
    except Exception:
        return None


def clean(text):
    return re.sub(r"\s+", " ", TAG.sub(" ", html.unescape(text or ""))).strip()


def greenhouse(slug):
    d = get(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true")
    return [dict(ats="greenhouse", company=slug, title=j.get("title", ""),
                 location=(j.get("location") or {}).get("name", ""), url=j.get("absolute_url", ""),
                 updated=j.get("updated_at", ""), text=clean(j.get("content", "")))
            for j in (d or {}).get("jobs", [])]


def lever(slug):
    for host in ("api.lever.co", "api.eu.lever.co"):
        d = get(f"https://{host}/v0/postings/{slug}?mode=json")
        if not isinstance(d, list) or not d:
            continue
        out = []
        for j in d:
            cat = j.get("categories") or {}
            locs = ", ".join(cat.get("allLocations") or [cat.get("location", "")])
            body = " ".join([j.get("descriptionPlain", "")] + [clean(x.get("content", "")) for x in j.get("lists", [])]
                            + [j.get("additionalPlain", "")])
            out.append(dict(ats="lever", company=slug, title=j.get("text", ""), location=locs,
                            url=j.get("hostedUrl", ""), updated=str(j.get("createdAt", "")), text=clean(body)))
        return out
    return []


def ashby(slug):
    d = get(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true")
    out = []
    for j in (d or {}).get("jobs", []):
        locs = [j.get("location", "")] + [s.get("location", "") for s in j.get("secondaryLocations", [])]
        out.append(dict(ats="ashby", company=slug, title=j.get("title", ""), location=", ".join(x for x in locs if x),
                        url=j.get("jobUrl", ""), updated=j.get("publishedAt", ""),
                        employment=j.get("employmentType", ""),
                        comp=(j.get("compensation") or {}).get("compensationTierSummary", "") or "",
                        text=clean(j.get("descriptionPlain", "") or j.get("descriptionHtml", ""))))
    return out


def scan(slug):
    jobs = []
    for fn in (greenhouse, lever, ashby):
        jobs += fn(slug)
    return slug, jobs


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    include = re.compile(cfg["include_title"], re.I)
    exclude = re.compile(cfg["exclude_title"], re.I) if cfg.get("exclude_title") else None
    loc = re.compile(cfg["locations"], re.I)
    slugs = sorted(set(cfg["boards"]))
    hits, boards = [], {}
    with ThreadPoolExecutor(16) as ex:
        for slug, jobs in ex.map(scan, slugs):
            if jobs:
                boards[slug] = (jobs[0]["ats"], len(jobs))
            hits += [j for j in jobs if include.search(j["title"]) and not (exclude and exclude.search(j["title"]))
                     and loc.search(j["location"])]
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(hits, f, ensure_ascii=False, indent=1)
    print(f"boards found: {len(boards)} of {len(slugs)} slugs; matching roles: {len(hits)}")
    print("boards:", ", ".join(f"{s}({v[0]}:{v[1]})" for s, v in sorted(boards.items())))
    missing = [s for s in slugs if s not in boards]
    if missing:
        print("no board for:", ", ".join(missing))


if __name__ == "__main__":
    main()
