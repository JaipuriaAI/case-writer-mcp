---
name: case-writer-plan
description: Phase 2 of the case-writer pipeline. Lock structural decisions for a Harvard-style MBA teaching case — case type, protagonist, ending mode (A Pure Interrupted / B Implied Tension / C Narrative Deliberation / D Structured Fork), temporal-freeze style, options, exhibits, learning objectives, difficulty calibration. Ends with a HARD user-approval gate (QG1) that advances spec status from DRAFT to APPROVED. Use after `case-writer-research` produces a DRAFT spec.
license: MIT
---

# case-writer-plan — Phase 2: Structural Planning & Approval

> Lock all structural decisions — case type, protagonist, decision options, section outline, exhibit plan, learning objectives. No drafting begins until the user explicitly approves this plan.

## When to use

Run after `case-writer-research` has produced a `DRAFT` spec. This skill ends with QG1 — a HARD approval gate — that advances the spec to `APPROVED`. Without `APPROVED`, `case-writer-draft` will refuse to run.

## Output

Updated spec at `${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-spec.md` with `**Status:** APPROVED`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md` — promoted patterns. Apply throughout planning.
2. If `./case-writer-learnings.md` exists, load it. Apply any NEW domain-relevant learnings.

## References to Load

- `references/status-definitions.md` — validate DRAFT status; produce exact error message if wrong
- `references/case-type-taxonomy.md` — structural template for the confirmed case type
- `references/decision-point-design.md` — decision-point quality criteria and option construction rules
- `references/difficulty-calibration.md` — 5-level Bloom-mapped calibration

**Status check:** Read the spec. If `**Status:**` is not `DRAFT`, stop and output the exact error message from `references/status-definitions.md`. Do not proceed.

---

## Step 2.1 — Load Spec and Structural Template

Read the full DRAFT spec. Load the structural template for the confirmed case type from `references/case-type-taxonomy.md`. Display to the user:

```
Structural template for [Case Type]:
  Narrative length: [N–N] pages
  Section structure: [list sections]
  Exhibit count:    [N–N]
  TN ratio:         [N.Nx]
```

Confirm the case type. If the user wants to change it, re-run the selection flowchart against the research material with the new preference.

---

## Step 2.2a — Case Architecture Gate (USER GATE — HARD)

For Decision Case, Critical Incident, and Mini-Case types, present the Case Architecture Gate. All 4 decisions are USER GATES — the pipeline pauses and asks. In `god-mode`, auto-select defaults.

**Gate 1 — Ending Mode (HARD GATE).** Present the 4 modes from `references/decision-point-design.md` with the recommended default based on case type and difficulty:
- **Mode A — Pure Interrupted** (DEFAULT): case ends cold. No options in body. Gragg standard.
- **Mode B — Implied Tension:** one paragraph acknowledges paths without naming them.
- **Mode C — Narrative Deliberation:** protagonist's reported options as sourced prose. Documentary evidence test required.
- **Mode D — Structured Fork:** explicit options box. For scaffolded contexts.

**Gate 2 — Temporal Freeze Style** (Modes A–C only):
- The Clock — deadline-driven urgency
- The Room — physical scene, sensory detail
- The Weight — emotional stakes, consequences (DEFAULT for god-mode)
- The Question — open-ended, reader-facing

**Gate 3 — TN Options Count:**
- 3 options — focused, for 75-minute sessions
- 4 options (DEFAULT) — standard breadth
- 5 options — rich, for 90–120 minute sessions

**Gate 4 — Case Structure:**
- Standalone A case (DEFAULT) — single case file, epilogue in TN
- A + B case pair — Case A = open dilemma, Case B = what happened (distributed after discussion)

Record all 4 decisions in the spec under `## Case Architecture Decisions`.

For Illustrative, Descriptive, Exploratory, and Industry Note: skip Gates 1–2 (no decision fork). Gates 3–4 still apply.

---

## Step 2.2 — Decision Moment Design

For Decision Case, Critical Incident, and Mini-Case types, apply `references/decision-point-design.md`:

**The decision moment:**
- Exact date
- Physical or organizational location
- What the protagonist knows at this moment (KNOWS / DOES NOT KNOW / UNCERTAIN — three columns)
- Irreversibility dimension: what cannot be undone
- Time-pressure mechanism: why the decision cannot be deferred

**Temporal freeze scene design** (per Gate 2 style selection):
- Draft the temporal freeze passage using the selected style template
- For Mode C: verify documentary evidence test for each option (3 conditions in `decision-point-design.md`)
- For Mode D: construct options per existing rules (3–5 options, genuine trade-offs, no dominant option)

**Teaching note options** (per Gate 3 count — TN Section 5a only, never in case body for Modes A–C):
- Each option must be actionable and specific — not "do nothing" vs "act"
- Each option must have genuine costs that make it non-trivially inferior to the others
- No option may be obviously dominant in the protagonist's information state at decision time
- Each option: one-sentence description + 2–3 genuine costs or risks

**For A+B pair** (Gate 4): outline Case B scope — events covered, estimated word count, additional sources needed.

