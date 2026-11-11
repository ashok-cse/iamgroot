# Using IamGroot from different AI assistants

IamGroot is three things, so that any assistant can use at least one of them:

1. **Instructions**: `AGENTS.md` at the repository root, which most coding agents read automatically.
2. **A skill**: the `skills/iamgroot/` folder in the open Agent Skills format (`SKILL.md` plus `references/` and `scripts/`).
3. **A tool**: `scripts/iamgroot.py`, a command-line program that needs only Python.

The table reflects each vendor's documentation as checked on 11 November 2026. These products change quickly; where a row says "unverified", check the vendor's current documentation.

## Install

Any agent supported by the `skills` installer:

```bash
npx skills add ashok-cse/iamgroot
```

Or clone the repository and work inside it: `AGENTS.md` and the skill folders are already in the places agents look. To install by hand, copy `skills/iamgroot/` into the skills directory your agent reads (see the table).

Chat apps without a file system: zip `skills/iamgroot/` and upload it as a skill where the app supports skills, or add `SKILL.md` and the files in `references/` to a project as knowledge and paste `SKILL.md` as the project instructions.

## What each assistant reads

| Assistant | Instructions it reads | Skill directories | Runs the scripts | Fills web forms |
| --- | --- | --- | --- | --- |
| Claude Code | `CLAUDE.md` (imports `AGENTS.md`) | `.claude/skills/`, `~/.claude/skills/` | Yes | Yes, with the Claude in Chrome extension |
| Claude.ai chat | Project instructions and files | Upload the zipped skill under Skills (needs code execution) | In its sandbox only | No: chat mode |
| OpenAI Codex (CLI, IDE, desktop) | `AGENTS.md` (32 KiB combined limit) | `.agents/skills/`, `~/.agents/skills/` | Yes | Desktop app, through its browser plugins |
| ChatGPT (chat, projects, GPTs) | Project or GPT instructions and files | Skills in the desktop app; upload on web is unverified | Limited | Desktop app browser plugins; otherwise chat mode |
| Gemini CLI | `GEMINI.md`; `AGENTS.md` through `.gemini/settings.json` (included here) | `.gemini/skills/`, `.agents/skills/` | Yes | Built-in browser agent, off by default |
| Google Antigravity | `AGENTS.md` or `GEMINI.md` (truncated at 24,000 bytes) | `.agents/skills/` | Unverified | Yes, browser subagent |
| Gemini app | Uploaded files or a skill folder | Upload `SKILL.md` folders on web or Mac | No | No: chat mode |
| Cursor | `AGENTS.md`, `.cursor/rules/` | `.agents/skills/`, `.cursor/skills/`, `.claude/skills/` | Yes | Yes, built-in browser tool |
| GitHub Copilot (cloud agent, CLI, VS Code) | `AGENTS.md`, `.github/copilot-instructions.md` | `.github/skills/`, `.agents/skills/`, `.claude/skills/` | Yes | Playwright MCP (cloud agent), browser tools (VS Code) |
| Devin and Devin Desktop (formerly Windsurf) | `AGENTS.md` (first 16 KiB per file) | `.agents/skills/`, `.devin/skills/`, `.claude/skills/` | Yes | Devin cloud has its own browser; Desktop unverified |
| Cline | `.clinerules/`, auto-detects `AGENTS.md` | `.cline/skills/`, `.claude/skills/` | Yes | Through an MCP browser server |
| OpenCode | `AGENTS.md` | `.opencode/skills/`, `.agents/skills/`, `.claude/skills/` | Yes | Desktop app browser tools, or MCP |
| Amp | `AGENTS.md` | `.agents/skills/`, `.claude/skills/` | Yes | Through an MCP browser server |
| Goose | `AGENTS.md`, `.goosehints` | `.agents/skills/`, `.goose/skills/`, `.claude/skills/` | Yes | Computer Controller extension |
| Kiro | `AGENTS.md`, `.kiro/steering/` | `.kiro/skills/` only: copy the skill there | Yes | None documented |
| Qwen Code | `QWEN.md`, `AGENTS.md` | `.qwen/skills/`, `.agents/skills/` | Unverified | Unverified |
| Aider | Nothing automatic; `.aider.conf.yml` here loads `AGENTS.md` | No skills support | `/run` | No |
| Roo Code | `AGENTS.md`, `.roo/rules/` | `.roo/skills/`, `.agents/skills/` | Unverified | Unverified (project archived in May 2026) |

Jules, Factory, Zed, Warp, Junie, Kilo Code and Augment also read `AGENTS.md`.

## Which mode you get

- **Shell and browser:** the full loop, including submitting forms.
- **Shell only:** discovery, review, tracking and prepared answers; you submit.
- **Chat only:** onboarding, fit checks, answers and cover notes; you submit and report back.

An assistant without a browser can gain one through an MCP browser server such as Playwright MCP. Each assistant keeps its MCP configuration in its own file, so add the server there instead of in this repository.

## Notes

- `.agents/skills/iamgroot`, `.claude/skills/iamgroot` and `.github/skills/iamgroot` in this repository are symbolic links to `skills/iamgroot`. On Windows, or if an assistant does not follow links, copy the folder instead.
- Skill uploads to chat apps reject frontmatter keys outside the Agent Skills specification; `SKILL.md` here uses only `name`, `description` and `compatibility`.
- Sources: agents.md, agentskills.io/specification, and the customization pages of each product's documentation.
