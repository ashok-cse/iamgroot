#!/usr/bin/env python3
"""Scan public job boards and keep the roles that match a search config.

    python3 discover_jobs.py --config profile/search.json --out profile/jobs/hits.json

Covers Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Recruitee and Workable.
Only anonymous requests to public job-board endpoints are made; no candidate data is sent.

The config is a JSON file (see references/search.example.json):
    boards         list of company board names to try on every system
    include_title  regex a job title must match
    exclude_title  regex that removes a title (seniority, unrelated functions)
    locations      regex a job location must match
    systems        optional list limiting which systems to query
"""
import argparse
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

TAG = re.compile(r"<[^>]+>")
UA = {"User-Agent": "Mozilla/5.0 (job-board-reader)", "Accept": "application/json"}


def fetch(url, data=None, raw=False):
    try:
        headers = dict(UA)
        body = None
        if data is not None:
            headers["Content-Type"] = "application/json"
            body = json.dumps(data).encode()
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers, data=body), timeout=20) as r:
            b = r.read()
        return b if raw else json.loads(b.decode("utf-8", "replace"))
    except Exception:
        return None


def clean(text):
    return re.sub(r"\s+", " ", TAG.sub(" ", html.unescape(text or ""))).strip()


def job(ats, company, title, location, url, updated="", text="", **extra):
    return dict(ats=ats, company=company, title=title or "", location=location or "", url=url or "",
                updated=str(updated or ""), text=text or "", **extra)


# Each reader takes (slug, keep) and returns the jobs that pass keep(title, location).
# Systems that need one more request per job for its description filter first, then fetch.

def greenhouse(slug, keep):
    d = fetch(f"https://boards-api.greenhouse.io/v1/boards/{slug}/jobs?content=true")
    jobs = (d or {}).get("jobs", [])
    out = [job("greenhouse", slug, j.get("title"), (j.get("location") or {}).get("name"), j.get("absolute_url"),
               j.get("updated_at"), clean(j.get("content")))
           for j in jobs if keep(j.get("title", ""), (j.get("location") or {}).get("name", ""))]
    return len(jobs), out


def lever(slug, keep):
    for host in ("api.lever.co", "api.eu.lever.co"):
        d = fetch(f"https://{host}/v0/postings/{slug}?mode=json")
        if not isinstance(d, list) or not d:
            continue
        out = []
        for j in d:
            cat = j.get("categories") or {}
            loc = ", ".join(cat.get("allLocations") or [cat.get("location", "")])
            if keep(j.get("text", ""), loc):
                body = " ".join([j.get("descriptionPlain", "")] + [clean(x.get("content")) for x in j.get("lists", [])]
                                + [j.get("additionalPlain", "")])
                out.append(job("lever", slug, j.get("text"), loc, j.get("hostedUrl"), j.get("createdAt"), clean(body)))
        return len(d), out
    return 0, []


def ashby(slug, keep):
    d = fetch(f"https://api.ashbyhq.com/posting-api/job-board/{slug}?includeCompensation=true")
    jobs = (d or {}).get("jobs", [])
    out = []
    for j in jobs:
        loc = ", ".join(x for x in [j.get("location", "")] + [s.get("location", "") for s in j.get("secondaryLocations", [])] if x)
        if keep(j.get("title", ""), loc):
            out.append(job("ashby", slug, j.get("title"), loc, j.get("jobUrl"), j.get("publishedAt"),
                           clean(j.get("descriptionPlain") or j.get("descriptionHtml")),
                           employment=j.get("employmentType", ""),
                           comp=(j.get("compensation") or {}).get("compensationTierSummary", "") or ""))
    return len(jobs), out


