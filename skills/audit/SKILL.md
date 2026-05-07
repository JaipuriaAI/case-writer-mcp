---
name: case-writer-audit
description: Phase 5 of the case-writer pipeline. Run 6 parallel audit roles over a complete case packet — source integrity, narrative quality, decision moment, exhibits, teaching-note depth, and the AP1–AP15 anti-pattern scanner. HARD findings auto-fix or block publication; MEDIUM findings require user approval. Use after `case-writer-teach` produces a TN COMPLETE case.
license: MIT
---

# case-writer-audit — Phase 5: 6-Role Audit & Rectification

> 6 parallel audit roles evaluate the complete case packet. HARD issues block publication. MEDIUM issues require user approval. All issues must be resolved before status advances to `AUDITED`.

## When to use

Run after `case-writer-teach` has advanced the spec to `TN COMPLETE`. This is the last quality gate before publication. Without `AUDITED`, `case-writer-publish` will refuse to render PDFs.

## Output

Rectified `{slug}-case.html` and `{slug}-teaching-note.html`, spec status `AUDITED`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md`.
2. If `./case-writer-learnings.md` exists, load it. Apply NEW learnings.

## References to Load

- `references/status-definitions.md` — validate TN COMPLETE; all 6 role definitions (HARD/MEDIUM classifications)
- `references/anti-patterns.md` — all 15 anti-patterns with detection heuristics
- `references/source-credibility.md` — source minimum thresholds for Role 1
- `references/teaching-note-protocol.md` — 12-section TN spec for Role 5
- `references/opening-protocol.md` — opening rules for Role 2
- `references/writing-standards.md` — prose and tense standards for Role 2

**Status check:** if `**Status:**` is not `TN COMPLETE`, stop and output the exact error message from `references/status-definitions.md`.

---

## Step 5.1 — Run 6 Audit Roles

Each role has full text of both `{slug}-case.html` and `{slug}-teaching-note.html` in scope.

> **Parallelism:** if your client exposes a Task / Agent / sub-agent dispatch tool, run all 6 roles in parallel using the prompts below as separate agent invocations. Each prompt is self-contained — no shared state needed between agents until rectification.
>
> If your client has no parallel-dispatch tool, run all 6 sequentially in this context. The procedures are identical; only wall-clock time differs.

---

### Role 1 — Source Integrity Auditor

**Inputs:** the complete case body and TN; `references/source-credibility.md`.

**Check criteria:**
- [ ] Total sources ≥ 15 (or ≥ 8 for Mini-Case)
- [ ] Tier 1–2 sources ≥ 3
- [ ] No single source exceeds 25% of all narrative `[SN]` citations
- [ ] Every direct quote in the narrative traces to a source registry entry — no ghost quotes (AP12)
- [ ] Key factual claims with specific metrics or durations have ≥ 2 independent sources
- [ ] No red-flag sources: unattributed "industry sources," clearly promotional material, sources failing 3+ CRAAP criteria

**Return:** PASS, or a list of issues tagged HARD (blocks publication) or MEDIUM (user review required).

---

### Role 2 — Narrative Quality Auditor

**Inputs:** the case body; `references/writing-standards.md`; `references/opening-protocol.md`; case-type target word count from `references/case-type-taxonomy.md`.

**Check criteria:**
- [ ] Opening paragraph: protagonist named, specific date present, dilemma surfaced within 3 sentences (AP5)
- [ ] First sentence of opening ≤ 25 words
- [ ] All narrative in past tense — present tense only inside quotation marks (AP9)
- [ ] No editorializing: evaluative adjectives without attribution
- [ ] No passive voice runs (3+ consecutive passive constructions)
- [ ] No jargon without in-text definition for international-audience terms
- [ ] Narrative word count within ±15% of the case type target
- [ ] No run of 3+ consecutive paragraphs without an `[SN]` citation

**Return:** PASS, or issues tagged HARD/MEDIUM with specific locations (section name + approximate paragraph).

---

### Role 3 — Decision Moment Auditor

**Inputs:** the case body, the spec's `## Case Architecture Decisions` section; `references/decision-point-design.md`.

For Decision Case, Critical Incident, Mini-Case (skip for other types):

**Mode A (Pure Interrupted):**
- [ ] Case ends at temporal freeze with genuine uncertainty
- [ ] No structured options box, "Options Available to [Name]" header, or Option A/B/C enumeration (AP13 — HARD)
- [ ] No enumerated alternatives of any kind in the final section

