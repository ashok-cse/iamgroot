#!/usr/bin/env python3
"""Merge the per-batch result files written by the apply-jobs workflow into the application tracker.

    python3 scripts/record_results.py profile/jobs/results profile/applications.csv --date 2026-01-31

Each agent appends one JSON line per job to results/<batch>.jsonl. A role whose Job URL is already in
the tracker is updated only when the new status is "submitted" and the old one was not.
"""
import argparse
import csv
import glob
import json
import os

COLS = ["Company", "Position", "Location", "Country", "Job URL", "Application URL", "Date Applied",
        "Application Method", "Recruiter/HR Contact", "Email Address", "Salary Info", "Start Date Info",
        "Visa Sponsorship Info", "Status", "Notes", "Custom Message Sent"]
STATUS = {
    "submitted": "Submitted - confirmation shown",
    "blocked": "NOT SUBMITTED - needs your input",
    "skipped": "Not applied - skipped",
    "failed": "NOT SUBMITTED - technical failure",
}


def row_from(r, date):
    status = r.get("status", "")
    notes = r.get("notes", "")
    if r.get("blocking_question"):
        notes = (notes + " " if notes else "") + "Question: " + r["blocking_question"]
    return {
        "Company": r.get("company", ""), "Position": r.get("position", ""), "Location": r.get("location", ""),
        "Country": r.get("country", ""), "Job URL": r.get("job_url", ""),
        "Application URL": r.get("application_url", ""), "Date Applied": date if status == "submitted" else "",
        "Application Method": r.get("application_method", ""), "Salary Info": r.get("salary_info", ""),
        "Start Date Info": r.get("start_date_info", ""), "Visa Sponsorship Info": r.get("visa_info", ""),
        "Status": STATUS.get(status, status), "Notes": notes, "Custom Message Sent": r.get("custom_message_sent", ""),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results_dir")
    ap.add_argument("tracker")
    ap.add_argument("--date", required=True, help="date to record for submitted applications (YYYY-MM-DD)")
    a = ap.parse_args()
    rows = []
    if os.path.exists(a.tracker):
        with open(a.tracker, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
    by_url = {r["Job URL"]: r for r in rows}
    added = updated = 0
    counts = {}
    for path in sorted(glob.glob(os.path.join(a.results_dir, "*.jsonl"))):
        for line in open(path, encoding="utf-8"):
            line = line.strip()
            if not line:
                continue
            r = json.loads(line)
            counts[r.get("status", "?")] = counts.get(r.get("status", "?"), 0) + 1
            new = row_from(r, a.date)
            old = by_url.get(new["Job URL"])
            if old is None:
                rows.append({c: new.get(c, "") for c in COLS})
                by_url[new["Job URL"]] = rows[-1]
                added += 1
            elif r.get("status") == "submitted" and not old["Status"].startswith("Submitted"):
                old.update(new)
                updated += 1
    with open(a.tracker, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"results read: {counts}; tracker rows added: {added}, updated: {updated}, total: {len(rows)}")


if __name__ == "__main__":
    main()
