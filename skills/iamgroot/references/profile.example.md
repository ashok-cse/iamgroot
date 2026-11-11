# Candidate profile (template)

Copy this file to `profile/profile.md` and fill it in. `profile/` is ignored by git: nothing in it is ever committed.
This file is the single source of truth for the candidate. Agents may only state what is written here or in the resume.

## Identity and contact

- **Salutation:**
- **First name:**
- **Last name:**
- **Legal name on forms with a middle-name field:** first …, middle …, last …
- **Preferred name:**
- **Email:**
- **Phone:** (country code and national number)
- **Address:** street, postcode, city, country
- **Current location:**
- **LinkedIn:**
- **GitHub / portfolio / work samples:**
- **Languages:** language and level (A1–C2)

## Availability

- **Employment type wanted:** full-time / part-time / contract / internship / working student
- **Earliest start date:**
- **Notice period wording:** the exact sentence to use
- **Work arrangement:** on-site / hybrid / remote, and the maximum office days
- **Relocation:** where the candidate would move to

## Target markets, salary and resume per market

| Market | Resume file (absolute path) | Default salary | Range when asked |
| --- | --- | --- | --- |
| | | | |

- Rule when a posting publishes a salary range:
- Target cities and remote policy:
- Resume source file and how to rebuild the PDFs:

Each target country also gets its own file in `profile/countries/` (create it with `iamgroot.py country "<Country>"`); it holds the answers, pay figures and resume for that country.

## Work authorization (one block per country)

- **Country:**
  - "Are you authorized to work here?" (Yes/No):
  - "Do you require visa sponsorship?" (Yes/No):
  - Option to choose in a list of permit types:
  - Sentence to use in free text:
- Nationality or citizenship: record it only if the candidate wants it stated on forms.

## Target roles

- Roles to prioritize, in order:
- Seniority band (derived from the resume):
- Do not apply to:
- Skills supported by the resume:
- Skills that are not on the resume (never claim):

## Experience (facts only; from the resume)

One line per role: title, employer, place, dates, stack, measurable results.
Projects, education and certifications below that.

## Standing form answers (with the date the candidate confirmed them)

- Directorships, board memberships or ownership stakes in other businesses:
- Public official (self or close family) in recent years:
- Keeping the application on file / talent pool:
- Newsletters, marketing emails, WhatsApp or SMS updates:
- Interview recording or AI note-taking, when optional:
- Diversity, gender, pronoun, age and ethnicity questions:
- Privacy or data consent that is required to submit:
- Previously employed by or applied to the company:
- Office attendance and relocation questions:
- Language levels on the A1–C2 scale:
- "How did you hear about us?":
- Field-specific screening answers the candidate has given (tools used, self-assessed levels, the project to describe):

## Questions the candidate has not answered

List them here. An agent that meets one of these on a required field stops and reports the question.
