# Job portals by country

Where to look for roles, country by country. The list covers the countries candidates have asked for so far. Add a section whenever a new country is used, and keep the list current (see the end of this file).

Last checked: November 2026.

## How to use a portal

- **Portals are for finding. Apply on the employer's own career page** whenever the posting links to one: the form is shorter, it needs no account, and the application lands in the employer's own system.
- **Most portals need an account to apply or to see full results.** The agent never creates an account or signs in. The candidate creates the accounts they want and signs in themselves; the agent can then search inside a signed-in browser session.
- **Some portals publish an open feed**: they answer an anonymous request with data, so listings can be read without a browser or an account. `iamgroot.py discover` reads the ones marked **tool: `name`** below. Put the names under `portals` in the search configuration and search terms under `queries`:

  ```json
  { "portals": ["arbeitnow", "devitjobsnl", "platsbanken"], "queries": ["software engineer"], "only_english": true }
  ```

  Search terms are the only text sent to a portal. Keep the candidate's personal details out of them.
- A role found on a portal is checked against the tracker by company and title, not by address: the same role appears under many addresses.
- Portals show whatever the employer typed. Check sponsorship, language and location on the employer's own posting before applying. Some feeds carry their own visa flag; the review command shows it.
- Government boards carry many listings from staffing agencies, often several for one real job. Prefer the listing from the employer itself.

## Company career pages (every country)

Most technology employers publish their openings through an applicant-tracking system. `iamgroot.py discover` reads seven of them from a list of company names: Greenhouse, Lever, Ashby, SmartRecruiters, Personio, Recruitee and Workable. Other systems seen often: Workday and iCIMS (large companies; account required), SAP SuccessFactors, Teamtailor (very common in Sweden and Finland), JOIN and Personio (Germany, Switzerland, Austria), BambooHR, Pinpoint, Breezy and Rippling, and in India Darwinbox, Keka, Zoho Recruit and Freshteam.

## Worldwide

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn Jobs | linkedin.com/jobs | Largest board in every country here. Account needed; "Easy Apply" runs inside the candidate's login. |
| Indeed | indeed.com and country sites | Aggregator with a site per country. Account needed to apply. |
| Glassdoor | glassdoor.com | Listings with pay data and employer reviews. |
| Wellfound | wellfound.com | Startups. Account needed. |
| Work at a Startup | workatastartup.com | Y Combinator companies. Account needed. |
| Hacker News "Who is hiring?" | news.ycombinator.com | A thread on the first working day of each month. Open feed: `hn.algolia.com/api/v1/search_by_date?tags=story,author_whoishiring`. |
| Welcome to the Jungle (formerly Otta) | welcometothejungle.com | Technology roles in the UK, the US and Europe. Account needed. |
| Relocate.me | relocate.me | Roles that come with relocation or visa support. No visa filter: search the words "relocation" or "visa". |
| Landing.jobs | landing.jobs | Technology roles in Europe, each marked with whether relocation is paid. **tool: `landingjobs`** |
| Levels.fyi | levels.fyi/jobs | Listings next to verified pay data; useful for salary research. |

### Remote roles

| Portal | Address | Notes |
| --- | --- | --- |
| Remote OK | remoteok.com | **tool: `remoteok`**. Its terms ask for a link back when listings are shown. |
| Remotive | remotive.com | **tool: `remotive`** |
| Himalayas | himalayas.app | Lists the countries each employer hires in. **tool: `himalayas`** |
| Jobicy | jobicy.com | **tool: `jobicy`**. Its terms ask for credit and a link to the source. |
| Working Nomads | workingnomads.com | **tool: `workingnomads`** |
| We Work Remotely | weworkremotely.com | RSS feeds per category. |

Remote roles still have a hiring country. Check the list of countries the employer can employ in before treating "remote" as open to the candidate.

