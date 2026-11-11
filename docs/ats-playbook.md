# ATS playbook

How to read and fill application forms on each applicant-tracking system with the Claude in Chrome tools.
Everything here is independent of the candidate; candidate facts come only from `profile/profile.md`.

## Ground rules for every form

1. Work in your own browser tab and pass its `tabId` on every call. Never touch another tab.
2. Read the whole form before typing anything. If one required question cannot be answered from the profile, do not start filling: report the application as `blocked` with the exact question text.
3. Fill, then verify the values in a separate step, then submit, then confirm the success page. Never chain a navigation after a submit unless a script step has thrown on "not submitted".
4. A click that lands while the button is off-screen can be lost. Scroll the submit button into view first. If the form is still showing after the click with no error banner, click once more and re-check.
5. Never solve a CAPTCHA, create an account, type a password, or log in. Report the application as `blocked`.
6. Decline non-essential cookies. Leave optional marketing opt-ins unticked unless the profile says otherwise.
7. One application per company unless the form or posting clearly allows more. Many boards cap applications ("This job has application limits").

## Finding roles and reading forms without a browser

Public, unauthenticated JSON endpoints (send no candidate data):

| ATS | Listings | Form questions |
| --- | --- | --- |
| Greenhouse | `https://boards-api.greenhouse.io/v1/boards/{board}/jobs?content=true` | `https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{id}?questions=true` |
| Lever | `https://api.lever.co/v0/postings/{board}?mode=json` (EU: `api.eu.lever.co`) | not exposed |
| Ashby | `https://api.ashbyhq.com/posting-api/job-board/{board}?includeCompensation=true` | not exposed; read the page |

`scripts/discover_jobs.py` scans all three; `scripts/gh_questions.py {board} {id}` prints a Greenhouse form with its select options.

## Ashby (`jobs.ashbyhq.com/{board}/{job-id}/application`)

Structure: every field is a `label` whose `for` points at the input. Yes/No questions are either two `button`s (active one has `_active_` in its class) or a radio `fieldset`. Location fields are autocompletes with placeholder `Start typing...`. Date fields have placeholder `Pick date...`.

Read the form:

```js
// field list with required marker and input type
const form=document.querySelector('[role=tabpanel]')||document.body;
JSON.stringify([...form.querySelectorAll('div')].filter(d=>d.querySelector(':scope > label')).map(d=>{
  const l=d.querySelector(':scope > label'); const req=/required|\*/.test(l.className+l.innerHTML);
  const inner=[...d.querySelectorAll('input,textarea,select')].map(e=>e.type+(e.placeholder?'('+e.placeholder+')':'')).slice(0,3);
  return (req?'*':'')+l.innerText.trim().slice(0,90)+' ['+inner.join(',')+']';}))
```

