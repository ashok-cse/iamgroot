# Country guide

A job search changes from country to country in six ways: the right to work, how pay is quoted, what a resume looks like, which language is needed, what forms ask, and where roles are advertised. This file holds what is true for everyone; the candidate's own answers go in a private country profile.

Permit rules and salary thresholds change every year. Each figure below carries the date it was checked and the official page to check it on. Check again before telling a candidate that a role does or does not qualify. Nothing here is legal advice.

## One profile per country

For every country the candidate targets, create `profile/countries/<country>.md` with `python3 scripts/iamgroot.py country "<Country>"` (template: `country.example.md`). Fill it from this guide and from the candidate's answers. The main profile stays the source for facts that do not change by country (identity, experience, start date).

Before the first application in a new country:

1. Read the country's section here and its section in `job-portals.md`.
2. Work out the candidate's route to the right to work there from their citizenship and current residence status. If either is not in the profile, ask.
3. Ask the country questions below in one round.
4. Research a salary default and range in the country's own convention (yearly or monthly, local currency) and record the sources.
5. Build a resume variant whose header and target statement fit that country.
6. Add the country's place names to the search configuration.

## Questions to ask for each new country

- Citizenship and any residence permit already held there. These decide every answer about the right to work.
- The exact answers to "are you authorised to work here?" and "do you need sponsorship?", and the sentence to use in free text.
- Salary default and range, in the local currency and the local convention.
- Level in the local language.
- Cities, and whether remote roles hired from that country count.
- Whether to apply to employers whose sponsorship policy is unknown, or only to those known to sponsor.
- Contract types the candidate accepts where a country has more than one.
- What the resume header should say about relocation and sponsorship.
- Anything the country's forms ask that the profile does not cover (see each section).

## What differs, at a glance

| Country | Usual work permit for a hire from abroad | Pay is quoted | Resume |
| --- | --- | --- | --- |
| United States | H-1B (yearly lottery) | per year, USD | 1 page, no photo, no personal data |
| United Kingdom | Skilled Worker | per year, GBP | 2 pages, no photo |
| Germany | EU Blue Card | per year, EUR | up to 2 pages, photo optional |
| Netherlands | Highly skilled migrant | per month, EUR, plus 8% holiday allowance | 1 to 2 pages |
| Sweden | Work permit | per month, SEK | 1 to 2 pages plus a short letter |
| Finland | Specialist residence permit | per month, EUR | 1 to 2 pages |
| Poland | Work permit or EU Blue Card | per month, PLN, by contract type | 1 to 2 pages with a data-consent clause |
| Switzerland | B or L permit under a yearly quota | per year, CHF, often in 13 payments | 2 pages, photo customary, certificates attached |
| Singapore | Employment Pass | per month, SGD | 1 to 2 pages |

## United States

- **Right to work.** A hire from abroad normally needs an H-1B, which the employer files. There is a yearly cap and a lottery: employers register candidates in March, results come at the end of March, and the earliest start is 1 October. Since the 2026 lottery, selection is weighted by wage level, so higher-paid offers have better odds. A September 2025 proclamation added a USD 100,000 payment for new petitions for workers outside the country; it has been challenged in court and its status was unsettled when checked. Other routes exist for some people only: L-1 (transfer after a year with the same company abroad), O-1 (extraordinary ability), E-3 (Australia), H-1B1 (Chile, Singapore), TN (Canada, Mexico), and universities and non-profit research bodies, which are outside the cap. Checked November 2026: `uscis.gov/working-in-the-united-states/h-1b-specialty-occupations`.
- **What this means.** An employer must be willing to wait for the lottery and may lose it. Many postings say "no sponsorship". The realistic targets are employers with a record of sponsoring (see `job-portals.md`) and international companies where a transfer is possible later.
- **Pay.** Yearly base salary in USD; equity and bonus are quoted separately. Several states require a pay range in the posting.
- **Resume.** One page (two for long careers). No photo, date of birth, nationality or marital status.
- **Forms ask.** "Are you legally authorized to work in the United States?" and "Will you now or in the future require sponsorship?", almost always as two separate questions. Voluntary self-identification of gender, race or ethnicity, veteran status and disability: each has a "decline to answer" choice. Export-control questions. Consent to a background check. Dates are month/day/year.

## United Kingdom

- **Right to work.** Skilled Worker visa. The employer must hold a sponsor licence and assigns a certificate of sponsorship. The salary must be at least the general threshold (GBP 41,700 a year) or the going rate for the occupation, whichever is higher; software roles were reported at about GBP 54,700. Lower rates apply to some new entrants. Checked November 2026: `gov.uk/skilled-worker-visa`.
- **Pay.** Yearly, GBP. Notice periods of one to three months are normal.
- **Resume.** Called a CV. Two pages, no photo.
- **Forms ask.** Right to work in the UK and need for sponsorship; optional equality monitoring; office days per week.

## Germany

