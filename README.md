# iamgroot

IamGroot is your personal job hunter in your field. Answer a few questions and hand over your existing resume; it builds an ATS-friendly resume, finds roles that fit, applies on your behalf, and learns from your answers and feedback to find better matches.

It is a chat you can have with any AI assistant: Claude Code, Codex, ChatGPT, Gemini, Cursor, Copilot and others. It works for any profile, field, employment type and country, and nothing about a candidate is stored in this repository.

## Three ways to use it

| As | What | For |
| --- | --- | --- |
| Instructions | `AGENTS.md` | Coding agents that read project instructions automatically |
| A skill | `skills/iamgroot/` (`SKILL.md`, references, scripts, LaTeX template) | Any assistant that supports Agent Skills, including chat apps |
| A tool | `skills/iamgroot/scripts/iamgroot.py` | Anything that can run a command; Python standard library only |

Install the skill into your assistant:

```bash
npx skills add ashok-cse/iamgroot
```

or clone this repository and open it in your assistant, then say: **"You are IamGroot. Onboard me."**

`skills/iamgroot/references/agents.md` lists what each assistant reads and what it can do. Assistants with a shell and a browser run the whole loop; chat-only assistants onboard you, check fit and write your answers, and you submit.

## How it works

1. **Onboard.** The assistant reads your resume and asks what every application form asks (address, salary, start date, work authorization, opt-ins) and writes the answers to a private `profile/profile.md`.
2. **Resume.** `iamgroot.py resume` builds a one-page, parser-friendly PDF from your resume data with LaTeX, one variant per market, changing only the header and target line.
3. **Find.** `iamgroot.py discover` scans public job boards (Greenhouse, Lever, Ashby) for the companies and locations you choose; `iamgroot.py review` flags seniority, sponsorship, language and clearance requirements.
4. **Apply.** Each form is filled from your profile, verified, submitted and confirmed. Questions only you can answer are parked and brought to you.
5. **Track.** Every role, including parked and skipped ones, goes into `profile/applications.csv`.
6. **Learn.** Your answers go into the profile; general lessons go into `skills/iamgroot/references/lessons.md`.

## Quick start with the tool

```bash
alias iamgroot="python3 skills/iamgroot/scripts/iamgroot.py"

iamgroot init                                   # creates the private profile/ folder from the templates
iamgroot resume --data profile/resume.json      # needs a LaTeX engine, e.g. tectonic
iamgroot discover --config profile/search.json --out profile/jobs/hits.json
iamgroot review profile/jobs/hits.json --languages German
iamgroot review profile/jobs/hits.json --show 3 17
iamgroot questions <greenhouse-board> <job-id>  # print an application form before opening it
iamgroot status profile/applications.csv
```

## Layout

| Path | What it is |
| --- | --- |
| `AGENTS.md`, `CLAUDE.md` | Entry points that agents read automatically |
| `skills/iamgroot/SKILL.md` | The skill: the loop, the modes, the rules |
| `skills/iamgroot/references/instructions.md` | Full agent instructions, the same for every candidate |
| `skills/iamgroot/references/ats-playbook.md` | How to read, fill and submit forms on each applicant-tracking system |
| `skills/iamgroot/references/lessons.md` | General lessons from real application runs |
| `skills/iamgroot/references/agents.md` | Support and install notes for each AI assistant |
| `skills/iamgroot/assets/resume-template.tex` | The LaTeX resume layout |
| `skills/iamgroot/scripts/` | The tool and its commands |
| `.agents/skills`, `.claude/skills`, `.github/skills` | Links to the skill for the agents that look there |
| `.claude/workflows/prepare-applications.js` | Claude Code workflow that prepares many applications in parallel |
| `profile/` | **Private and git-ignored:** your profile, resume data, job lists and tracker |

## What it will not do

- Invent experience, skills, opinions or answers. Questions only you can answer are parked and brought to you.
- Solve CAPTCHAs, create accounts or enter passwords.
- Apply to roles outside the limits in your profile to raise the count.
- Commit anything personal: `profile/` and all documents are ignored by git.
