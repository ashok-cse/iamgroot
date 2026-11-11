#!/usr/bin/env python3
"""Scan public job boards and keep the roles that match a search config.

    python3 discover_jobs.py --config profile/search.json --out profile/jobs/hits.json

Two kinds of source, both read with anonymous requests:

  company career pages   Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Recruitee and Workable,
                         tried for every name under "boards"
  job portals            boards that publish an open feed, named under "portals":
                         arbeitnow, germantechjobs (Germany), swissdevjobs, jobsch (Switzerland),
                         devitjobsuk (United Kingdom), devitjobsnl (Netherlands), devitjobsus (United States, Canada),
                         platsbanken (Sweden), duunitori (Finland), mycareersfuture (Singapore),
                         instahyre, hasjob (India), landingjobs (Europe),
                         remotive, remoteok, jobicy, himalayas, workingnomads (remote roles)

No candidate data is sent. The only text that leaves the machine is the company names and, for portals
that search by text, the search terms under "queries": keep personal details out of both.

The config is a JSON file (see references/search.example.json):
    boards         company board names to try on every career-page system (may be empty)
    include_title  regex a job title must match
    exclude_title  regex that removes a title (seniority, unrelated functions)
    locations      regex a job location must match; portal locations end with the country name in English
    systems        optional list limiting which career-page systems to query
    portals        optional list of job portals to read
    queries        search terms for the portals that search by text
    only_english   true keeps only portal listings written in English
"""
import argparse
import html
import json
import re
import urllib.parse
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


# Job portals with an open feed. Each reader takes (queries, keep) and returns
# (number of listings read, matching jobs). Locations end with the country name in English,
# so one "locations" regex works for career pages and portals alike.

ENGLISH_WORDS = {"the", "and", "you", "with", "our", "for", "are", "will", "team", "experience", "we", "to", "of", "in"}


def looks_english(text):
    words = re.findall(r"[^\W\d_]+", (text or "").lower())[:400]
    return bool(words) and sum(w in ENGLISH_WORDS for w in words) / len(words) > 0.12


def pay(low, high, unit):
    return f"{low}-{high} {unit}" if low and high else ""


def arbeitnow(queries, keep):
    total, out = 0, []
    for page in range(1, 11):
        d = fetch(f"https://www.arbeitnow.com/api/job-board-api?page={page}")
        data = (d or {}).get("data", [])
        if not data:
            break
        total += len(data)
        for j in data:
            loc = re.sub(r"\bDeutschland\b", "Germany", j.get("location") or "")
            loc += ("" if "germany" in loc.lower() else ", Germany") + (" (remote)" if j.get("remote") else "")
            if keep(j.get("title", ""), loc):
                text = clean(j.get("description")) + " " + " ".join((j.get("tags") or []) + (j.get("job_types") or []))
                out.append(job("arbeitnow", j.get("company_name"), j.get("title"), loc, j.get("url"), j.get("created_at"), text))
        if not ((d.get("links") or {}).get("next")):
            break
    return total, out


def _devjobs(site, name, country, currency):
    """Reader for the DevJobs family of boards (same feed format on every country site)."""
    def reader(queries, keep):
        d = fetch(f"https://{site}/api/jobsLight")
        data = d if isinstance(d, list) else []
        out = []
        for j in data:
            where = country(j) if callable(country) else country
            loc = f"{j.get('actualCity') or j.get('cityCategory') or ''}, {where}" + (" (remote)" if j.get("workplace") == "remote" else "")
            if keep(j.get("name", ""), loc):
                visa = {"yes": "Visa sponsorship available.", "no": "Cannot sponsor a work permit."}.get(
                    str(j.get("hasVisaSponsorship", "")).lower(), "")
                text = (f"Technologies: {', '.join(j.get('technologies') or [])}. Level: {j.get('expLevel', '')}. "
                        f"Working language: {j.get('language', '')}. {visa} "
                        f"Type: {j.get('jobType', '')}. Workplace: {j.get('workplace', '')}.")
                out.append(job(name, j.get("company"), j.get("name"), loc, f"https://{site}/jobs/{j.get('jobUrl')}",
                               j.get("activeFrom"), text, comp=pay(j.get("annualSalaryFrom"), j.get("annualSalaryTo"), currency + "/year"),
                               language=j.get("language") or "", apply=j.get("redirectJobUrl") or ""))
        return len(data), out
    return reader


def _north_america(j):
    state = (j.get("stateCategory") or "").replace("-", " ")
    return "Canada" if state == "Canada" else ", ".join(x for x in (state, "United States") if x)