For Illustrative, Descriptive, Exploratory, and Industry Note types: skip this step. These types use an analytical question, not a decision fork.

---

## Step 2.3 — Section Outline

Generate, for the confirmed case type's section structure:
- Section headings matching the case type template
- One-line description of what happens or what data appears in each section
- Word count budget per section (summing to the case type's target narrative length)
- Opening paragraph: draft or refine the opening from the DRAFT spec, validated against `references/opening-protocol.md`:
  - Protagonist named with title in sentence 1
  - Specific date by sentence 2
  - Dilemma surfaced by end of paragraph
  - First sentence ≤ 25 words
  - All past tense

---

## Step 2.4 — Exhibit Plan

For each planned exhibit, specify:
- Sequential exhibit number (determines narrative reference order)
- Descriptive title
- Data to include — specific enough that a reader knows what they'll see
- Primary source from the source registry (source ID)
- Which section first references this exhibit

Confirm: every exhibit is referenced in the narrative; every narrative exhibit reference has a matching exhibit. No orphans in either direction.

---

## Step 2.5 — Teaching Note Outline

Pre-plan using `references/teaching-note-protocol.md`:

**Learning objectives (3–5):**
- Each begins with a Bloom's taxonomy verb
- Must span ≥ 3 Bloom's levels (e.g. Remember, Analyze, Evaluate)
- Objectives must be distinct — each illuminates a different facet

**Discussion questions (4–6):**
- Pair each with a Bloom's level
- Progress from lower to higher Bloom's levels across the sequence
- Each must be answerable from the case material — no outside knowledge required

**Theory connections (3–5):**
- Name the framework, its author(s), and one sentence on how this case illuminates it

**Teaching plan duration:** 75 / 90 / 120 minutes

---

## Step 2.6 — Difficulty Calibration

Using `references/difficulty-calibration.md`, assign a difficulty level 1–5 with explicit rationale referencing the calibration criteria. Record the level in the spec.

---

## Step 2.7 — QG1: Spec Approval (HARD GATE)

Present the complete structural plan. Do not proceed without explicit user approval.

```
QG1 SPEC APPROVAL — Please confirm before approving:

Case:         [Title]
Slug:         [slug]
GBA Number:   [GBA YYYY-NNN]
Case Type:    [type]
Difficulty:   [1–5]
Protagonist:  [name, title, org]
Decision:     [1–2 sentence description]

Case Architecture:
  Ending Mode:     [A / B / C / D]
  Temporal Freeze: [Clock / Room / Weight / Question]
  TN Options:      [3 / 4 / 5]
  Structure:       [Standalone A / A+B Pair]

TN Options (instructor only):
  1. [Option] — [trade-off]
  2. [Option] — [trade-off]
  3. [Option] — [trade-off]
  [4–5 per Gate 3 count]

Sections:             [list with word counts]
Exhibits:             [list N exhibits with titles]
Learning Objectives:  [list, Bloom's levels in brackets]
Teaching Plan:        [N] minutes
Source Count:         [N] / 15 required minimum
Tier 1–2 Sources:     [N] / 3 required minimum

Type APPROVE to lock these decisions and advance the spec to APPROVED status.
Type REVISE [item] to request changes before approval.
```

Do not self-approve. Do not proceed if the user does not respond. QG1 is a HARD GATE.

After approval: update `**Status:** APPROVED`. Append `- APPROVED: [date] — QG1 confirmed by user` to the Status History section.

---

## Self-Validation Checklist

- [ ] **DRAFT status confirmed** before any work began
- [ ] **All 4 architecture gates** recorded in spec under `## Case Architecture Decisions` (or marked N/A for non-decision-fork types)
- [ ] **Decision moment specifies** date, location, KNOWS/DOES NOT KNOW/UNCERTAIN columns, irreversibility, time-pressure mechanism
- [ ] **Section word counts sum** to the case type's target ±10%
- [ ] **No exhibit orphans** — every planned exhibit has a narrative section that references it
- [ ] **Bloom's spread ≥ 3 levels** across learning objectives and discussion questions
- [ ] **Source minimums hold** — registry has ≥ 15 sources, ≥ 3 Tier 1–2, ≤ 25% single-source share. If not, send back to `case-writer-research` for a second search round
- [ ] **QG1 approval received** in the chat — do not advance status without it
- [ ] **Status History line appended** — `- APPROVED: [ISO date] — QG1 confirmed`

## Don't

- Do not skip QG1. Even in god-mode, god-mode auto-approves but still runs the gate. Do not silently advance.
- Do not change case type after QG1 — that invalidates section structure, exhibit count, and TN ratio. Send the user back to research if a fundamental rethink is needed.
- Do not use options-in-body language for Modes A/B/C — those modes deliberately exclude structured options from the case narrative (see AP13 in `references/anti-patterns.md`).
- Do not pad section word counts to hit the target. If the material doesn't support 4,000 words, propose a shorter case type.

## Output

Updated spec with `**Status:** APPROVED`.