**Mode B (Implied Tension):**
- [ ] Same as Mode A checks
- [ ] One implied-tension paragraph present (2–4 sentences acknowledging paths without naming them)
- [ ] No specific paths, counts, or option names in the implied paragraph

**Mode C (Narrative Deliberation):**
- [ ] Each narrative-embedded option cites a Tier 1–2 source (documentary evidence test)
- [ ] No "Option A/B/C" labels or structured format
- [ ] Options woven as prose, not as a list or formatted section

**Mode D (Structured Fork):**
- [ ] 3–5 distinct options present with balanced rhetorical weight (AP1, AP10)
- [ ] Every option has genuine, non-trivial costs — no strawman alternatives

**All modes:**
- [ ] Time-pressure mechanism is named and specific
- [ ] Case narrative ends at the decision point — no post-decision narrative, outcomes, or consequences (AP3)
- [ ] The protagonist demonstrably had authority to make this decision
- [ ] Temporal freeze conveys stakes and irreversibility (Modes A–C)
- [ ] Teaching Note Section 5a contains full options analysis

**Return:** PASS, or issues tagged HARD/MEDIUM.

---

### Role 4 — Exhibit and Data Auditor

**Inputs:** the case body and exhibits; `references/exhibit-design.md`.

**Check criteria:**
- [ ] Exhibit numbers are sequential and match their order of first narrative reference (AP7)
- [ ] Every exhibit has a source line
- [ ] No orphaned exhibits (exhibit exists but is never referenced in narrative) — AP7
- [ ] No phantom exhibit references (narrative references an exhibit that does not exist) — AP7
- [ ] Financial data: raw numbers present alongside any percentages
- [ ] Temporal consistency: all data points have specific dates; no anachronistic data in pre-decision sections
- [ ] Data is formatted for student analysis — structured for interpretation, not just presented

**Return:** PASS, or issues tagged HARD/MEDIUM with exhibit numbers.

---

### Role 5 — Teaching Note Depth Auditor

**Inputs:** the teaching note; `references/teaching-note-protocol.md`.

**Check criteria:**
- [ ] All 12 mandatory TN sections present (Confidential header, Summary, Learning Objectives, Key Issues, Assignment Questions, **Options Analysis (5a)**, Discussion Questions, Theory Connections, Teaching Plan, Board Plan, Epilogue, Methodology Disclosure, Supplementary Reading)
- [ ] TN word count ≥ case narrative × the required ratio for this case type
- [ ] Bloom's levels span ≥ 3 levels across discussion questions
- [ ] Each discussion question model answer cites academic literature
- [ ] Board plan present with 3 panels: FACTS, ANALYSIS, RECOMMENDATIONS
- [ ] Assignment questions (pre-class) are distinct from discussion questions (in-class)
- [ ] Research methodology disclosure section present with the standard language
- [ ] Supplementary reading ≥ 5 items, including ≥ 2 peer-reviewed sources
- [ ] Epilogue is sourced — all outcome claims have `[SN]` citations

**Also run the inline TN tone-discipline procedure** (banned phrases, prescriptive conclusions, moral verdicts, advocacy language) from `case-writer-teach`'s Self-Validation Checklist. The procedure can be dispatched as a Task / Agent if available; otherwise execute inline.

**Return:** PASS, or issues tagged HARD/MEDIUM.

---

### Role 6 — Anti-Pattern Scanner

**Inputs:** both case body and TN; `references/anti-patterns.md`.

Run the detection heuristic for all 15 anti-patterns:

| AP | Name | Severity |
|----|------|----------|
| AP1 | Dominant Option | HARD |
| AP2 | Manufactured Urgency | HARD |
| AP3 | Hindsight Contamination | HARD |
| AP4 | Single-Source Syndrome | HARD |
| AP5 | Opaque Opening | HARD |
| AP6 | Temporal Confusion | MEDIUM |
| AP7 | Exhibit Orphaning | HARD |
| AP8 | Strawman Options | HARD |
| AP9 | Present-Tense Narration | MEDIUM |
| AP10 | Rhetorical Tilt | HARD |
| AP11 | Missing Attribution | MEDIUM |
| AP12 | Ghost Quotes | HARD |
| AP13 | Structured Options in Case Body | HARD (Modes A–C) / N/A (Mode D) |
| AP14 | Theory Vocabulary in Case Body | HARD |
| AP15 | Protagonist Dilution | MEDIUM |