def jobsch(queries, keep):
    total, out = 0, []
    for q in queries:
        for page in range(1, 11):  # the feed serves at most 20 rows a page
            d = fetch("https://www.jobs.ch/api/v1/public/search?rows=20&page=%d&query=%s" % (page, urllib.parse.quote(q)))
            docs = (d or {}).get("documents", [])
            if not docs:
                break
            total += len(docs)
            for j in docs:
                loc = (j.get("place") or "") + ", Switzerland"
                if keep(j.get("title", ""), loc):
                    links = j.get("_links") or {}
                    url = ((links.get("detail_en") or links.get("detail_de") or links.get("detail_fr") or {}).get("href")) or ""
                    langs = ", ".join(f"{x.get('language')} level {x.get('level')}" for x in j.get("language_skills") or [])
                    out.append(job("jobsch", j.get("company_name"), j.get("title"), loc, url, j.get("publication_date"),
                                   clean(j.get("preview")) + (f" Languages asked: {langs}." if langs else "")))
            if page >= (d.get("num_pages") or 1):
                break
    return total, out


def platsbanken(queries, keep):
    total, out = 0, []
    for q in queries:
        for offset in (0, 100, 200):
            d = fetch("https://jobsearch.api.jobtechdev.se/search?limit=100&offset=%d&q=%s" % (offset, urllib.parse.quote(q)))
            found = (d or {}).get("hits", [])
            if not found:
                break
            total += len(found)
            for j in found:
                w = j.get("workplace_address") or {}
                loc = ", ".join(x for x in (w.get("municipality"), w.get("region"), "Sweden") if x)
                if keep(j.get("headline", ""), loc):
                    out.append(job("platsbanken", (j.get("employer") or {}).get("name"), j.get("headline"), loc, j.get("webpage_url"),
                                   j.get("publication_date"), clean((j.get("description") or {}).get("text")),
                                   apply=(j.get("application_details") or {}).get("url") or ""))
            if len(found) < 100:
                break
    return total, out


def duunitori(queries, keep):
    total, out = 0, []
    for q in queries:
        url = "https://duunitori.fi/api/v1/jobentries?format=json&search=" + urllib.parse.quote(q)
        for _ in range(5):
            d = fetch(url)
            found = (d or {}).get("results", [])
            if not found:
                break
            total += len(found)
            for j in found:
                loc = (j.get("municipality_name") or "") + ", Finland"
                if keep(j.get("heading", ""), loc):
                    out.append(job("duunitori", j.get("company_name"), j.get("heading"), loc,
                                   f"https://duunitori.fi/tyopaikat/tyo/{j.get('slug')}", j.get("date_posted"), clean(j.get("descr"))))
            url = d.get("next")
            if not url:
                break
    return total, out


def mycareersfuture(queries, keep):
    total, out = 0, []
    for q in queries:
        for page in range(3):
            d = fetch("https://api.mycareersfuture.gov.sg/v2/jobs?limit=100&page=%d&search=%s" % (page, urllib.parse.quote(q)))
            found = (d or {}).get("results", [])
            if not found:
                break
            total += len(found)
            for j in found:
                if keep(j.get("title", ""), "Singapore"):
                    sal, meta = j.get("salary") or {}, j.get("metadata") or {}
                    kinds = ", ".join(x.get("employmentType", "") for x in j.get("employmentTypes") or [])
                    text = clean(j.get("description")) + f" Minimum years of experience: {j.get('minimumYearsExperience')}. Type: {kinds}."
                    out.append(job("mycareersfuture", (j.get("postedCompany") or {}).get("name"), j.get("title"), "Singapore",
                                   meta.get("jobDetailsUrl"), meta.get("newPostingDate"), text,
                                   comp=pay(sal.get("minimum"), sal.get("maximum"), "SGD/month")))
            if len(found) < 100:
                break
    return total, out


def remotive(queries, keep):
    total, out = 0, []
    for q in queries:
        d = fetch("https://remotive.com/api/remote-jobs?search=" + urllib.parse.quote(q))
        found = (d or {}).get("jobs", [])
        total += len(found)
        for j in found:
            loc = (j.get("candidate_required_location") or "Worldwide") + " (remote)"
            if keep(j.get("title", ""), loc):
                out.append(job("remotive", j.get("company_name"), j.get("title"), loc, j.get("url"), j.get("publication_date"),
                               clean(j.get("description")), comp=j.get("salary") or ""))
    return total, out


def remoteok(queries, keep):
    d = fetch("https://remoteok.com/api")
    data = [j for j in d if isinstance(j, dict) and j.get("position")] if isinstance(d, list) else []
    out = []
    for j in data:
        loc = (j.get("location") or "Worldwide") + " (remote)"
        if keep(j.get("position", ""), loc):
            out.append(job("remoteok", j.get("company"), j.get("position"), loc, j.get("url"), j.get("date"),
                           clean(j.get("description")) + " " + " ".join(j.get("tags") or []),
                           comp=pay(j.get("salary_min"), j.get("salary_max"), "USD/year")))
    return len(data), out


