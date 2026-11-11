@AGENTS.md

## Claude Code specifics

- Browser work uses the Claude in Chrome extension. Fill and submit forms from the main session only: the permission system refuses form submission, and often form filling, by sub-agents.
- To prepare many applications at once, build a queue (`iamgroot.py queue`) and run the saved `prepare-applications` workflow. Its agents read each posting and form and return an answer plan per role; the main session then fills, verifies and submits.
- The same skill is available as `/iamgroot` through `.claude/skills/iamgroot`.