`get_page_text` gives the full question wording and option labels. `find` with "Resume file input and Submit Application button" gives the two refs you need (`file_upload` needs the ref of the field's own file input, not the "Autofill from resume" one).

Helpers to install once per page load (one `javascript_tool` call):

```js
window.__lab=(t)=>{const l=[...document.querySelectorAll('label')].find(l=>l.innerText.trim().replace(/\s+/g,' ').startsWith(t)); if(!l) throw new Error('no label: '+t); return l;};
window.__el=(t)=>{const l=__lab(t); const el=document.getElementById(l.htmlFor)||l.parentElement.querySelector('input,textarea'); if(!el) throw new Error('no input: '+t); return el;};
window.__focus=(t)=>{const el=__el(t); el.scrollIntoView({block:'center'}); el.focus(); return 'focused '+t;};
window.__val=(t)=>__el(t).value;
// Yes/No rendered as buttons
window.__yn=(t,ans)=>{let c=__lab(t).parentElement,b; for(let i=0;i<4&&c;i++){b=[...c.querySelectorAll('button')].find(b=>b.innerText.trim()===ans); if(b) break; c=c.parentElement;} if(!b) throw new Error('no button '+ans+' for '+t); b.click(); return 'clicked '+ans;};
window.__ynv=(t)=>{let c=__lab(t).parentElement; for(let i=0;i<4&&c;i++){const bs=[...c.querySelectorAll('button')].filter(b=>/^(Yes|No)$/.test(b.innerText.trim())); if(bs.length){const a=bs.find(b=>/active/i.test(b.className)); return a?a.innerText.trim():null;} c=c.parentElement;} return null;};
// radio / checkbox option inside a question group
window.__grp=(q,opt)=>{let c=__lab(q).parentElement; for(let i=0;i<4&&c;i++){const l=[...c.querySelectorAll('label')].find(l=>l.innerText.trim()===opt); if(l){const el=document.getElementById(l.htmlFor)||l.querySelector('input'); if(!el||!el.checked) l.click(); return 'picked '+opt;} c=c.parentElement;} throw new Error('no option '+opt+' for '+q);};
window.__grpv=(q)=>{let c=__lab(q).parentElement; for(let i=0;i<4&&c;i++){const ins=[...c.querySelectorAll('input[type=radio],input[type=checkbox]')]; if(ins.length) return ins.filter(x=>x.checked).map(x=>((document.querySelector('label[for="'+x.id+'"]')||x.closest('label')||{}).innerText||'').trim()).join('+'); c=c.parentElement;} return null;};
```

Fill pattern, all in one `browser_batch`:

- Text: `javascript_tool` `__focus('Label start')`, then `computer` `type`. Typing real keys is what makes the React state update; do not set `.value` from script.
- Number inputs reject text: type digits only (`80000`).
- Yes/No buttons: `__yn(label,'Yes')`. Radios and checkboxes: `__grp(question, optionText)`.
- Location autocomplete: focus, type the city (or country), `wait` 2 s, press `Return`; the first suggestion is preselected. Verify the value afterwards (`Berlin, Germany`).
- Date picker: focus, type `MM/DD/YYYY`, press `Escape`.
- A plain-text start-date field takes words ("September 2027"), never an ambiguous numeric date.

Verify in a later `javascript_tool` step, never in the same script that clicked: the active class on a Yes/No button appears only after React re-renders. Ignore the hidden reCAPTCHA `textarea` when checking that textareas are filled. A hidden checkbox behind a Yes/No widget is checked for Yes and unchecked for both No and unanswered, so read the active button instead.

Submit and confirm:

```js
// before the click: put the button on screen
[...document.querySelectorAll('button')].find(b=>/Submit Application/.test(b.innerText)).scrollIntoView({block:'center'});
// after the click and a 7 s wait: throw unless the success banner is there
const t=document.body.innerText; const ok=/Success/i.test(t)&&!/Submit Application/.test(t);
const banner=(t.match(/(Success[\s\S]{0,160})/)||t.match(/(Your form needs corrections[\s\S]{0,300})/)||t.match(/(We couldn't submit[\s\S]{0,200})/)||['(no banner)'])[0];
if(!ok) throw new Error('NOT SUBMITTED: '+banner); banner
```

Outcomes seen: a green "Success" banner (submitted); "Your form needs corrections" listing a missed required field (fix and resubmit); "We couldn't submit your application ... limiting applications" (employer cap; report `blocked`, do not retry); form unchanged with no banner (click was lost; click again).

## Greenhouse (`job-boards.greenhouse.io`)

Any Greenhouse job, including ones embedded in a company site inside an iframe, opens as a top-level form at:

`https://job-boards.greenhouse.io/embed/job_app?for={board}&token={job_id}`

Use that URL when a company careers page wraps the form in an iframe, because the tools cannot reach inside a cross-origin iframe.

Field ids are stable and match the questions API: `first_name`, `last_name`, `email`, `country` (phone country), `phone`, `candidate-location`, `resume` (file input), `question_{id}` for custom questions, numeric ids for demographic questions, and `gdpr_demographic_data_consent_given_1` for the demographic consent box.

```js
window.__f=(id)=>{const e=document.getElementById(id); if(!e) throw new Error('no element '+id); e.scrollIntoView({block:'center'}); e.focus(); return 'focused '+id;};
// selected value(s) of a react-select
window.__sv=(id)=>{const e=document.getElementById(id); let c=e; for(let i=0;i<8&&c;i++){const v=[...c.querySelectorAll('[class*=multi-value__label],[class*=single-value]')]; if(v.length) return v.map(x=>x.innerText.trim()).join('+'); c=c.parentElement;} return null;};
// options of the currently open react-select (the phone country list also uses role=option, so scope to the menu)
window.__opts=()=>[...document.querySelectorAll('[class*=select__menu] [role=option], [class*=select__option]')].map(o=>o.innerText.trim());
```

- Text inputs: `__f(id)` then `type`.
- Phone: select the country first (`__f('country')`, type the country name, `Return`), then type the national number without the country code.
- Location: `__f('candidate-location')`, type the city, `wait` 3 s, `Return`.
- Selects are react-select comboboxes: `__f(id)`, type the start of the option text, `Return`. Type enough text to be unique: typing `75.000` matched "65.000€ - 75.000€" before "75.000€ - 85.000€". Check the result with `__sv(id)`; on a multi-select, `Backspace` removes the last chosen value.
- To list options that the API did not return (demographic questions), focus the field, press `ArrowDown`, read `__opts()`, press `Escape`.
- Checkboxes: click the `label[for=id]`.
- Resume: `find` "Resume/CV attach file input and Submit application button"; the first file input is the resume, the second is the cover letter.
- Success is a redirect to a path ending in `/confirmation` with "Thank you for applying".

## Lever, Workday, SmartRecruiters, Personio and company-built portals

Not yet exercised. Workday and many company portals require creating an account, which the agent must not do: report those as `blocked` for the candidate to apply manually. Record what works here as soon as a form on a new system has been completed.

## Running several applications at once

Several agents can each drive their own tab in the same Chrome at the same time: typing, autocompletes and uploads are per tab and do not interfere, as long as every call carries the agent's own `tabId`.

`javascript_tool` results that look like `key=value; key=value` are blocked by the browser tool's output filter ("BLOCKED: Cookie/query string data"). Return `JSON.stringify({...})` from every script instead of hand-built strings.

`navigate` to `about:blank` or other browser-internal URLs is refused, and one such step makes a whole `browser_batch` fail before it starts.
