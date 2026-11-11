#!/usr/bin/env python3
"""iamgroot: one entry point for the job-hunter tools.

    python3 iamgroot.py init [--dir profile]          create the private profile folder from the templates
    python3 iamgroot.py country "Name" [--dir profile]  create the private profile for one target country
    python3 iamgroot.py resume --data profile/resume.json   build ATS-friendly resume PDFs with LaTeX
    python3 iamgroot.py discover --config ... --out ...   scan public job boards for matching roles
    python3 iamgroot.py review HITS [--show N ...]    list roles with requirement flags, or show details
    python3 iamgroot.py questions BOARD JOB_ID        print a Greenhouse application form
    python3 iamgroot.py queue HITS OUT --batch A=1,2  build a batched queue of chosen roles
    python3 iamgroot.py track TRACKER '{json row}'    add one application to the tracker
    python3 iamgroot.py update TRACKER URL '{json}'   change fields of a tracked application
    python3 iamgroot.py record RESULTS_DIR TRACKER --date YYYY-MM-DD   merge workflow results into the tracker
    python3 iamgroot.py status [TRACKER]              count tracked applications by status and country

Add --help after any command for its own options. Standard library only; no candidate data leaves the machine.
"""
import collections
import csv
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REFERENCES = os.path.join(os.path.dirname(HERE), "references")
COMMANDS = {
    "discover": "discover_jobs.py",
    "review": "review_jobs.py",
    "questions": "gh_questions.py",
    "queue": "build_queue.py",
    "track": "track.py",
    "update": "update_tracker.py",
    "record": "record_results.py",
    "resume": "build_resume.py",
}
TRACKER_COLUMNS = ["Company", "Position", "Location", "Country", "Job URL", "Application URL", "Date Applied",
                   "Application Method", "Recruiter/HR Contact", "Email Address", "Salary Info", "Start Date Info",
                   "Visa Sponsorship Info", "Status", "Notes", "Custom Message Sent"]


def init(argv):
    target = argv[argv.index("--dir") + 1] if "--dir" in argv else "profile"
    os.makedirs(os.path.join(target, "jobs", "results"), exist_ok=True)
    os.makedirs(os.path.join(target, "resume"), exist_ok=True)
    for template, name in (("profile.example.md", "profile.md"), ("search.example.json", "search.json"),
                           ("resume.example.json", "resume.json")):
        dest = os.path.join(target, name)
        if os.path.exists(dest):
            print("kept   ", dest)
        else:
            shutil.copyfile(os.path.join(REFERENCES, template), dest)
            print("created", dest)
    tracker = os.path.join(target, "applications.csv")
    if not os.path.exists(tracker):
        with open(tracker, "w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(TRACKER_COLUMNS)
        print("created", tracker)
    # keep the private folder out of version control
    if os.path.isdir(".git"):
        entry = target.rstrip("/") + "/"
        lines = open(".gitignore", encoding="utf-8").read().splitlines() if os.path.exists(".gitignore") else []
        if entry not in lines:
            with open(".gitignore", "a", encoding="utf-8") as f:
                f.write(("\n" if lines and lines[-1] else "") + entry + "\n")
            print("added  ", entry, "to .gitignore")
    print(f"Next: fill in {target}/profile.md, {target}/resume.json and {target}/search.json (your assistant can do this with you).")


def country(argv):
    names = [a for i, a in enumerate(argv) if not a.startswith("--") and (i == 0 or argv[i - 1] != "--dir")]
    if not names:
        sys.exit('usage: iamgroot.py country "Country name" [--dir profile]')
    target = argv[argv.index("--dir") + 1] if "--dir" in argv else "profile"
    folder = os.path.join(target, "countries")
    os.makedirs(folder, exist_ok=True)
    template = open(os.path.join(REFERENCES, "country.example.md"), encoding="utf-8").read()
    for name in names:
        slug = "-".join("".join(c if c.isalnum() else " " for c in name.lower()).split())
        dest = os.path.join(folder, slug + ".md")
        if os.path.exists(dest):
            print("kept   ", dest)
            continue
        with open(dest, "w", encoding="utf-8") as f:
            f.write(template.replace("{{COUNTRY}}", name).replace(" (template)", "", 1))
        print("created", dest)
    print("Next: fill each file from references/countries.md and the candidate's answers.")


def status(argv):
    path = argv[0] if argv else os.path.join("profile", "applications.csv")
    if not os.path.exists(path):
        sys.exit(f"no tracker at {path}; run: iamgroot.py init")
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    by_status = collections.Counter((r.get("Status") or "").split(" - ")[0] or "(no status)" for r in rows)
    submitted = [r for r in rows if (r.get("Status") or "").lower().startswith("submitted")]
    by_country = collections.Counter(r.get("Country") or "(unknown)" for r in submitted)
    print(f"{len(rows)} roles tracked, {len(submitted)} submitted")
    for name, n in by_status.most_common():
        print(f"  {n:3d}  {name}")
    if submitted:
        print("submitted by country:", ", ".join(f"{c} {n}" for c, n in by_country.most_common()))


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(__doc__.strip())
        return
    command, rest = argv[0], argv[1:]
    if command == "init":
        return init(rest)
    if command == "country":
        return country(rest)
    if command == "status":
        return status(rest)
    if command not in COMMANDS:
        sys.exit(f"unknown command: {command}\n\n{__doc__.strip()}")
    sys.exit(subprocess.run([sys.executable, os.path.join(HERE, COMMANDS[command]), *rest]).returncode)


if __name__ == "__main__":
    main()
