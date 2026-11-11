export const meta = {
  name: 'apply-jobs',
  description: 'Apply to the queued job postings in parallel browser tabs using the candidate profile, and return one result per job',
  whenToUse: 'After a job queue exists (profile/jobs/queue.json) and the candidate profile has its standing answers filled in',
  phases: [
    { title: 'Apply', detail: 'one agent per batch of roles, each in its own browser tab; lanes run side by side' },
  ],
}

const cfg = args || {}
const root = cfg.root
const queueFile = cfg.queueFile || 'profile/jobs/queue.json'
const lanes = cfg.lanes || []
const date = cfg.date || ''
if (!root || !lanes.length) throw new Error('args must include root and lanes')

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    results: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          company: { type: 'string' },
          position: { type: 'string' },
          location: { type: 'string' },
          country: { type: 'string' },
          job_url: { type: 'string' },
          application_url: { type: 'string' },
          status: { type: 'string', enum: ['submitted', 'blocked', 'skipped', 'failed'] },
          application_method: { type: 'string' },
          salary_info: { type: 'string' },
          start_date_info: { type: 'string' },
          visa_info: { type: 'string' },
          notes: { type: 'string' },
          custom_message_sent: { type: 'string' },
          blocking_question: { type: 'string' },
        },
        required: ['company', 'position', 'job_url', 'status', 'notes'],
      },
    },
    lessons: { type: 'array', items: { type: 'string' } },
  },
  required: ['results', 'lessons'],
}

const BROWSER_TOOLS = 'select:mcp__claude-in-chrome__tabs_context_mcp,mcp__claude-in-chrome__tabs_create_mcp,mcp__claude-in-chrome__tabs_close_mcp,mcp__claude-in-chrome__navigate,mcp__claude-in-chrome__computer,mcp__claude-in-chrome__find,mcp__claude-in-chrome__get_page_text,mcp__claude-in-chrome__javascript_tool,mcp__claude-in-chrome__file_upload,mcp__claude-in-chrome__browser_batch'

