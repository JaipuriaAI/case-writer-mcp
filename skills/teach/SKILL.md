---
name: case-writer-teach
description: Phase 4 of the case-writer pipeline. Write the full teaching note for a Harvard-style MBA teaching case — all 12 mandatory sections (confidential header, summary, learning objectives, key issues, assignment questions, options analysis 5a, discussion questions with model answers, theory connections, teaching plan, board plan, epilogue, methodology disclosure, supplementary reading). Enforces TN tone discipline (banned phrases, no moral verdicts, no asymmetric advocacy) and a length ratio relative to the case body. Use after `case-writer-draft` produces a DRAFTED case.
license: MIT
---

# case-writer-teach — Phase 4: Teaching Note Generation

> Write the full teaching note — all 12 mandatory sections — and ensure it meets or exceeds the case narrative word count at the required ratio.

## When to use

Run after `case-writer-draft` has advanced the spec to `DRAFTED`. Produces the instructor-only teaching note. Output feeds directly into the 6-agent audit (`case-writer-audit`).

## Output

`${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-teaching-note.html` with spec status `TN COMPLETE`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md`.
2. If `./case-writer-learnings.md` exists, load it.

## References to Load

- `references/status-definitions.md` — validate DRAFTED status
- `references/teaching-note-protocol.md` — all 12 mandatory TN sections, board-plan format, length enforcement, **tone discipline**
- `references/difficulty-calibration.md` — Bloom's reference for LO/DQ levels
- `references/anti-patterns.md` — AP3 (Hindsight Contamination) is the central risk in TN

**Status check:** if `**Status:**` is not `DRAFTED`, stop and output the exact error message from `references/status-definitions.md`.

Load the full spec and the generated `{slug}-case.html`. Read the case HTML completely — the TN must reference specific sections, exhibit numbers, and page references accurately.

---

## Step 4.1 — Write All 12 Mandatory TN Sections

Follow `references/teaching-note-protocol.md` for the complete structure. Write in this order:

**1. Confidential Header.** `TEACHING NOTE — CONFIDENTIAL. Not for distribution to students.` Include case title, GBA number, author, date.

**2. Case Summary (100–150 words).** Describe the situation without revealing the protagonist's decision or outcome. A student who reads only this should understand stakes but not resolution.

**3. Learning Objectives (3–5).** Carry forward from the approved spec. Each begins with a Bloom's verb, identifies a specific competency, is tagged with its Bloom's level. Span ≥ 3 distinct Bloom's levels.

**4. Key Issues (3–6 tensions).** Name the central tensions the case surfaces. These are not discussion questions — they are the underlying analytical problems the case illuminates. Format: `**[Tension Name]:** [2–3 sentence description]`.

**5. Assignment Questions (3–5, pre-class).** Fact-based questions answerable from the case material. Each must reference a specific section or exhibit, be answerable without outside research, and be distinct from in-class discussion questions.

**5a. Options Analysis (TN — instructor only).** For Decision Case, Critical Incident, and Mini-Case types, present the full options analysis here. This contains the options deliberately excluded from the case body in Modes A–C. For each option (per Gate 3 count from the spec):
- Option name and one-sentence description
- Supporting evidence from the case
- Genuine costs, risks, and trade-offs
- Stakeholder impact analysis
- Frameworks that inform evaluation of this option

**6. Discussion Questions with Model Answers (4–6).** For each:
- State the question
- Bloom's level in brackets
- Model answer (150–250 words) — cite academic frameworks, not just practical reasoning
- Theory box: `**Theory connection:** [Framework name] ([Author(s)]) — [1–2 sentence application]`
- Facilitation note: `**Facilitation:** [1–2 sentences on how to open this question, what to write on the board, how to sequence student responses]`

Questions must progress from lower to higher Bloom's levels across the sequence.

**7. Theory Connections (3–5 frameworks).** For each:
- Framework name and author(s)
- How this case specifically illuminates the framework (not generic description)
- Recommended reading: one article or book chapter, full citation

**8. Teaching Plan (minute-by-minute).** Cover the full session duration (75/90/120 per spec):
- Opening move (0–5 min) — cold call or opening question
- Section-by-section discussion blocks with minute markers
- Transition language between postures (e.g. fact-gathering → analysis)
- Board work timing
- Debrief and theory connection (final 10 min)

**9. Board Plan (3 panels).**
```
| FACTS | ANALYSIS | RECOMMENDATIONS |
|-------|----------|-----------------|
| [Key facts to surface] | [Frameworks to apply] | [Options and criteria] |
```
Must be usable as a literal teaching guide — a professor should be able to reproduce it from this alone.

**10. Epilogue (what actually happened).** Reveal the protagonist's actual decision and consequences:
- Sourced — every claim has an `[SN]` citation (use the same source registry or add new sources)
- Formatted with a visual separator (gold box / distinct styling)
- Covers: decision made, immediate consequences, longer-term outcomes, stakeholder effects
- Does NOT editorialize — no "wisely decided" or "fatally chose"

**11. Research Methodology Disclosure.** Standard language: "This teaching case was developed entirely from publicly available secondary sources. No interviews were conducted with case participants. The authors cannot verify the completeness of the public record, and instructors should treat all non-sourced characterizations as analytical constructs, not factual claims."

**12. Supplementary Reading (5–8 items).** Mix of academic and practitioner sources. Include at least:
- 2 peer-reviewed articles or book chapters
- 1 practitioner article or case study from a business publication
- 1 data source or primary document relevant to the industry or event

---

## Step 4.2 — Length Enforcement

Count TN words (all 12 sections, excluding the case summary). Count case narrative words (excluding exhibits and source registry).

Required ratio (`references/case-type-taxonomy.md`):
- Decision Case: TN ≥ 1.0× case
- Critical Incident: TN ≥ 1.5×
- Illustrative: TN ≥ 1.0×
- Descriptive: TN ≥ 1.0×
- Exploratory: TN ≥ 1.0×
- Mini-Case: TN ≥ 2.0×
- Series (per part): TN ≥ 1.0×
- Industry Note: TN ≥ 0.5×

If TN falls below the required ratio:
1. Expand model answers — add 50–100 words each, deepen theory connections
2. Expand theory connections — add one more framework with reading recommendation
3. Add a discussion question if fewer than 6 exist
4. Expand the teaching plan — add transition detail and facilitation nuance

Repeat until the ratio is satisfied. Do NOT pad with filler — every added word must teach.

---

## Step 4.3 — HTML Assembly

Read `assets/templates/teaching-note-template.html`. Replace every `{{PLACEHOLDER}}`.

**Cover tokens:** `{{TITLE}}`, `{{CASE_NUMBER}}`, `{{PUBLISH_DATE}}`.

**Learning objective tokens** (repeat for LO_2, LO_3, LO_4, LO_5):
- `{{LO_1_VERB}}` — Bloom's action verb (e.g. "Analyze")
- `{{LO_1_TEXT}}` — objective text following the verb
- `{{LO_1_BLOOM}}` — level label (e.g. "Analyze")
- `{{LO_1_BLOOM_CLASS}}` — CSS class: `bloom-remember`, `bloom-understand`, `bloom-apply`, `bloom-analyze`, `bloom-evaluate`, `bloom-create`

**Key issues / assignment questions:** `{{KEY_ISSUE_N_NAME}}`, `{{KEY_ISSUE_N_DESC}}`, `{{ASSIGN_Q_N}}`.

**Discussion question tokens** (repeat for DQ_2, DQ_3, DQ_4):
- `{{DQ_1_TEXT}}`, `{{DQ_1_BLOOM}}`, `{{DQ_1_BLOOM_CLASS}}`
- `{{DQ_1_ANSWER}}`, `{{DQ_1_THEORY_NAME}}`, `{{DQ_1_THEORY_BODY}}`, `{{DQ_1_FACILITATION}}`

**Theory connections** (repeat for THEORY_2, THEORY_3): `{{THEORY_N_NAME}}`, `{{THEORY_N_AUTHOR}}`, `{{THEORY_N_CONNECTION}}`, `{{THEORY_N_READING}}`.

**Teaching plan:** `{{TEACHING_PLAN_TABLE}}` — render as full `<table>` with columns: Time | Activity | Discussion Focus.

**Board plan:** `{{BOARD_PLAN_PANEL_1/2/3}}` — render as `<ul><li>` lists inside each panel.

**Epilogue / methodology / reading:** `{{EPILOGUE}}`, `{{RESEARCH_METHOD}}`, `{{SUPP_READING}}` (renders as `<li>` items; the `<ol>` wrapper is in the template).

**Note:** Do NOT replace `{{INLINE_CSS}}` — handled by `case-writer-publish` Step 6.1.

Save as `${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-teaching-note.html`.

Update spec: `**Status:** TN COMPLETE`. Append `- TN COMPLETE: [date] — Teaching note generated (TN: [N] words / Case: [N] words, ratio: [N.Nx])` to Status History.

---

## Self-Validation Checklist (TN tone discipline + structure)

Before declaring complete, run these. The original `tn-tone-checker` agent's full procedure is encoded here; if your client exposes a Task / Agent dispatch tool, you may dispatch the inline prompt below instead.

**Banned phrases (HARD — must be 0 hits):**
- "strong students will recognize"
- "the correct answer is"
- "students should conclude"
- "it is clear that"
- "obviously"
- "the right choice"
- "clearly the best"
- "the protagonist should have"
- "the correct approach"
- "without doubt"
- "any reasonable person"
- "the evidence conclusively shows"

For each match, replace per `references/teaching-note-protocol.md` "Replacement Pattern" column.

**Prescriptive conclusions in model answers (MEDIUM):**
- In Section 5a (Options Analysis), check no option is presented as definitively superior without acknowledging counterarguments
- All options receive roughly equal analytical depth — flag asymmetry like 3 paragraphs for Option A vs. 1 for Option B

**Moral verdicts (HARD):**
- Scan for moral/ethical language presented as fact: "ethically wrong," "morally bankrupt," "irresponsible," "reckless," "negligent," "duty to," "obligation to"
- Direct quotes from regulators, courts, or named commentators are exempt
- Reframe as discussion prompts or attribute to a named source

**Advocacy language (MEDIUM):**
- Emotive adjectives applied asymmetrically ("visionary CEO" vs. "stubborn board")
- One-sided framing of consequences ("devastating" for one option, "transformative" for another)
- Rhetorical questions with implied answers
- Selective evidence citation

**Structural integrity:**
- [ ] All 12 mandatory sections present and in the correct order
- [ ] Bloom's levels span ≥ 3 levels across discussion questions
- [ ] Each model answer cites at least one academic framework
- [ ] Board plan has 3 panels with content in each
- [ ] Epilogue is fully sourced — every outcome claim has `[SN]`
- [ ] TN word count meets or exceeds the case-type required ratio
- [ ] Methodology disclosure present with the standard language
- [ ] Supplementary reading ≥ 5 items including ≥ 2 peer-reviewed
- [ ] Status History line appended

**Optional: dispatch as a sub-agent.** If your client has a Task tool, you can run this audit as a sub-agent with the prompt:

> *You are the TN Tone Checker. Read the teaching note at the path provided. Run all 4 categories above (banned phrases, prescriptive conclusions, moral verdicts, advocacy language). Return a structured findings report with location + exact phrase + suggested rewrite for each issue. Do not modify the document.*

Otherwise, run the procedure inline in your own context.

## Don't

- Do not write a TN that prescribes "the right answer." Cases don't have right answers — instructors do.
- Do not editorialize in the epilogue. Report the decision and consequences with sources; let the framework analysis happen elsewhere.
- Do not let one option dominate Section 5a. If you find yourself writing more about Option A than Option B, audit the asymmetry — that's how an instructor's bias enters the classroom.
- Do not invent supplementary reading. Every recommended item must exist and be locatable.
- Do not pad to hit the ratio. Add depth, not filler.

## Output

`${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-teaching-note.html` with spec status `TN COMPLETE`.