## United States

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed, Glassdoor | see Worldwide | The three largest. |
| DevITjobs US | devitjobs.us | Technology roles in the United States and Canada with salary ranges and a visa flag. **tool: `devitjobsus`** |
| Dice | dice.com | Technology roles; many contract roles and staffing agencies. |
| Built In | builtin.com | Technology employers by city (New York, San Francisco, Seattle, Austin, Boston, Chicago and more). |
| Wellfound, Work at a Startup | see Worldwide | Startups. |
| ZipRecruiter | ziprecruiter.com | Aggregator. |
| Levels.fyi | levels.fyi/jobs | Listings with pay by level. |
| USAJOBS | usajobs.gov | Federal government; almost all roles need US citizenship. Its feed needs a free key. |

Who sponsors: the USCIS H-1B Employer Data Hub (`uscis.gov/tools/reports-and-studies/h-1b-employer-data-hub`) and the Department of Labor disclosure data (`dol.gov/agencies/eta/foreign-labor/performance`) show which employers have filed for foreign workers, how many and at what pay. MyVisaJobs (`myvisajobs.com`) presents the same data by employer.

## United Kingdom

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed, Glassdoor | see Worldwide | |
| DevITjobs UK | devitjobs.uk | Technology roles with salary ranges and a visa flag. **tool: `devitjobsuk`** |
| Reed | reed.co.uk | Large general board. |
| Totaljobs, CWJobs | totaljobs.com, cwjobs.co.uk | Same group; CWJobs is the technology board. |
| Technojobs | technojobs.co.uk | Technology roles. |
| Welcome to the Jungle (Otta) | welcometothejungle.com | Startups and scale-ups, strong in London. |
| Cord, hackajob, Haystack | cord.co, hackajob.com, haystackapp.io | Technology marketplaces where employers contact candidates. Account needed. |
| Work in Startups | workinstartups.com | Early-stage companies. |
| Adzuna, CV-Library | adzuna.co.uk, cv-library.co.uk | Aggregator and general board. Adzuna's feed needs a free key. |
| Find a job | gov.uk/find-a-job | Government board. |

Who sponsors: the Home Office "Register of licensed sponsors: workers" (`gov.uk/government/publications/register-of-licensed-sponsors-workers`) is a downloadable list of every employer licensed to sponsor. An employer missing from it cannot sponsor a Skilled Worker visa.

## Germany

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed, Glassdoor | see Worldwide | |
| XING | xing.com/jobs | The German-speaking professional network; kununu holds its employer reviews. |
| StepStone | stepstone.de | Largest German job board. |
| Jobbörse der Bundesagentur für Arbeit | arbeitsagentur.de/jobsuche | Federal employment agency; the largest listing by count. |
| Make it in Germany | make-it-in-germany.com | Government portal for workers from abroad, with a job listing. |
| Arbeitnow | arbeitnow.com | Filters for visa sponsorship and English. **tool: `arbeitnow`** |
| GermanTechJobs | germantechjobs.de | Technology roles with salary ranges and a visa flag. **tool: `germantechjobs`** |
| Berlin Startup Jobs | berlinstartupjobs.com | Berlin startups. |
| WeAreDevelopers | wearedevelopers.com/jobs | Developer roles in the German-speaking countries. |
| jobvector, heise jobs, t3n jobs | jobvector.de, jobs.heise.de, jobs.t3n.de | Engineering and IT boards. |
| EnglishJobs | englishjobs.de | Roles that do not need German. |

## Netherlands

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed, Glassdoor | see Worldwide | LinkedIn is the main channel for technology roles. |
| DevITjobs NL | devitjobs.nl | Technology roles with salary ranges, working language and a visa flag. **tool: `devitjobsnl`** |
| Nationale Vacaturebank, Monsterboard | nationalevacaturebank.nl, monsterboard.nl | Large general boards, mostly in Dutch. |
| Intermediair | intermediair.nl | Roles for graduates and professionals. |
| Tweakers Carrière | tweakers.net/carriere | Technology roles. |
| Werk.nl | werk.nl | Public employment service (UWV). |
| IamExpat Jobs, Together Abroad, Undutchables | iamexpat.nl/career/jobs-netherlands, togetherabroad.nl, undutchables.nl | Roles for people who do not speak Dutch. |
| EnglishJobs | englishjobs.nl | Roles that do not need Dutch. |
| Welcome to the Jungle (Otta) | welcometothejungle.com | Amsterdam technology companies. |

