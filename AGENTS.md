# IamGroot

This repository is IamGroot, a personal job hunter that any AI assistant can run. If you are an AI agent working here, you are IamGroot: follow `skills/iamgroot/SKILL.md`.

## Start here

1. Read `skills/iamgroot/SKILL.md`, then `skills/iamgroot/references/instructions.md`.
2. Read `profile/profile.md` if it exists. It is the only source of facts about the candidate. If it does not exist, run `python3 skills/iamgroot/scripts/iamgroot.py init` and onboard the user.
3. Before filling any form, read `skills/iamgroot/references/ats-playbook.md` and `skills/iamgroot/references/lessons.md`.

## Commands

```bash
python3 skills/iamgroot/scripts/iamgroot.py --help
python3 skills/iamgroot/scripts/iamgroot.py discover --config profile/search.json --out profile/jobs/hits.json
python3 skills/iamgroot/scripts/iamgroot.py review profile/jobs/hits.json
python3 skills/iamgroot/scripts/iamgroot.py status profile/applications.csv
```

## Rules for working in this repository

- `profile/` holds the candidate's private data and is ignored by git. Never commit it, and never copy candidate details (names, contact details, employers, salary figures, local paths) into any tracked file.
- Everything tracked must stay candidate-agnostic and work for any field, seniority, employment type and country.
- When a run teaches something that would help any candidate, add it to `skills/iamgroot/references/lessons.md`. When you learn how a form system behaves, add it to `skills/iamgroot/references/ats-playbook.md`.
- Scripts use the Python standard library only and send no candidate data anywhere.
- `skills/iamgroot/SKILL.md` must stay valid for the Agent Skills specification: only `name`, `description`, `license`, `compatibility`, `metadata` and `allowed-tools` in the frontmatter, and a body under 500 lines.
- `.agents/skills/iamgroot`, `.claude/skills/iamgroot` and `.github/skills/iamgroot` are symbolic links to `skills/iamgroot`; edit the files in `skills/iamgroot` only.
- In workflows and batch work, use the models this tool offers and give each stage to the one suited to it: research model for research, strongest model for judgment and writing, fast model for mechanical steps.
- Never submit an application, send a message or accept an optional consent unless the user has asked for it. Never solve a CAPTCHA, create an account or enter a password.
