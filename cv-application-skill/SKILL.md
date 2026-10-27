---
name: cv-application-workflow
description: Tailor a UK job application end to end from a job description - JD gap analysis, ATS-ready British English CV (.docx), ATS and recruiter review, optional cover letter and interview preparation. Use when the user shares a job description, job link or vacancy and wants a CV, cover letter or interview prep for it.
---

# CV Application Workflow

A staged workflow for turning one job description (JD) into a tailored, ATS-safe CV and, on request, a cover letter and interview kit. It works for any candidate: everything about the person comes from their own CV and answers, never from assumptions.

## Ground rules (apply at every stage)

1. **Never invent experience.** Every claim, number, tool and employer must come from the candidate's CV, earlier answers in the conversation, or a facts file they provided. If a bullet needs a number you do not have, ask. Do not estimate.
2. **Ask before you write.** If you disagree with the candidate's framing, or a gap needs a decision, raise it and wait for their answer before drafting.
3. **Discussion language** follows the candidate (e.g. reply in Chinese if they write in Chinese). **All application content** (CV, cover letter, interview answers) is in **British English** (organise, prioritise, programme, analyse, licence/license, -ise spellings).
4. **No AI tone.** Avoid: em dashes, "leveraged", "spearheaded", "passionate about", "dynamic", "results-driven", "proven track record", "in today's fast-paced", rule-of-three padding, and signposting ("It is worth noting that"). Shorter sentences, concrete nouns, plain verbs.
5. **Honest gaps.** A gap that writing cannot fix is acknowledged at interview, not hidden or stretched in the CV. If a JD has a hard-barrier gap (a required licence, regulated experience, a domain the candidate has never touched), say so early and suggest withdrawing rather than polishing a weak application.
6. **Certifications** are listed only if completed or genuinely in progress. Never list an unstarted course.
7. **Seniority framing** matches the role: for Associate / Executive / Specialist roles avoid "led strategy" or management language; prefer established, defined, enabled, coached, owned.

## First run: set up the candidate profile

Before Stage 1 on a new candidate, collect and confirm:

- Full name (for the CV header and cover letter sign-off), location, phone, email, LinkedIn, right-to-work status
- Current CV (attached file or pasted text)
- Optional: a list of verified metrics and "do not claim" boundaries (tools never used, responsibilities never held)

Summarise this as a short **facts list** in the conversation and treat it as the only source of truth. If the user keeps a facts file in a Project or memory, read it first and use it instead of asking again.

## Naming convention

Name every application `[Company name] - [Job title]`. Output files: `[Full Name] [Year] CV - [Job title] ([Company]).docx` and `... CL - ...` for cover letters.

---

## Stage 1: Job analysis and CV drafting

### 1.1 Research
Look up the company's product, market and recent news (web search when available). Identify **the problem this hire is meant to solve**; the CV should show the candidate can solve that problem.

### 1.2 JD deconstruction
List every requirement in the JD, split into:
- **Essential / minimum requirements**
- **Other duties and desirable requirements**

### 1.3 Gap analysis
For each requirement, map it to the candidate's evidence in a table:

| Requirement | Candidate evidence | Status (Strong / Partial / Missing) |

Then list **everything missing**: skills, experience, tools, metrics or context needed to write a stronger CV. Ask the candidate specific questions to fill those gaps. **Do not draft bullets until they answer**, unless they explicitly tell you to proceed with what you have.

### 1.4 Draft the CV

**Header:** name, target job title (matching the JD title), contact lines, right-to-work statement.

**Summary** (read in 30 seconds; a capability statement, not a case study). Three moves in one paragraph:
1. Who I am (role identity, years, sectors)
2. What sets me apart (a working habit or strength, described as behaviour)
3. What value I bring to this role

Rules: no specific cases or project names, no achievement figures (those live in Experience; years of experience are fine), never a summary of the bullets below.

Example (fictional):
> Customer operations specialist with seven years in payments and B2B software, most recently the only operations specialist covering the UK and Ireland for a card-issuing platform. My work has always sat where a small error reaches someone's money, and I am usually the one who finds it: I review my own case log daily and follow anything that does not look right until the cause is proven and fixed. I keep cases open until they close, chasing counterparties myself rather than passing the problem on, and I explain where a case stands in plain language. I am applying to bring that discipline and ownership to an operation where every case carries a deadline and a customer waiting on the other side.