function buildPrompt(batchId) {
  return `You are applying to job postings on behalf of a candidate, using the Claude in Chrome browser tools. This is real: every form you submit goes to a real employer. The candidate asked for this run and has authorised submitting applications that follow the rules below.

PROJECT ROOT: ${root}
YOUR BATCH: key "${batchId}" in ${root}/${queueFile}. The file is a JSON object keyed by batch id; each job has id, company, position, location, ats, markets_listed, job_url, application_url, greenhouse_board, greenhouse_job_id, compensation and job_description. Load only your batch (for example with a short python3 command).
TODAY: ${date}

Read these three files completely before anything else:
1. ${root}/profile/profile.md is the only source of facts about the candidate: identity, which resume file to upload per market, salary per market, work-authorization answers, standing form answers, and the list of questions the candidate has NOT answered.
2. ${root}/docs/ats-playbook.md explains how to read, fill, verify and submit forms on Ashby and Greenhouse, with script helpers to paste, and how to confirm a submission.
3. ${root}/LESSONS.md holds general lessons from earlier runs.

BROWSER SETUP
- Load the tools in one ToolSearch call with the query: ${BROWSER_TOOLS}
- Call tabs_context_mcp, then tabs_create_mcp to open YOUR OWN tab. Use only that tabId on every call. Other agents are working in other tabs of the same browser right now: never navigate, type in, or close a tab you did not create. Close your own tab when you finish.
- Chain steps with browser_batch. Return JSON.stringify(...) from every javascript_tool script.

FOR EACH JOB IN YOUR BATCH, IN ORDER
1. Decide whether to apply. Read the job description. SKIP (status "skipped", say why) when any of these holds: the profile's do-not-apply list covers it; it is a UK-only role and the posting says it does not sponsor visas or requires an existing right to work in the UK; it requires fluent or business German; it requires security clearance or a specific citizenship; the central required technology is one the profile lists as not on the resume (for example a Go-only, Kotlin/Spring-only, .NET or Ruby role, or model-training / classic ML as the core); the required experience is clearly more than 6 years; it is not a full-time software engineering role.
2. Pick the market. If the role can be done in Germany or remotely from Germany, treat it as Germany: Germany resume, German work-authorization answers, EUR salary, residence Germany. If it is UK-only: London resume, UK answers (sponsorship required), GBP salary. When a role lists both, treat it as Germany.
3. Read the whole form before typing. For Greenhouse run: python3 ${root}/scripts/gh_questions.py <greenhouse_board> <greenhouse_job_id>. For Ashby and others read the page as the playbook describes. Lever forms (jobs.lever.co/.../apply) are a single page; read them with get_page_text and find.
4. If any REQUIRED question cannot be answered from profile.md (see its "not answered" list), do not fill the form: status "blocked" and put the exact question text in blocking_question. Do the same if a CAPTCHA challenge is shown, if applying needs a login or an account, or if the employer rejects the application because of an application limit.
5. Otherwise fill the form, verify every value in a separate step, submit, and confirm the success page or banner exactly as the playbook describes. Status is "submitted" only after you have read the confirmation.
6. Immediately append the outcome as ONE JSON line to ${root}/profile/jobs/results/${batchId}.jsonl (same fields as a results item in your final output) before you start the next job. This file is the record if you are interrupted.

HARD RULES
- Facts come only from profile.md and the job posting. Never invent experience, skills, opinions about a product, product usage, salary history, visa status, references or contacts. Never claim a technology that profile.md lists as not on the resume.
- Written answers: 2 to 5 plain, specific sentences in the first person, tied to the role, built from the profile's experience section. State the start date, and for UK roles also the relocation to London and the sponsorship need. No filler and no invented enthusiasm.
- Salary: the profile default for the market, or a figure inside the posted range when one is published.
- Consents: accept privacy or data-processing consent that is required to submit; follow the profile for talent pools, marketing, WhatsApp and interview-recording choices; reject non-essential cookies.
- Never solve a CAPTCHA, create an account, type a password, log in, or download a file.
- One application per company. Apply only to the roles in your batch.
- If the same browser step fails three times, give the job status "failed" with what happened and move on. Do not loop. Aim for about 15 tool calls per job.
- Do not edit profile.md, profile/applications.csv or any other project file. The only file you write is your results .jsonl.

YOUR FINAL OUTPUT
- results: one item per job in your batch, including skipped, blocked and failed ones. In notes, list every consent you ticked and every answer the candidate should know about (for example language levels, relocation, office attendance, anything selected in a dropdown about work authorization). application_method is like "Company career page (Ashby)". custom_message_sent says "Yes (...)" or "No".
- lessons: general, candidate-independent lessons from this batch that would change how a future run handles a form, an ATS or a question type (new mechanics, new kinds of question, new failure modes). No candidate details. Empty array if none.`
}

phase('Apply')
const laneResults = await parallel(lanes.map((lane, laneIndex) => async () => {
  const out = []
  for (const batchId of lane) {
    const r = await agent(buildPrompt(batchId), {
      label: `apply:${batchId}`,
      phase: 'Apply',
      schema: RESULT_SCHEMA,
      agentType: 'general-purpose',
    })
    if (r) {
      out.push({ batch: batchId, results: r.results || [], lessons: r.lessons || [] })
      const n = (r.results || []).filter(x => x.status === 'submitted').length
      log(`batch ${batchId}: ${n} submitted of ${(r.results || []).length}`)
    } else {
      log(`batch ${batchId}: agent returned nothing; read profile/jobs/results/${batchId}.jsonl for what it recorded`)
      out.push({ batch: batchId, results: [], lessons: [], incomplete: true })
    }
  }
  return out
}))

const batches = laneResults.filter(Boolean).flat()
const results = batches.flatMap(b => b.results.map(r => ({ ...r, batch: b.batch })))
const lessons = batches.flatMap(b => b.lessons)
const counts = {}
for (const r of results) counts[r.status] = (counts[r.status] || 0) + 1
const incomplete = batches.filter(b => b.incomplete).map(b => b.batch)
return { counts, incomplete, results, lessons }
