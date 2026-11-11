# iamgroot

IamGroot is your personal job hunter in your field. Answer a few questions and hand over your existing resume; it prepares an ATS-friendly resume, finds roles that fit, applies on your behalf, and learns from your answers and feedback to find better matches.

It runs inside [Claude Code](https://claude.com/claude-code) with the Claude in Chrome extension, and works for any profile, field and country: nothing about a candidate is stored in this repository.

## How it works

1. **Onboard.** The agent reads your resume, asks the questions every application form asks (address, salary, start date, work authorization, opt-ins and so on) and writes them to `profile/profile.md`.
2. **Find.** `scripts/discover_jobs.py` scans public job boards for the companies and locations in `profile/search.json`; `scripts/review_jobs.py` flags seniority, sponsorship, language and clearance requirements.
3. **Apply.** The agent fills each form from the profile, verifies it, submits it and confirms the success page. The `apply-jobs` workflow runs several applications in parallel browser tabs.
4. **Track.** Every role, including parked and skipped ones, is recorded in `profile/applications.csv`.
5. **Learn.** New answers go into the profile; general lessons go into `LESSONS.md`.

## Layout

| Path | What it is |
| --- | --- |
| `PROMPT.md` | Agent instructions, the same for every candidate |
| `profile.example.md` | Template for the private candidate profile |
| `search.example.json` | Template for the job-search configuration |
| `LESSONS.md` | General lessons from real application runs |
| `docs/ats-playbook.md` | How to read, fill and submit forms on each applicant-tracking system |
| `scripts/` | Job discovery, review, queue building and tracker tools |
| `.claude/workflows/apply-jobs.js` | Workflow that applies to a queue of roles in parallel |
| `profile/` | **Private and git-ignored:** your profile, resumes, job lists and tracker |

## Quick start

```bash
mkdir -p profile/jobs
cp profile.example.md profile/profile.md      # or let the agent fill it in with you
cp search.example.json profile/search.json    # companies, titles and locations to search

python3 scripts/discover_jobs.py --config profile/search.json --out profile/jobs/hits.json
python3 scripts/review_jobs.py profile/jobs/hits.json --languages German
python3 scripts/review_jobs.py profile/jobs/hits.json --show 3 17
python3 scripts/build_queue.py profile/jobs/hits.json profile/jobs/queue.json --batch A=3,17 --tracker profile/applications.csv
```

Then, in Claude Code: "Follow PROMPT.md and run the apply-jobs workflow on the queue." Afterwards:

```bash
python3 scripts/record_results.py profile/jobs/results profile/applications.csv --date YYYY-MM-DD
```

## What it will not do

- Invent experience, skills, opinions or answers. Questions only you can answer are parked and brought to you.
- Solve CAPTCHAs, create accounts or enter passwords.
- Apply to roles outside the limits in your profile to raise the count.
- Commit anything personal: `profile/` and all documents are ignored by git.