def smartrecruiters(slug, keep):
    total, offset, out = 0, 0, []
    while offset < 2000:
        d = fetch(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings?limit=100&offset={offset}")
        content = (d or {}).get("content", [])
        if not content:
            break
        total = d.get("totalFound", total)
        for j in content:
            l = j.get("location") or {}
            loc = l.get("fullLocation") or ", ".join(x for x in (l.get("city"), l.get("region"), l.get("country")) if x)
            if l.get("remote"):
                loc += " (remote)"
            if keep(j.get("name", ""), loc):
                det = fetch(f"https://api.smartrecruiters.com/v1/companies/{slug}/postings/{j.get('id')}") or {}
                sections = ((det.get("jobAd") or {}).get("sections") or {})
                text = " ".join(clean((sections.get(k) or {}).get("text"))
                                for k in ("jobDescription", "qualifications", "additionalInformation"))
                url = det.get("postingUrl") or f"https://jobs.smartrecruiters.com/{slug}/{j.get('id')}"
                out.append(job("smartrecruiters", slug, j.get("name"), loc, url, j.get("releasedDate"), text))
        offset += 100
        if offset >= total:
            break
    return total, out


def personio(slug, keep):
    for tld in ("de", "com"):
        b = fetch(f"https://{slug}.jobs.personio.{tld}/xml?language=en", raw=True)
        if not b or not b.lstrip().startswith(b"<"):
            continue
        try:
            positions = ET.fromstring(b).findall(".//position")
        except ET.ParseError:
            continue
        out = []
        for p in positions:
            title, loc = p.findtext("name") or "", p.findtext("office") or ""
            if keep(title, loc):
                text = " ".join(clean(x.findtext("value")) for x in p.findall(".//jobDescription"))
                out.append(job("personio", slug, title, loc,
                               f"https://{slug}.jobs.personio.{tld}/job/{p.findtext('id')}?language=en",
                               p.findtext("createdAt"), text, employment=p.findtext("schedule") or ""))
        return len(positions), out
    return 0, []


def recruitee(slug, keep):
    d = fetch(f"https://{slug}.recruitee.com/api/offers/")
    offers = (d or {}).get("offers", []) if isinstance(d, dict) else []
    out = [job("recruitee", slug, j.get("title"), j.get("location") or ", ".join(x for x in (j.get("city"), j.get("country")) if x),
               j.get("careers_url"), j.get("published_at"), clean((j.get("description") or "") + " " + (j.get("requirements") or "")))
           for j in offers
           if keep(j.get("title", ""), j.get("location") or ", ".join(x for x in (j.get("city"), j.get("country")) if x))]
    return len(offers), out


def workable(slug, keep):
    total, out, token = 0, [], None
    for _ in range(10):
        body = {"query": "", "location": [], "department": [], "worktype": [], "remote": []}
        if token:
            body["token"] = token
        d = fetch(f"https://apply.workable.com/api/v3/accounts/{slug}/jobs", data=body)
        results = (d or {}).get("results", [])
        if not results:
            break
        total = d.get("total", total)
        for j in results:
            l = j.get("location") or {}
            loc = ", ".join(x for x in (l.get("city"), l.get("region"), l.get("country")) if x) + (" (remote)" if j.get("remote") else "")
            if keep(j.get("title", ""), loc):
                det = fetch(f"https://apply.workable.com/api/v2/accounts/{slug}/jobs/{j.get('shortcode')}") or {}
                text = " ".join(clean(det.get(k)) for k in ("description", "requirements", "benefits"))
                out.append(job("workable", slug, j.get("title"), loc,
                               f"https://apply.workable.com/{slug}/j/{j.get('shortcode')}/", j.get("published"), text))
        token = d.get("nextPage")
        if not token:
            break
    return total, out


SYSTEMS = {"greenhouse": greenhouse, "lever": lever, "ashby": ashby, "smartrecruiters": smartrecruiters,
           "personio": personio, "recruitee": recruitee, "workable": workable}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--config", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    cfg = json.load(open(a.config, encoding="utf-8"))
    include = re.compile(cfg["include_title"], re.I)
    exclude = re.compile(cfg["exclude_title"], re.I) if cfg.get("exclude_title") else None
    loc_re = re.compile(cfg["locations"], re.I)
    readers = [SYSTEMS[s] for s in (cfg.get("systems") or SYSTEMS)]

    def keep(title, location):
        return bool(include.search(title or "") and not (exclude and exclude.search(title or "")) and loc_re.search(location or ""))

    def scan(slug):
        found, hits = {}, []
        for reader in readers:
            try:
                total, jobs = reader(slug, keep)
            except Exception:
                total, jobs = 0, []
            if total:
                found[reader.__name__] = total
            hits += jobs
        return slug, found, hits

    slugs = sorted(set(cfg["boards"]))
    hits, boards = [], {}
    with ThreadPoolExecutor(16) as ex:
        for slug, found, jobs in ex.map(scan, slugs):
            if found:
                boards[slug] = found
            hits += jobs
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(hits, f, ensure_ascii=False, indent=1)
    print(f"boards found: {len(boards)} of {len(slugs)} names; matching roles: {len(hits)}")
    print("boards:", ", ".join(f"{s}({'/'.join(f'{k}:{v}' for k, v in found.items())})" for s, found in sorted(boards.items())))
    missing = [s for s in slugs if s not in boards]
    if missing:
        print("no board for:", ", ".join(missing))


if __name__ == "__main__":
    main()
