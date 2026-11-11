#!/usr/bin/env python3
"""Review discovered roles: a one-line table with requirement flags, or the detail of chosen roles.

    python3 scripts/review_jobs.py profile/jobs/hits.json                       # table of everything
    python3 scripts/review_jobs.py profile/jobs/hits.json --company "wolt|n26"  # filter by company
    python3 scripts/review_jobs.py profile/jobs/hits.json --location "berlin"   # filter by location
    python3 scripts/review_jobs.py profile/jobs/hits.json --show 12 40 63       # requirements of some roles

Flags are hints to read the posting, not decisions:
    yrs:N        highest "N years" figure mentioned
    SENIOR       senior in the title
    NO-SPONSOR?  wording that suggests no visa sponsorship / existing right to work
    sponsor+     wording that suggests visa or relocation support
    LANG-REQ?    a required local-language level (pass the language names with --languages)
    CLEARANCE?   security clearance or citizenship wording
"""
import argparse
import json
import re

YEARS = re.compile(r"(\d{1,2})\s*\+?\s*(?:[-–to]+\s*\d{1,2}\s*\+?\s*)?(?:years|yrs|jahre|ans|años)", re.I)
SPONSOR_NO = re.compile(
    r"(unable|not able|cannot|can't|do not|don't|won't|will not|no)\s+(?:\w+\s+){0,4}(sponsor|visa)|"
    r"without (?:the need for )?(?:visa )?sponsorship|must (?:already )?have (?:the )?right to work|"
    r"existing right to work", re.I)
SPONSOR_YES = re.compile(r"(visa|relocation)\s+(sponsorship|support|assistance)|sponsor\w*\s+visa|we (?:do )?sponsor", re.I)
CLEARANCE = re.compile(r"security clearance|sc clearance|dv clearance|national only|citizen(ship)? (is )?required|"
                       r"must be a \w+ citizen", re.I)
REQ = re.compile(r"(what we.re looking for|who you are|requirements|you.ll be a great fit|about you|what you.ll bring|"
                 r"your profile|we.re looking for|what you bring|qualifications|must.have)", re.I)
KEY = re.compile(r"[^.•\n]*\b(visa|sponsor|right to work|work permit|clearance|relocat|years|start date|on-?site|"
                 r"days (a|per) week|hybrid|remote|fluent|native)\b[^.•\n]*", re.I)


def lang_re(languages):
    if not languages:
        return None
    names = "|".join(re.escape(x) for x in languages)
    level = r"fluent|fluency|native|proficien\w+|business[- ]level|very good|excellent|c1|c2|b2"
    return re.compile(rf"({level})[^.]{{0,60}}({names})|({names})[^.]{{0,40}}({level}|required|mandatory|must)", re.I)


def flags(j, lang):
    t = j.get("text", "")
    f = []
    yrs = [int(x) for x in YEARS.findall(t) if 0 < int(x) < 20]
    if yrs:
        f.append(f"yrs:{max(yrs)}")
    if re.search(r"\bsenior\b|\bsr\.?\b", j["title"], re.I):
        f.append("SENIOR")
    if SPONSOR_NO.search(t):
        f.append("NO-SPONSOR?")
    if SPONSOR_YES.search(t):
        f.append("sponsor+")
    if lang and lang.search(t):
        f.append("LANG-REQ?")
    if CLEARANCE.search(t):
        f.append("CLEARANCE?")
    if j.get("comp"):
        f.append("comp:" + j["comp"][:40])
    return " ".join(f)


def show(hits, idxs, chars):
    for i in idxs:
        j = hits[i]
        t = j["text"]
        m = REQ.search(t, 300)
        s = m.start() if m else 0
        print(f"=== [{i}] {j['company']} | {j['title']} | {j['location'][:60]} | {j['ats']} | {j.get('comp', '')}")
        print("URL:", j["url"])
        print("REQ:", t[s:s + chars])
        seen = set()
        for k in KEY.finditer(t):
            x = k.group(0).strip()[:200]
            if x[:60] not in seen and not (s <= k.start() < s + chars):
                seen.add(x[:60])
                print("  *", x)
            if len(seen) >= 8:
                break
        print()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("hits")
    ap.add_argument("--company", help="regex on the board slug")
    ap.add_argument("--location", help="regex on the location")
    ap.add_argument("--languages", nargs="*", default=[], help="local language names to flag, e.g. German Deutsch")
    ap.add_argument("--show", nargs="*", type=int, help="print the requirements of these indexes")
    ap.add_argument("--chars", type=int, default=900)
    a = ap.parse_args()
    hits = json.load(open(a.hits, encoding="utf-8"))
    if a.show:
        return show(hits, a.show, a.chars)
    lang = lang_re(a.languages)
    comp = re.compile(a.company, re.I) if a.company else None
    loc = re.compile(a.location, re.I) if a.location else None
    rows = [(j["company"], j["title"], i, j) for i, j in enumerate(hits)
            if (not comp or comp.search(j["company"])) and (not loc or loc.search(j["location"]))]
    for company, title, i, j in sorted(rows, key=lambda r: (r[0], r[1])):
        print(f"[{i}] {company} | {title[:70]} | {j['location'][:40]} | {flags(j, lang)}")
    print(f"-- {len(rows)} roles")


if __name__ == "__main__":
    main()