**Skills & Tools:** up to **9** items, chosen for the JD, using the JD's own wording where truthful (ATS keyword match). Only tools the candidate has actually used. Laid out as a three-column table (3 items per column).

**Experience** (reverse chronological):
- **Most recent or most relevant role: 7 or more bullets** of relevant achievements or duties. For a newly formed team or a broad role, more bullets are acceptable to show range.
- **Every other role: 1 bullet** summarising the duties.
- Bullet formula (Google XYZ): *Accomplished [X], as measured by [Y], by doing [Z]*, or the action-first variant *[Did Z] to [achieve X], [measured by Y]*.
  - e.g. "Built and trained a six-person outsourced support team for EU payment operations, holding a 98% SLA attainment rate."
- Bullets without a real metric keep a concrete outcome rather than an invented number.

**Education** and **Training / Certifications** at the end.

### 1.5 Build the .docx
Write the CV content as JSON (see `examples/cv_example.json` for the shape), then run:

```bash
pip install python-docx   # if missing
python scripts/build_cv.py content.json "Full Name 2026 CV - Job Title (Company).docx"
```

Add `--compact` if the second page holds only Education / Training. The script applies `references/formatting-standard.md`; no template file is needed. Then run the ATS checks in that file, render to PDF and look at every page before moving on.

---

## Stage 2: Review and rewrite

Act as a **talent acquisition partner and hiring manager** for this role.

### Stage 2.1 ATS analysis
Score each item **1 to 10** (10 = perfect match) in three sections:
1. **JD-listed minimum requirements**
2. **All other JD duties and requirements**
3. **Common requirements for this industry / role family** (not in the JD but expected)

Present each section as a table: `Item | Score | Evidence in CV | Suggestion (required if score < 5)`.

### Stage 2.2 Human review
Act as a **senior HR manager who screens 200 CVs a day**. State:
- What catches the eye in the first 6 to 10 seconds
- What gets skipped, and why
- The single biggest risk of rejection

### Pass / fail gate
- **Pass** if more than 80% of all items score above 8, **or** every Section 1 (minimum requirement) item scores above 8. Deliver the final .docx for the candidate's review.
- **Fail** otherwise: return to Stage 1, fix the weak items (asking the candidate for missing facts where needed), rebuild and review again.

---

## Stage 3: Cover letter (only on request)

Use the `business-writing` skill if it is available.

- **Length:** 250 to 400 words, one page maximum
- **Opening:** name the exact role and give a one-line reason the candidate fits. A reader should get the whole letter from this paragraph in 10 seconds.
- **Body (1 to 2 paragraphs):** one or two key achievements that match the JD. Do not repeat CV figures; give the context, the problem, how the candidate solved it and the value added.
- **Company fit:** why this organisation and this industry, grounded in something specific (product, market position, recent news).
- **Closing:** restate interest, thank the reader, ask for an interview.
- **Sign-off:** "Sincerely," followed by the candidate's full name.
- Every paragraph leads with its main point. Disclose a material gap here if the candidate wants it addressed upfront.

---

## Stage 4: Interview preparation (only on request)

### Self-introduction (Present, Past, Future)
- **Present:** how the latest role prepares the candidate for this job
- **Past:** earlier experience (including other countries or industries) that adds relevant evidence
- **Future:** what the candidate is looking for and why this job

### Must-prepare questions
- Why this company?
- Why you?
- **Five behavioural questions** likely for this role, each answered as:
  - **An opening statement** that answers the question directly
  - **A STAR story** (Situation, Task, Action, Result) that proves the statement, clearly sectioned so the listener can follow
  - The candidate's own influence: what would have happened without them
- Questions for the candidate to ask the interviewer, each with a follow-up question to keep the conversation going

### Gap handling
For domain gaps, use a "same discipline, different domain" answer: name the transferable method, then the evidence of fast ramp-up in a previous move.

---

## Deliverables checklist

- [ ] Gap analysis with questions answered by the candidate
- [ ] CV .docx passing the formatting and ATS checks, visually verified
- [ ] Stage 2.1 score tables and Stage 2.2 commentary, gate passed
- [ ] (On request) cover letter .docx
- [ ] (On request) interview kit