- **Right to work.** EU Blue Card: a recognised degree and a job offer above the salary threshold (EUR 50,700 a year in 2026; EUR 45,934.20 for shortage occupations including IT, and for recent graduates). IT specialists can qualify on experience without a degree. Any employer can hire this way; there is no sponsor licence. Graduates of German universities may stay 18 months to look for work and can switch permit from inside the country. Checked November 2026: `make-it-in-germany.com/en/visa-residence/types/eu-blue-card`.
- **Pay.** Yearly gross, EUR. Forms ask for a salary expectation ("Gehaltsvorstellung") and the earliest start date.
- **Resume.** "Lebenslauf", up to two pages. A photo is traditional and optional.
- **Language.** Many roles need German; technology roles in large cities often do not. Check every posting.
- **Forms ask.** Salutation, salary expectation, start date, current permit, German level.

## Netherlands

- **Right to work.** Highly skilled migrant permit ("kennismigrant"). Only an employer on the IND register of recognised sponsors can use it. Salary criteria for 2026, per month and excluding the 8% holiday allowance: EUR 5,942 from age 30, EUR 4,357 under 30, EUR 3,122 for people eligible for the orientation year for recent graduates. The EU Blue Card is an alternative. A tax facility for workers recruited from abroad (the "30% ruling") exists and is being reduced. Checked November 2026: `ind.nl/en/required-amounts-income-requirements`.
- **Pay.** Monthly gross, EUR, plus 8% holiday allowance paid once a year; some employers add a thirteenth month. Say clearly whether a yearly figure includes the allowance.
- **Resume.** One to two pages. English is normal in technology.
- **Forms ask.** Whether a work permit is needed, salary expectation per month or per year, notice period, Dutch level.

## Sweden

- **Right to work.** Work permit based on a job offer. Since 1 June 2026 the salary must be at least 90% of the Swedish median (SEK 34,470 a month when checked) and the terms must match collective agreements or custom for the occupation. The employer must have advertised the role in the EU for at least ten days. The EU Blue Card is an alternative. Checked November 2026: `migrationsverket.se/en/you-want-to-apply/work.html`.
- **Pay.** Monthly gross, SEK. There is no statutory minimum wage; collective agreements set the floor.
- **Resume.** One to two pages with a short personal letter. English is normal in technology.
- **Forms.** Many employers use Teamtailor. Forms are short: resume, letter, sometimes salary expectation per month.

## Finland

- **Right to work.** Residence permit for a specialist: expert work, a higher-education degree or equal expertise, and a gross salary of at least EUR 3,937 a month in 2026. The EU Blue Card has the same threshold. A fast track with a decision in about two weeks is offered to specialists. Checked November 2026: `migri.fi/en/specialist`.
- **Pay.** Monthly gross, EUR. A holiday bonus is common.
- **Resume.** One to two pages. English is the working language in many technology companies.
- **Forms ask.** Salary request per month, start date, Finnish level.

## Poland

- **Right to work.** Either a work permit that the employer applies for, followed by a national visa, or the EU Blue Card, which needs a salary of at least 150% of the national average wage (about PLN 13,000 a month in 2026) and a contract of a year or more. Checked November 2026: `gov.pl/web/udsc-en`.
- **Contract types.** Listings quote two: an employment contract (umowa o pracę, "UoP") and a business-to-business contract ("B2B") in which the worker invoices as a self-employed person. A permit for a hire from abroad is tied to employment; a B2B contract needs the worker's own registered business and does not by itself give a right to work.
- **Pay.** Monthly gross, PLN, shown as a range per contract type.
- **Resume.** One to two pages. A sentence consenting to the processing of personal data for recruitment is customary at the foot of the resume, or a tick box on the form.
- **Language.** English is common in technology; Polish is needed elsewhere.

## Switzerland

- **Right to work.** For people from outside the EU and EFTA the employer applies to the canton, and the federal migration office then decides. The employer must show that no suitable person was found in Switzerland or the EU, the candidate must be a qualified specialist, the pay must match local custom, and a permit must be left in the yearly quota (4,500 B permits and 4,000 L permits for 2026). L permits cover up to a year, B permits longer. Checked November 2026: `sem.admin.ch/sem/en/home/themen/arbeit/nicht-eu_efta-angehoerige.html`.
- **What this means.** This is the hardest route in Europe for a new hire from outside. Large international employers and research institutions use it most.
- **Pay.** Yearly gross, CHF, often paid in 13 instalments.
- **Resume.** Two pages; a photo is customary; diplomas and work certificates are often requested with the application.
- **Language.** German around Zurich, Basel and Bern; French around Geneva and Lausanne; English in international companies.

## Singapore

- **Right to work.** Employment Pass, which the employer applies for. Two tests: a qualifying salary that starts at SGD 5,600 a month (SGD 6,200 in financial services) and rises with age, and a points system (COMPASS) that scores salary against the sector, qualifications and the employer's workforce. A rise of the starting figures to SGD 6,000 and SGD 6,600 from January 2027 was reported. The employer must first advertise the role on MyCareersFuture for 14 days. Checked November 2026: `mom.gov.sg/passes-and-permits/employment-pass/eligibility`.
- **Pay.** Monthly, SGD; a thirteenth month and a bonus are common.
- **Resume.** One to two pages.
- **Forms ask.** Nationality and residency status (citizen, permanent resident, pass holder), current or last salary, expected salary, notice period. Where the profile does not allow a question to be answered, stop and ask.

## Adding a country

Add a row to the table and a section with the same headings. Use the immigration authority's own page as the source, write the date checked, and add the country's portals to `job-portals.md`.