For each finding, output:
- AP code, severity
- File (case body / TN), section, paragraph
- Exact phrase or excerpt
- Suggested fix

Cross-check with Role 3 findings to avoid duplicate issues. AP3 requires reading both case body and TN epilogue.

**Return:** PASS, or list of identified anti-patterns.

**Inline anti-pattern auditor prompt** (use as a sub-agent if available):

> *You are the Anti-Pattern Auditor. Load `references/anti-patterns.md` for the AP1–AP15 definitions and detection heuristics. Read the case body and TN at the paths provided. For each AP, run its detection heuristic and report all findings with location, exact text, severity, and a concrete suggested fix. Group related findings under one heading. Do not modify the documents.*

---

## Step 5.2 — Rectification

After all 6 roles return:

**Compile all HARD issues across all roles.**

**Tier-1 auto-fixes** (apply immediately without user confirmation):
- AP9 present-tense narration → convert to past tense
- AP6 temporal confusion → add transitional date phrases to clarify sequence
- AP11 missing attribution → add hedging language from `references/hedging-protocol.md`
- Exhibit numbering out of sequence → renumber to match order of first narrative reference
- Source-citation formatting errors → reformat to match registry convention

**After auto-fixes, re-check for remaining HARD issues.** For each remaining HARD issue:
- Implement the correction directly (do not ask the user — HARD issues must be fixed)
- If the fix requires a judgment call (e.g. replacing a dominant option requires generating new option content), make the best editorial correction and flag it in the resolution log

**For MEDIUM issues, present to the user:**

```
The following MEDIUM issues were identified and require your review:

[AP6 | Role 2 | Location: Section 3, paragraph 2]
[Description of issue]
→ Proposed fix: [specific fix]

[AP11 | Role 6 | Location: Opening paragraph]
[Description of issue]
→ Proposed fix: [specific fix]

Type APPROVE to accept all proposed fixes and advance to AUDITED.
Type FIX [issue number] to request a different resolution for that item.
```

**Maximum 3 rectification cycles.** If HARD issues persist after 3 cycles, stop and present a diagnostic: which anti-pattern remains, why auto-fix can't resolve it, what human editorial intervention is required.

---

## Step 5.3 — Auto-Capture Learnings

After rectification, capture novel findings to `./case-writer-learnings.md` in the working directory:

For each HARD or recurring MEDIUM issue that was fixed:
1. Check if a similar correction already exists in `references/known-corrections.md`
2. If not, append:

```markdown
### [date] | audit | [slug]
**Correction:** [What was wrong]
**Rule:** [The corrective rule]
**Applies to:** [Which phase/step]
**Status:** NEW
```

After all HARD issues resolved and MEDIUM issues approved: update spec `**Status:** AUDITED`. Append `- AUDITED: [date] — All 6 roles passed, [N] HARD auto-fixed, [N] MEDIUM issues approved by user` to Status History.

---

## Self-Validation Checklist

- [ ] **TN COMPLETE status confirmed** before any audit work began
- [ ] **All 6 roles completed** — none skipped, even when roles overlap (e.g. Role 3 + Role 6 both touch decision moment)
- [ ] **All HARD findings resolved** — auto-fixed or directly corrected
- [ ] **All MEDIUM findings either approved by user or fixed**
- [ ] **No new anti-patterns introduced** by the rectification itself — re-scan after corrections
- [ ] **Rectification did not exceed 3 cycles** — if it did, the case has structural issues that require human editorial work
- [ ] **Novel learnings captured** to `./case-writer-learnings.md` if new patterns emerged
- [ ] **Status History line appended** — `- AUDITED: [ISO date] — [counts]`

## Don't

- Do not silently approve MEDIUM findings on behalf of the user — present them and wait for explicit approval (god-mode is the only exception, and even there the count must be reported in the final summary)
- Do not introduce new HARD violations while fixing existing ones — re-scan after every rectification round
- Do not advance status to AUDITED while any HARD issue remains
- Do not skip any of the 6 roles, even when one role's findings make another seem redundant — overlapping checks catch errors that single passes miss

## Output

Rectified `{slug}-case.html` and `{slug}-teaching-note.html`, spec status `AUDITED`.
