---
name: case-writer-god-mode
description: Full autonomous orchestration of the 6-phase case-writer pipeline. Runs case-writer-research, case-writer-plan, case-writer-draft, case-writer-teach, case-writer-audit, and case-writer-publish in sequence with autonomous default decisions. Pauses only at two HARD gates — source-minimum verification (after research) and final publication confirmation. Skips Exploratory and Series case types (too complex for autonomous decisions). Use when the user wants an end-to-end case generated from a single input prompt with minimal interaction.
license: MIT
---

# case-writer-god-mode — Full Autonomous Pipeline

> Orchestrates all 6 phases. Pauses only at two points: source-minimum verification (Phase 1) and final publication confirmation (Phase 6).

## When to use

The user supplies a topic, URL, or "Company / Event / Year" and asks for a complete case packet without per-phase interaction. Typical phrasings: *"god-mode this,"* *"run the whole pipeline,"* *"generate the case end-to-end."*

This skill does NOT inline the procedures of the six phase skills. It **orchestrates** them — delegates to each phase skill in order with autonomous override flags. The phase skills must be loaded from the same skill repo (which they will be if the host MCP client connected to this repo's URL).

## Output

Complete case packet at `${CASE_OUTPUT_DIR:-./cases}/{slug}/` with spec status `PUBLISHED`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md` — promoted patterns. Apply throughout.
2. If `./case-writer-learnings.md` exists, load it.

## References to Load (cross-phase)

These are needed across all phases. Load once at the start so the procedures don't waste tokens reloading:
- `references/status-definitions.md`
- `references/source-credibility.md`
- `references/case-type-taxonomy.md`
- `references/case-spec-template.md`
- `references/decision-point-design.md`
- `references/difficulty-calibration.md`
- `references/opening-protocol.md`
- `references/hedging-protocol.md`
- `references/writing-standards.md`
- `references/exhibit-design.md`
- `references/anti-patterns.md`
- `references/teaching-note-protocol.md`

---

## Autonomous Overrides

These decisions are made automatically in lieu of user interaction:

| Decision | God-mode override |
|----------|-------------------|
| Case type selection | Highest-scoring on the `references/case-type-taxonomy.md` flowchart — first match wins |
| Protagonist selection | Highest-authority named individual with ≥ 3 Tier 1–2 sourced quotes |
| Case Architecture | Mode A (Pure Interrupted), The Weight freeze style, 4 TN options, Standalone A. Plan 4 options for TN Section 5a — never in case body. |
| Difficulty level | Set per `references/difficulty-calibration.md` criteria |
| Teaching plan duration | 75 minutes |
| MEDIUM audit issues | Auto-approve all proposed fixes (logged in summary) |
| Research Sufficiency Gate | Skip the user gate but still run the evaluation. Log warnings. **Halt if 2+ FAIL dimensions.** |
| QG1 (spec approval) | Auto-approve |

---

## God-Mode Restrictions

- **Does NOT run for Exploratory or Series case types.** Both have structural ambiguity that autonomous decisions can't resolve responsibly. If the flowchart recommends either, HALT and ask the user to select a different type or run the pipeline interactively (one phase at a time).
- **Does NOT self-approve the source-minimum check.** If sources are below threshold after research, HALT.

---

## Pipeline Execution

Delegate to each phase skill in order. The phase skills enforce their own status gates and self-validation checklists; god-mode just supplies the autonomous flags and passes control through.

### Phase 1 — Research

Invoke the **`case-writer-research`** skill with the user's input and an `autonomous=true` flag. The skill should:
- Run all of its steps as defined
- Auto-confirm protagonist + case-type recommendation (no user gate)
- Run the Research Sufficiency Gate evaluation but skip the user gate; HALT only if 2+ FAIL dimensions

**HARD PAUSE 1 — Source Minimum Check.**
After research returns, if the registry contains fewer than 10 sources or fewer than 2 Tier 1–2 sources, HALT and report:

```
Source count is insufficient for autonomous generation.
  Total sources:    [N] / 10 minimum for god-mode
  Tier 1–2 sources: [N] / 2 minimum for god-mode

Please provide additional source URLs or confirm proceeding with the available material.
```

### Phase 2 — Plan

Invoke **`case-writer-plan`**. Auto-select Case Architecture defaults (Mode A, The Weight, 4 options, Standalone A) and auto-approve QG1.

### Phase 3 — Draft

Invoke **`case-writer-draft`**. Run all inline validation. Fix any failures from Step 3.8 HBS Readiness Self-Check automatically.

### Phase 4 — Teach

Invoke **`case-writer-teach`**. Auto-expand to meet the TN ratio if necessary.

### Phase 5 — Audit

Invoke **`case-writer-audit`**. Auto-approve all MEDIUM findings (count them for the publication summary).

### Phase 6 — Publish

Invoke **`case-writer-publish`** through Step 6.2 (verification). **Then pause for HARD PAUSE 2 before running Step 6.3 (registry update) and Step 6.4 (status update).**

**HARD PAUSE 2 — Publication Gate.**

```
Ready to publish [Case Title] ([N] pages case + [Y] pages TN) as GBA [YYYY-NNN]?

Files (rendered, not yet registered):
  {slug}-case.pdf            ([X] pages, [N] words)
  {slug}-teaching-note.pdf   ([Y] pages, [N] words, ratio: [N.Nx])

Audit:   [N] HARD auto-fixed, [N] MEDIUM auto-approved
Sources: [N] total, [N] Tier 1–2

Type YES to proceed with publication and case-registry update.
Type CANCEL to stop here — files remain on disk but the registry is not updated.
```

After user confirms, complete `case-writer-publish` Steps 6.3 and 6.4 to update status to PUBLISHED.

---

## Troubleshooting

**Web fetch fails (paywall or 404):** ask the user to paste the article text directly. Store as raw input and proceed.

**Protagonist has insufficient public presence:** report which qualification criteria the candidate fails. Ask the user to confirm a different protagonist or provide additional source URLs.

**Source count below minimum after Phase 1:** run a second targeted search round focusing on regulatory filings, earnings transcripts, or court documents. If still below minimum, HALT.

**WeasyPrint rendering error:** check the HTML for unclosed tags, invalid CSS, or missing character encoding. The canonical templates in `assets/templates/` are known-good — rendering errors typically originate in dynamically generated exhibit HTML.

**Spec not found for a slug:** list contents of `${CASE_OUTPUT_DIR:-./cases}/`. Never create a stub spec to paper over a missing file.

**Case type changes after QG1 approval:** not permitted without re-running `case-writer-plan`. The case type determines TN ratio, section structure, and exhibit count.

**TN length enforcement fails after 3 expansion rounds:** add a final discussion question, expand the epilogue with additional sourced outcome detail, and extend the teaching plan to 90 or 120 minutes.

---

## Self-Validation Checklist (orchestrator-level)

- [ ] **All 6 phase skills invoked in order** — none skipped or merged
- [ ] **Autonomous overrides applied** at each phase as documented in the table above
- [ ] **HARD PAUSE 1 honored** when sources fell below threshold
- [ ] **HARD PAUSE 2 honored** before registry update — no silent publication
- [ ] **No Exploratory/Series autonomous run** — these halt with a recommendation
- [ ] **Final summary** lists HARD auto-fix count, MEDIUM auto-approve count, source counts, page counts, GBA number
- [ ] **Status History contains all 6 transitions** — DRAFT → APPROVED → DRAFTED → TN COMPLETE → AUDITED → PUBLISHED

## Don't

- Do not inline the contents of the phase skills here. This file is an orchestrator. The phase skills are the source of truth for procedure.
- Do not bypass the two HARD PAUSEs. They are the only points where the user retains control in god-mode.
- Do not run god-mode for Exploratory or Series — refuse and recommend interactive mode.
- Do not silently approve MEDIUM audit findings without reporting the count in the publication summary.

## Output

Complete case packet at `${CASE_OUTPUT_DIR:-./cases}/{slug}/`, status `PUBLISHED`.