def jobicy(queries, keep):
    total, out = 0, []
    for q in queries or [""]:
        d = fetch("https://jobicy.com/api/v2/remote-jobs?count=100" + ("&tag=" + urllib.parse.quote(q) if q else ""))
        found = (d or {}).get("jobs", [])
        total += len(found)
        for j in found:
            loc = (j.get("jobGeo") or "Worldwide") + " (remote)"
            if keep(j.get("jobTitle", ""), loc):
                out.append(job("jobicy", j.get("companyName"), j.get("jobTitle"), loc, j.get("url"), j.get("pubDate"),
                               clean(j.get("jobDescription") or j.get("jobExcerpt")),
                               comp=pay(j.get("salaryMin"), j.get("salaryMax"), f"{j.get('salaryCurrency') or ''}/{j.get('salaryPeriod') or 'year'}")))
    return total, out


def himalayas(queries, keep):
    total, out = 0, []
    for q in queries:
        for offset in range(0, 100, 20):  # the feed serves 20 rows a page
            d = fetch("https://himalayas.app/jobs/api/search?limit=20&offset=%d&q=%s" % (offset, urllib.parse.quote(q)))
            found = (d or {}).get("jobs", [])
            if not found:
                break
            total += len(found)
            for j in found:
                loc = (", ".join(j.get("locationRestrictions") or []) or "Worldwide") + " (remote)"
                if keep(j.get("title", ""), loc):
                    out.append(job("himalayas", j.get("companyName"), j.get("title"), loc, j.get("guid") or j.get("applicationLink"),
                                   j.get("pubDate"), clean(j.get("description") or j.get("excerpt")),
                                   comp=pay(j.get("minSalary"), j.get("maxSalary"), f"{j.get('currency') or ''}/{j.get('salaryPeriod') or 'year'}")))
    return total, out


def workingnomads(queries, keep):
    d = fetch("https://www.workingnomads.com/api/exposed_jobs/")
    data = d if isinstance(d, list) else []
    out = []
    for j in data:
        loc = (j.get("location") or "Worldwide") + " (remote)"
        if keep(j.get("title", ""), loc):
            out.append(job("workingnomads", j.get("company_name"), j.get("title"), loc, j.get("url"), j.get("pub_date"),
                           clean(j.get("description")) + " " + (j.get("tags") or "")))
    return len(data), out


def instahyre(queries, keep):
    total, out = 0, []
    for q in queries or [""]:
        for offset in range(0, 100, 20):  # the feed serves 20 rows a page
            d = fetch("https://www.instahyre.com/api/v1/job_search?company_size=0&isLandingPage=true&job_type=0&offset=%d%s"
                      % (offset, "&skills=" + urllib.parse.quote(q) if q else ""))
            found = (d or {}).get("objects", [])
            if not found:
                break
            total += len(found)
            for j in found:
                emp = j.get("employer") or {}
                loc = (j.get("locations") or "") + ", India"
                if keep(j.get("title", ""), loc):
                    text = f"Skills: {', '.join(j.get('keywords') or [])}. {clean(emp.get('instahyre_note'))} {clean(emp.get('company_tagline'))}"
                    out.append(job("instahyre", emp.get("company_name"), j.get("title"), loc, j.get("public_url"), "", text))
    return total, out


COUNTRY_NAMES = {"AT": "Austria", "BE": "Belgium", "CH": "Switzerland", "CZ": "Czechia", "DE": "Germany", "DK": "Denmark",
                 "ES": "Spain", "FI": "Finland", "FR": "France", "GB": "United Kingdom", "IE": "Ireland", "IT": "Italy",
                 "LU": "Luxembourg", "NL": "Netherlands", "NO": "Norway", "PL": "Poland", "PT": "Portugal", "SE": "Sweden",
                 "US": "United States", "BR": "Brazil", "CA": "Canada"}


def landingjobs(queries, keep):
    total, out = 0, []
    for offset in range(0, 500, 50):
        d = fetch(f"https://landing.jobs/api/v1/jobs?limit=50&offset={offset}")
        found = d if isinstance(d, list) else []
        if not found:
            break
        total += len(found)
        for j in found:
            loc = "; ".join(f"{x.get('city') or ''}, {COUNTRY_NAMES.get(x.get('country_code'), x.get('country_code') or '')}"
                            for x in j.get("locations") or []) + (" (remote)" if j.get("remote") else "")
            if keep(j.get("title", ""), loc):
                text = " ".join(clean(j.get(k)) for k in ("role_description", "main_requirements", "nice_to_have", "perks"))
                text += " " + ", ".join(j.get("tags") or []) + (" Relocation support paid by the employer." if j.get("relocation_paid") else "")
                out.append(job("landingjobs", "", j.get("title"), loc, j.get("url"), j.get("published_at"), text,
                               comp=pay(j.get("gross_salary_low"), j.get("gross_salary_high"), f"{j.get('currency_code') or ''}/year")))
        if len(found) < 50:
            break
    for j in out:  # the company is only in the address: landing.jobs/at/{company}/{role}
        m = re.search(r"/at/([^/]+)/", j["url"])
        j["company"] = m.group(1) if m else ""
    return total, out


