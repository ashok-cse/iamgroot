# IamGroot

**English** · [中文](docs/README.zh.md) · [हिन्दी](docs/README.hi.md) · [Español](docs/README.es.md) · [Français](docs/README.fr.md) · [العربية](docs/README.ar.md) · [বাংলা](docs/README.bn.md) · [Português](docs/README.pt.md) · [Русский](docs/README.ru.md) · [اردو](docs/README.ur.md) · [Bahasa Indonesia](docs/README.id.md) · [Deutsch](docs/README.de.md) · [日本語](docs/README.ja.md) · [मराठी](docs/README.mr.md) · [Tiếng Việt](docs/README.vi.md)

**Your personal job hunter.**

Looking for a job takes a lot of time. IamGroot does the slow, boring parts for you. It is a helper that works inside AI chat tools such as Claude Code, Codex, ChatGPT, Gemini and Cursor. It works for any kind of job, in any country.

## What it does

1. **Gets to know you.** It reads your resume and asks a few questions, such as where you want to work and when you can start.
2. **Builds a clean resume.** It makes a one-page resume that hiring software can read without mistakes.
3. **Finds jobs.** It looks through the job pages of many companies and keeps the jobs that fit you.
4. **Applies for you.** It fills in the application forms with your details and sends them. If your AI tool cannot use a web browser, it writes the answers and you send them.
5. **Keeps a list.** Every job goes into one list, so you always know where you applied and what happened.
6. **Learns.** It remembers your answers, so it does not ask the same question twice.

## How to start

You need an AI chat tool. To use every feature you also need Python, a free program, on your computer.

1. Get IamGroot. Run this command, or download this project and open it in your AI tool:

   ```bash
   npx skills add ashok-cse/iamgroot
   ```

2. Tell your AI tool: **"You are IamGroot. Onboard me."**
3. Give it your resume and answer its questions.
4. Ask it to find jobs and apply.

## Your information stays with you

Everything about you is saved in a folder named `profile/` on your own computer. It is never added to this project and never shared.

## What it will never do

- Make up skills, jobs or answers. When only you know the answer, it asks you.
- Create accounts, type passwords, or get past "I am not a robot" checks.
- Apply to jobs that do not fit you just to reach a bigger number.

## More details

| If you want to know | Read |
| --- | --- |
| How it works step by step | [`skills/iamgroot/SKILL.md`](skills/iamgroot/SKILL.md) |
| The full rules it follows | [`skills/iamgroot/references/instructions.md`](skills/iamgroot/references/instructions.md) |
| Which AI tools it works with | [`skills/iamgroot/references/agents.md`](skills/iamgroot/references/agents.md) |
| What it has learned from real job applications | [`skills/iamgroot/references/lessons.md`](skills/iamgroot/references/lessons.md) |
| How it fills in forms on job websites | [`skills/iamgroot/references/ats-playbook.md`](skills/iamgroot/references/ats-playbook.md) |
| The commands | `python3 skills/iamgroot/scripts/iamgroot.py --help` |