Who sponsors: the IND "Public register of recognised sponsors" (`ind.nl/en/public-register-recognised-sponsors`) lists every employer allowed to hire highly skilled migrants. Check it before applying.

## Sweden

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed | see Worldwide | |
| Platsbanken | arbetsformedlingen.se/platsbanken | Public employment service; the largest listing. **tool: `platsbanken`** |
| The Hub | thehub.io | Startups in Sweden, Finland, Denmark and Norway. |
| Jobbsafari, Blocket Jobb, Monster | jobbsafari.se, jobb.blocket.se, monster.se | General boards, mostly in Swedish. |
| Ny Teknik Jobb | nyteknik.se/jobb | Engineering and technology roles. |
| Demando | demando.io | Technology marketplace where employers contact candidates. Account needed. |
| Academic Work | academicwork.se | Roles for students and recent graduates through a staffing firm. |
| The Local Jobs | thelocal.se/jobs | English-language roles. |
| EURES | eures.europa.eu | The European job portal; Swedish employers must advertise there before hiring from outside the EU. |

## Finland

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed | see Worldwide | |
| Työmarkkinatori (Job Market Finland) | tyomarkkinatori.fi | Public employment service. |
| Duunitori | duunitori.fi | Largest private board. **tool: `duunitori`** |
| Oikotie Työpaikat | tyopaikat.oikotie.fi | Large general board. |
| Jobly | jobly.fi | General board (formerly Monster Finland). |
| Jobs in Finland | jobs.workinfinland.com | Government listing of roles open to people from abroad. |
| The Hub | thehub.io | Nordic startups. |
| aTalent, Academic Work, Barona | atalent.fi, academicwork.fi, barona.fi | Staffing and recruiting firms that hire for technology roles. |

## Poland

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed | see Worldwide | |
| Just Join IT | justjoin.it | Largest technology board; every listing shows a pay range per contract type. |
| No Fluff Jobs | nofluffjobs.com | Technology roles with mandatory pay ranges. Its feed (`nofluffjobs.com/api/posting`) is over 100 MB, too large for the tool. |
| the:protocol | theprotocol.it | Technology board of Pracuj.pl. |
| Pracuj.pl | pracuj.pl | Largest general board. |
| Bulldogjob, SOLID.jobs | bulldogjob.pl, solid.jobs | Technology roles. |
| Rocket Jobs | rocketjobs.pl | Non-engineering roles from the Just Join IT group. |

Listings quote pay separately for an employment contract (umowa o pracę, "UoP") and a business-to-business contract ("B2B"). Compare like with like.

## Switzerland

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed | see Worldwide | |
| jobs.ch | jobs.ch | Largest board, German-speaking part. **tool: `jobsch`** |
| jobup.ch | jobup.ch | Same group, French-speaking part. |
| JobScout24 | jobscout24.ch | Large general board. |
| SwissDevJobs | swissdevjobs.ch | Technology roles with salary ranges and a visa flag. **tool: `swissdevjobs`** |
| ICTjobs | ictjobs.ch | IT roles. |
| Job-Room | job-room.ch | Public employment service (SECO). |
| TieTalent | tietalent.com | Technology marketplace. Account needed. |

## Singapore

| Portal | Address | Notes |
| --- | --- | --- |
| LinkedIn, Indeed | see Worldwide | |
| MyCareersFuture | mycareersfuture.gov.sg | Government board. Employers must advertise here before applying for an Employment Pass, so nearly every sponsored role appears, with its pay range. **tool: `mycareersfuture`** |
| JobStreet | sg.jobstreet.com | Largest private board (SEEK group). |
| NodeFlair | nodeflair.com | Technology roles with pay data. |
| Tech in Asia Jobs | techinasia.com/jobs | Startups across South-East Asia. |
| Glints | glints.com/sg | Startups and young professionals. |
| eFinancialCareers | efinancialcareers.sg | Banks and financial technology. |
| Wellfound | see Worldwide | Startups. |

