export const meta = {
  name: 'prepare-applications',
  description: 'Read each queued job posting and its application form in parallel and return a ready-to-fill answer plan per job (nothing is filled in or submitted)',
  whenToUse: 'After a job queue exists (profile/jobs/queue.json) and before the main session fills and submits the forms. Helper agents only prepare: form submission by sub-agents is refused by the permission system, and belongs in the session the user is talking to.',
  phases: [
    { title: 'Prepare', detail: 'one agent per batch: fit check, read the form, draft every answer from the profile' },
  ],
}

const cfg = args || {}
const root = cfg.root
const skill = cfg.skillDir || `${root}/skills/iamgroot`
const queueFile = cfg.queueFile || 'profile/jobs/queue.json'
const batches = cfg.batches || []
const date = cfg.date || ''
// Optional overrides. Preparation is judgment and writing, so by default it runs on the session's own model;
// pass a faster model only for batches that are purely mechanical.
const modelOpts = { ...(cfg.model ? { model: cfg.model } : {}), ...(cfg.effort ? { effort: cfg.effort } : {}) }
if (!root || !batches.length) throw new Error('args must include root and batches')

const PLAN_SCHEMA = {
  type: 'object',
  properties: {
    plans: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          id: { type: 'integer' },
          company: { type: 'string' },
          position: { type: 'string' },
          location: { type: 'string' },
          market: { type: 'string' },
          job_url: { type: 'string' },
          application_url: { type: 'string' },
          decision: { type: 'string', enum: ['apply', 'park', 'skip'] },
          reason: { type: 'string' },
          resume_file: { type: 'string' },
          answers: {
            type: 'array',
            items: {
              type: 'object',
              properties: {
                question: { type: 'string' },
                field: { type: 'string' },
                control: { type: 'string' },
                required: { type: 'boolean' },
                value: { type: 'string' },
              },
              required: ['question', 'value'],
            },
          },
          blocking_questions: { type: 'array', items: { type: 'string' } },
          application_limit: { type: 'string' },
          notes: { type: 'string' },
        },
        required: ['company', 'position', 'job_url', 'decision', 'reason'],
      },
    },
    lessons: { type: 'array', items: { type: 'string' } },
  },
  required: ['plans', 'lessons'],
}

function buildPrompt(batchId) {
  return `You are preparing job applications for a candidate. You do NOT fill in or submit anything: you read, decide and draft, so that the main session can fill and submit each form quickly and correctly.

PROJECT ROOT: ${root}
YOUR BATCH: key "${batchId}" in ${root}/${queueFile} (a JSON object keyed by batch id; each job has id, company, position, location, ats, markets_listed, job_url, application_url, greenhouse_board, greenhouse_job_id, compensation and job_description). Load only your batch.
TODAY: ${date}

Read these completely first:
1. ${root}/profile/profile.md: the source of facts about the candidate, including the resume file per market, salary per market, work-authorization answers, standing form answers, and the questions the candidate has NOT answered. If ${root}/profile/countries/ exists, also read the file for each job's country: where it differs from the main profile, the country file decides.
2. ${skill}/references/instructions.md: the matching rules (section 3) and the rules on what may never be invented (section 8). ${skill}/references/countries.md describes what forms ask in each country.
3. ${skill}/references/ats-playbook.md: how each form system exposes its questions.
4. ${skill}/references/lessons.md.

FOR EACH JOB
1. Fit: decide "skip" (say why) when the profile's do-not-apply list covers the role, the central required technology or qualification is missing from the profile, a required language level, clearance or citizenship is not met, the employer states it does not sponsor in a country where the candidate needs sponsorship, the required experience is clearly beyond the profile's band, or the posting is closed.
2. Market: pick the country from the profile's table and name the resume file to upload. If the candidate's start date is outside the application window recorded for that country, the decision is "park" with that reason.
3. Read the whole form without typing into it. For Greenhouse run: python3 ${skill}/scripts/iamgroot.py questions <greenhouse_board> <greenhouse_job_id>. For other systems open the application page read-only (in your own browser tab if you have a browser tool; never type, upload, tick or click submit) or fetch it, and list every question with its control type (text, number, yes/no, radio, select, date, autocomplete, file) and whether it is required. Record any stated application limit.
4. Answer every question from the profile. Written answers are 2 to 5 plain, specific first-person sentences built from the profile's experience and tied to the role; state the start date, and relocation and sponsorship needs where the profile requires them. Never invent experience, skills, opinions about a product, or product usage.
5. If a REQUIRED question cannot be answered from the profile, the decision is "park": list the exact question texts in blocking_questions and still draft every answer you can.
6. Otherwise the decision is "apply" with a complete answers list in the order the form shows them.

OUTPUT
- plans: one item per job, including skipped and parked ones. In notes, name every consent the form asks for and which choice the profile implies, and anything the candidate should know.
- lessons: general, candidate-independent lessons from this batch (new form mechanics, new kinds of question). No candidate details. Empty array if none.`
}

phase('Prepare')
const out = await parallel(batches.map(batchId => () =>
  agent(buildPrompt(batchId), { label: `prepare:${batchId}`, phase: 'Prepare', schema: PLAN_SCHEMA, agentType: 'general-purpose', ...modelOpts })
    .then(r => (r ? { batch: batchId, plans: r.plans || [], lessons: r.lessons || [] } : { batch: batchId, plans: [], lessons: [], incomplete: true }))
))

const done = out.filter(Boolean)
const plans = done.flatMap(b => b.plans.map(p => ({ ...p, batch: b.batch })))
const counts = {}
for (const p of plans) counts[p.decision] = (counts[p.decision] || 0) + 1
log(`prepared ${plans.length} roles: ${JSON.stringify(counts)}`)
return { counts, incomplete: done.filter(b => b.incomplete).map(b => b.batch), plans, lessons: done.flatMap(b => b.lessons) }
