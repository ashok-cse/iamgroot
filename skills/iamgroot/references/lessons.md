# Lessons

General lessons from running real application batches. They apply to every candidate, role and country.
Add a lesson whenever a run teaches something that would change what the next run does; keep candidate-specific facts out of this file (they belong in `profile/profile.md`). Form mechanics per ATS are in `ats-playbook.md`.

## Before the first application

1. **Collect the standing answers first.** The same personal questions come back on almost every form. Ask the candidate once, up front, and store the answers in the profile: salutation, postal address, legal name split (first / middle / last), salary expectation per country, notice period wording, on-site and relocation preferences, work authorization per country (both the Yes/No answer and the free-text wording), talent-pool and marketing opt-ins, conflict-of-interest questions (directorships, public office), language levels on the A1–C2 scale, and how to answer diversity and pronoun questions.
2. **One resume per market.** A resume that states a target country or a sponsorship need for one market must not go to employers in another. Keep the resume source editable and derive each market variant from it by changing only the header line and the target statement, never the experience.
3. **Check the resume as a recruiter's parser will see it.** Extract the text of every generated PDF and read it once: dates, dashes and ligatures should survive as plain text, and the document should stay on the intended number of pages.
4. **Set the seniority band from the resume, not from the template.** Years of experience decide whether junior, mid-level or senior roles are the target; applying across the wrong band wastes the daily budget.
5. **Say the start date everywhere it can be said.** If availability is months away, most open roles will not wait. Put the date in the resume header and in every notice-period, start-date and free-text field so nobody is surprised later.

## Choosing roles

6. **Read the posting for hard filters before opening the form:** required language level, "no visa sponsorship", "existing right to work required", security clearance or citizenship, years of experience, and whether a named technology is a must-have that the resume lacks.
7. **Public job-board APIs beat browsing.** Greenhouse, Lever and Ashby expose listings as JSON, which makes it possible to scan a hundred companies in a minute and filter by title and location before spending any browser time.
8. **Respect application caps.** Many employers limit candidates to one to three applications per period, and some reject a second submission outright. Pick the single best-fitting role per company unless the posting says otherwise.
9. **A match on the main stack is enough; a missing must-have is not.** Apply when the core requirement is covered by the resume. Skip when the central requirement (a specific language, a domain, model-training experience) is absent.

## Answering questions

10. **Never answer a question the candidate has not answered.** Product opinions, "have you used our product", prior knowledge of the company, conflict-of-interest and legal questions, nationality, and self-assessments of skill level are the candidate's to give. Park the application, record the exact question, and move on; ask the parked questions in one batch.
11. **Written answers come only from the resume and the candidate's own statements.** Quote the measurable results that exist; do not add how something was measured, team sizes, or tools that are not recorded.
12. **Work-authorization questions are worded three different ways:** "are you authorized", "do you require sponsorship", and a list of permit types. Record the candidate's answer for each wording and each country, because a wrong tick filters the application out automatically.
13. **Salary fields vary in type.** Some accept only digits, some want a range from a dropdown, some are free text. When the posting publishes a range, answer inside it. Keep the currency explicit in free-text fields.
14. **Numeric dates are ambiguous.** Use the date picker when there is one; in free text write the month in words.
15. **Demographic surveys are optional far more often than they look.** Leave them blank; when a field is marked required, use the "prefer not to answer" option. Some forms then require a consent tick for processing that one answer.
16. **Consent boxes are not all the same.** Separate the consent that is needed to submit the application (accept) from optional ones: talent pool, newsletters, WhatsApp updates, interview recording. Follow the candidate's stated default for each kind.
17. **Compliance questions hide in short forms.** Conflict-of-interest, public-official and "previously employed here" questions appear on otherwise simple forms and are usually required.

## Submitting