def hasjob(queries, keep):
    b = fetch("https://hasjob.co/feed", raw=True)
    try:
        entries = ET.fromstring(b).findall("{http://www.w3.org/2005/Atom}entry") if b else []
    except ET.ParseError:
        entries = []
    out = []
    for e in entries:
        ns = "{http://www.w3.org/2005/Atom}"
        title, content = e.findtext(ns + "title") or "", e.findtext(ns + "content") or ""
        loc = (e.findtext(ns + "location") or "") + ", India"
        if keep(title, loc):
            company = re.search(r"<strong>(?:<a[^>]*>)?([^<]+)", content)
            link = e.find(ns + "link")
            out.append(job("hasjob", company.group(1).strip() if company else "", title, loc,
                           link.get("href") if link is not None else "", e.findtext(ns + "published"), clean(content)))
    return len(entries), out


PORTALS = {
    # Germany, Switzerland, United Kingdom, Netherlands, North America: the DevJobs family
    "germantechjobs": _devjobs("germantechjobs.de", "germantechjobs", "Germany", "EUR"),
    "swissdevjobs": _devjobs("swissdevjobs.ch", "swissdevjobs", "Switzerland", "CHF"),
    "devitjobsuk": _devjobs("devitjobs.uk", "devitjobsuk", "United Kingdom", "GBP"),
    "devitjobsnl": _devjobs("devitjobs.nl", "devitjobsnl", "Netherlands", "EUR"),
    "devitjobsus": _devjobs("devitjobs.us", "devitjobsus", _north_america, "USD"),
    # single-country boards
    "arbeitnow": arbeitnow, "jobsch": jobsch, "platsbanken": platsbanken, "duunitori": duunitori,
    "mycareersfuture": mycareersfuture, "instahyre": instahyre, "hasjob": hasjob,
    # several countries, and remote roles
    "landingjobs": landingjobs, "remotive": remotive, "remoteok": remoteok, "jobicy": jobicy,
    "himalayas": himalayas, "workingnomads": workingnomads,
}
NEEDS_QUERY = {"jobsch", "platsbanken", "duunitori", "mycareersfuture", "remotive", "himalayas"}


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

    slugs = sorted(set(cfg.get("boards") or []))
    hits, boards = [], {}
    with ThreadPoolExecutor(16) as ex:
        for slug, found, jobs in ex.map(scan, slugs):
            if found:
                boards[slug] = found
            hits += jobs
    company_roles = len(hits)

    # job portals with an open feed
    queries = [q for q in cfg.get("queries") or [] if q.strip()]
    english_only = bool(cfg.get("only_english"))
    portal_report = []
    for name in cfg.get("portals") or []:
        if name not in PORTALS:
            portal_report.append(f"{name}(unknown portal; known: {', '.join(sorted(PORTALS))})")
            continue
        if name in NEEDS_QUERY and not queries:
            portal_report.append(f"{name}(skipped: add search terms under \"queries\")")
            continue
        try:
            total, jobs = PORTALS[name](queries, keep)
        except Exception:
            total, jobs = 0, []
        if english_only:
            jobs = [j for j in jobs if (j.get("language") or "").lower() == "english" or (not j.get("language") and looks_english(j["text"]))]
        hits += jobs
        portal_report.append(f"{name}({total} read, {len(jobs)} kept)")

    # the same role can come from several sources and searches: keep the first copy
    seen, unique = set(), []
    for j in hits:
        key = j["url"] or (j["company"].lower(), j["title"].lower(), j["location"].lower())
        if key not in seen:
            seen.add(key)
            unique.append(j)
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(unique, f, ensure_ascii=False, indent=1)
    if slugs:
        print(f"boards found: {len(boards)} of {len(slugs)} names; matching roles: {company_roles}")
        print("boards:", ", ".join(f"{s}({'/'.join(f'{k}:{v}' for k, v in found.items())})" for s, found in sorted(boards.items())))
        missing = [s for s in slugs if s not in boards]
        if missing:
            print("no board for:", ", ".join(missing))
    if portal_report:
        print("portals:", ", ".join(portal_report))
    print(f"total roles written: {len(unique)}")


if __name__ == "__main__":
    main()