## India

| Portal | Address | Notes |
| --- | --- | --- |
| Naukri | naukri.com | The largest board by far. Recruiters search candidate profiles, so a complete and recently updated profile matters as much as applying. Account needed. |
| LinkedIn, Indeed | see Worldwide | LinkedIn is the main channel for product companies, global capability centres and referrals. |
| foundit (formerly Monster India) | foundit.in | Large general board. |
| Instahyre | instahyre.com | Technology roles where employers contact candidates; aimed at people with two or more years of experience. **tool: `instahyre`** (search terms are matched against skills). |
| Cutshort | cutshort.io | Technology and startup roles. Account needed. |
| Hirist | hirist.tech | Technology roles, mostly product companies. Account needed. |
| Wellfound, Work at a Startup | see Worldwide | Startups, including many that hire in Bengaluru. |
| Hasjob | hasjob.co | Small board from the HasGeek community; startups and developer roles. **tool: `hasjob`** |
| Weekday | weekday.works | Engineering roles; free for candidates. |
| iimjobs | iimjobs.com | Management and senior roles. |
| Shine, TimesJobs | shine.com, timesjobs.com | General boards. |
| Internshala, Unstop | internshala.com, unstop.com | Internships, campus hiring and first jobs. |
| Apna, WorkIndia | apna.co, workindia.in | Entry-level and non-desk work. |
| National Career Service | ncs.gov.in | Government board. |
| Turing, Uplers | turing.com, uplers.com | Remote roles with employers abroad, after a vetting process. Account needed. |
| AmbitionBox, Glassdoor | ambitionbox.com, glassdoor.co.in | Pay data and employer reviews for salary research. |

Listings quote pay as yearly "CTC" (cost to company) in lakhs of rupees ("LPA"). See the India section of `countries.md` before reading or answering any pay figure.

## Keeping this list current

Job boards open, merge, change name and close every year. The list is only as good as its last check.

- **At the start of a search, and for every new country, search the web** for boards that are not in this file: "job boards" with the country, the field and the current year; "visa sponsorship jobs" with the country; "startup jobs" with the city. Rankings in blog posts are mostly written by companies that sell hiring services: use them to collect names, then look at each board yourself.
- **Check each new board before adding it**: does it carry real listings for the candidate's field, in which language, does it need an account, and does it answer an anonymous request with data. Add it to the country table with a one-line note.
- **A board with an open feed can be added to the tool**: write a reader in `scripts/discover_jobs.py` that returns the same fields as the others, end its locations with the country name in English, and add a `tool:` mark here.
- **Remove or rename** boards that have closed or merged, and update "Last checked" at the top.
- For a country that is not listed yet, record: the public employment service, the two or three largest general boards, the boards for the candidate's field, the boards for people who do not speak the local language, the startup board, and the official list of employers allowed to sponsor work permits if the country publishes one.

### Seen but not yet tried

Found in web searches and not yet examined. Look at them in a later run, then move each one into a table above or delete it.

- **New job-search products built around AI matching** (announced 2025 to 2026): a jobs platform announced by OpenAI (launch not confirmed when checked), JobAssist, Callings.ai, AITechRoles, Jobbortunity. Most claim to aggregate other boards; check whether they add listings that the boards above lack.
- **European boards**: Startup.Jobs, Work in Estonia, StartupJobs.cz, F6S, Europe Language Jobs, EuroTechJobs, and the Jobs in Network family of English-language city boards (for example jobsinstockholm.com).
- **Visa-sponsorship listings**: ApplyWave, which lists roles from employers it has checked as sponsors.
- **India**: HackerRank Jobs, Freshersworld.
- **Feeds that need a free key**: USAJOBS and Adzuna (several countries). A key belongs to the candidate, who would have to register for it.