18. **Verify, then submit, then confirm.** Check every field value in a separate step before the submit click, and treat an application as submitted only when the confirmation page or banner has been read.
19. **A silent non-submission is common.** If the form is still on screen with no message after submitting, the click was lost; scroll the button into view and click again before assuming anything else.
20. **Do not navigate away on an unconfirmed submit.** Chaining the next page load after a submit hides whether it worked and risks duplicates on the retry.
21. **Record each application the moment it is confirmed:** company, role, location, both URLs, date, what was stated for salary, start date and work authorization, every consent given, and any answer the candidate should know about.
22. **Keep parked applications in the tracker too,** with the exact question that blocked them, so they can be finished in a few minutes once the candidate answers.

## Pace

23. **A realistic rate with careful verification is roughly one application every few minutes** on forms without custom questions, and much slower on questionnaire-style forms. A target such as "100 in a day" is reached only by keeping quality rules fixed and widening the company list, not by loosening the match.
24. **Questionnaire-heavy employers are worth the candidate's own time.** Forms that ask for product critiques or long self-assessments usually belong to the best-matched companies; hand those to the candidate with the questions listed instead of skipping them silently.

## Working with helper agents and tools

25. **Submit from the session the candidate is talking to.** Permission systems treat a form submission as a real-world action and may refuse it, and even the typing of personal data, when a helper agent attempts it, because the candidate's instruction is not visible there. Use helpers for read-only preparation (fit check, reading the form, drafting every answer) and keep filling and submitting in the main session.
26. **Preparation is the part that parallelises.** Deciding fit and drafting answers for thirty roles can run side by side; filling and submitting is quick once each form has an answer plan.
27. **Some forms must be completed by the candidate personally.** A box such as "I certify that I have personally completed this application" cannot be ticked truthfully by an assistant. Hand the role to the candidate with the prepared answers.
28. **Screening self-assessments repeat across employers:** years with a specific language, on-call willingness, experience with a named domain or dataset type, and "which option best describes your level". Add each new one to the profile's standing answers the first time the candidate answers it.
29. **Listings outlive postings.** A role can stay in a job-board API after its page has closed. Open the application page before investing time in a role.
30. **Application caps are usually stated on the form** ("no more than N applications in M days"). Record the cap in the tracker and spend it on the best-fitting role.
31. **Keep the resume as data.** With the facts in one data file and the layout in a template, a new market version is a two-line change and cannot drift from the original.
32. **An assistant-neutral package travels further.** Instructions in `AGENTS.md`, the same content as an Agent Skill, and a plain command-line tool cover nearly every assistant; anything tied to one product's features stays optional.
33. **"Are you a human or an automated program?" is the candidate's to answer.** Some forms ask it outright. An assistant must not select "human" on the candidate's behalf; hand the role over with the other answers prepared.
34. **Export-control questions appear on forms of US-headquartered employers,** even for roles elsewhere: citizenship or residency of sanctioned countries, with follow-ups that are "not applicable" when the first answer is no. Record the candidate's answer once.
35. **Permit questions with three options need the accurate one, not the convenient one.** When the choices are "authorised (citizen, permanent resident)", "current authorisation needs sponsorship or renewal" and "unknown", a temporary permit holder belongs in the second, even if they answer "yes" to a plain right-to-work question.
36. **Write the public pages for a reader in a hurry.** A README in short sentences and everyday words, translated into the languages the users speak and checked by a second reader per language, does more for adoption than a detailed one.
37. **Match the model to the stage.** In batch work, research, judgment and mechanical extraction are different jobs. Use the research model for research, the strongest model for decisions and written answers, and the fast model for scanning and extraction, all from the models the user's own tool provides.
38. **Fintech and regulated employers add legal questions on a second page:** criminal record, planned side employment, and requests for degree certificates and references. Read every page of a multi-step form before filling the first.
39. **Some employers require that the candidate drafts the answers personally** and say so in a candidate AI policy. Read the policy the form links to; where it asks for the candidate's own first draft, hand the form to the candidate.
40. **Forms grow while you fill them.** A prepared answer plan covers the questions visible when the form was read. Answers can reveal new required questions (current permit, salary band). Re-read the form after each choice, answer the new questions from the profile, and stop if one is not covered.
41. **A sponsorship question means what the form says it means.** Some employers define sponsorship in the question itself, for example by naming a permit the candidate plans to arrange alone. A standing "no sponsorship needed" answer does not settle that wording: ask the candidate.
42. **Location-restricted remote roles screen on where the candidate lives now.** "Remote" postings often list the only countries they hire in and ask whether the applicant is located there. Answer truthfully, put the relocation plan in the free text, and tell the candidate the odds are low.
43. **Salary bands are picked by the stored expectation.** When the form offers ranges instead of a number, choose the band that starts at the candidate's expected figure, inside the candidate's stated range.
44. **A new country is a new profile, not a new line in a table.** The right to work, the way pay is quoted (per year or per month, with or without allowances), resume customs, language and form questions all change. Keep one private profile per country and ask its questions in one round before the first application there.
45. **Work out the permit route before searching.** Citizenship and current residence status decide which employers can hire the candidate at all: a sponsor licence in one country, a register of recognised sponsors in another, a yearly lottery or quota in a third. Search only where a route exists, and order the countries by how likely the route is to work.
46. **A residence permit in one country is not a right to work in its neighbours.** A permit issued by one EU state does not cover another, so "are you authorised to work in the EU?" on a form from a different country is answered for that country.
47. **Permit salary floors set the bottom of the salary range.** An expectation below the floor makes the candidate ineligible however good the match, so the range given on forms must start at or above it. Floors change every year and some rise with age.
48. **Use portals to find and the employer's page to apply.** Boards need accounts and repeat the same role under many addresses. Several publish open feeds that can be read without an account; check each new board for one.
49. **Official sponsor lists save applications.** Where a country publishes the employers allowed to hire from abroad, checking the employer first is quicker than learning the answer from a rejection.
50. **Timing decides before fit does.** A posting open today is meant to be filled within one to three months. An application for a start many months later is rejected for the date alone, and at many employers that rejection counts against a later application. Work out the application window from the start date before sending anything.
51. **Say the hard thing first, as a decision.** When the plan itself has a flaw, such as a start date too far away or a country with no route, a remark in passing is not enough. Stop, explain it plainly with dates and consequences, and let the candidate choose before any volume goes out.
52. **A pause is part of the search.** While the window is closed, the useful work is the kind that keeps: the profile, the resumes, the country files, the portal list, contacts and referrals. Listings do not keep: search again when the window opens.
53. **A foot in the door beats a cold application for a far-off start.** An employer the candidate already works, studies or interns with can plan for a start date that a stranger's application cannot. Ask about converting such a role first.
54. **Permit calendars override the usual lead time.** Where a country runs a yearly lottery or quota, the employer's registration deadline is the real date to work back from.
55. **Read the feed before opening the browser.** Many boards answer an anonymous request with data. Reading them takes seconds, needs no account and covers countries where few employers use the common application systems.
56. **Board families share a format.** A board that runs sites in several countries usually serves the same feed on each, so one reader covers them all. When a feed works for one country, try the sister sites.
57. **Feeds have their own limits.** Page sizes are fixed and often small, some feeds refuse larger requests, some are too large to download, and some ask for credit and a link back. Test with the smallest request first and keep to the board's terms.
58. **Filter by language and by who is hiring.** A national board is mostly in the national language and full of staffing-agency copies of the same job. Keep listings in a language the candidate works in, and prefer the listing from the employer.
59. **Pay words differ as much as currencies.** "Cost to company" in one country includes employer contributions and variable pay; a monthly figure in another excludes a holiday allowance; a yearly figure in a third is paid in thirteen parts. Record what the local figure contains before quoting or comparing it.
60. **Government identity numbers are never the agent's to type.** Some countries' forms ask for a tax or identity number. Leave those fields for the candidate.
61. **Keep looking for new boards.** Search the web for boards at the start of each search and for each new country. Lists written by hiring vendors are a source of names, not of rankings: look at each board before recording it.

