# Status Definitions
**Version:** 1.0.0
**Loaded by:** All commands — validate case status before proceeding

Every command checks status before running. Wrong status = prescriptive error message. Do not guess or override — enforce the state machine exactly as defined here.

---

## Status State Machine

```
[Input] → :research → DRAFT
DRAFT   → :plan (QG1 — HARD GATE, user confirmation required) → APPROVED
APPROVED → :draft → DRAFTED
DRAFTED  → :teach → TN COMPLETE
TN COMPLETE → :audit (QG2 — HARD GATE, all 6 agents must pass) → AUDITED
AUDITED  → :publish → PUBLISHED
```

No command may skip a stage. A case cannot go from DRAFT directly to DRAFTED, or from APPROVED directly to AUDITED. The pipeline is sequential.

---

## Status Definitions

| Status | Set By | Meaning | Accepted By |
|--------|--------|---------|-------------|
| `DRAFT` | `:research` | Research complete, spec exists, no structural decisions locked | `:plan` only |
| `APPROVED` | `:plan` at QG1 (requires explicit user confirmation) | All structural decisions locked: case type, protagonist, options, outline, exhibit plan, learning objectives | `:draft` only |
| `DRAFTED` | `:draft` | Case HTML generated, all exhibits included, source registry complete | `:teach` only |
| `TN COMPLETE` | `:teach` | Teaching note HTML generated, TN word count ≥ case narrative word count | `:audit` only |
| `AUDITED` | `:audit` at QG2 (all 6 agents must pass) | All quality gates passed, all HARD anti-patterns resolved, MEDIUM issues approved by user | `:publish` only |
| `PUBLISHED` | `:publish` | PDFs generated, case packet complete | Terminal — no further commands |

---

## Wrong-Status Error Messages

When a command is invoked on a case with the wrong status, stop immediately and produce the appropriate error below. Do not proceed with generation. Do not offer workarounds.

---

**`:plan` on a non-DRAFT spec:**
```
ERROR: This case spec has status `[STATUS]`. `:plan` only accepts `DRAFT` specs.

If status is `APPROVED`: The spec has already been approved. Run `/case-writer:draft [slug]` to generate the case narrative.
If status is `DRAFTED` or later: The case is already in progress. Re-running `:plan` would overwrite approved decisions. If you need to restructure, start a new spec or contact your supervisor.
```

**`:draft` on a non-APPROVED spec:**
```
ERROR: This case spec has status `[STATUS]`. `:draft` only accepts `APPROVED` specs.

If status is `DRAFT`: Run `/case-writer:plan [slug]` to finalize structural decisions (case type, protagonist, options, exhibit plan) and receive approval before drafting.
If status is `DRAFTED`: The case has already been drafted. Run `/case-writer:teach [slug]` to generate the teaching note.
If status is `TN COMPLETE` or later: The case is past the draft stage. See the pipeline map in `status-definitions.md`.
```

**`:teach` on a non-DRAFTED spec:**
```
ERROR: This case spec has status `[STATUS]`. `:teach` only accepts `DRAFTED` specs.

If status is `APPROVED`: Run `/case-writer:draft [slug]` first to generate the case narrative before writing the teaching note.
If status is `TN COMPLETE`: The teaching note has already been generated. Run `/case-writer:audit [slug]` to audit the complete case packet.
If status is `DRAFT`: Run `/case-writer:plan [slug]` → then `:draft` → then `:teach` in sequence.
```

**`:audit` on a non-TN-COMPLETE spec:**
```
ERROR: This case spec has status `[STATUS]`. `:audit` only accepts `TN COMPLETE` specs.

If status is `DRAFTED`: Run `/case-writer:teach [slug]` to generate the teaching note before auditing. The audit reviews both the case narrative and the teaching note together.
If status is `AUDITED`: The case has already passed audit. Run `/case-writer:publish [slug]` to generate the final case packet.
If status is `APPROVED` or earlier: Complete the pipeline in sequence: `:draft` → `:teach` → `:audit`.
```

**`:publish` on a non-AUDITED spec:**
```
ERROR: This case spec has status `[STATUS]`. `:publish` only accepts `AUDITED` specs.

All 6 audit agents must pass before publishing. Run `/case-writer:audit [slug]` to audit the case. Every HARD anti-pattern must be resolved. Every MEDIUM issue must be reviewed and approved by the user. Only then will status advance to `AUDITED`.

Publishing unaudited cases violates academic integrity standards.
```

---

## Quality Gate Definitions

### QG1 — Spec Approval (Hard Gate)
**Triggered by:** `:plan`, at the end of the structural planning phase
**Type:** HARD — requires explicit user confirmation before proceeding
**Blocks:** `:draft` will not run without APPROVED status

Present the user with a summary of all locked decisions and ask for explicit confirmation. The confirmation message must include:

```
QG1 SPEC APPROVAL — Please confirm the following before approving:

Case: [Title]
Slug: [slug]
Case Type: [type]
Difficulty: [1-5]
Protagonist: [name, title, org]
Decision Point: [1-2 sentence description]
Options: [list 3-5 options]
Exhibit Plan: [N exhibits, titles listed]
Learning Objectives: [list, confirm Bloom's levels span 3+ levels]
Source Count: [N sources / 15 required minimum]
Tier 1-2 Sources: [N / 3 required minimum]

Type APPROVE to lock these decisions and advance to DRAFTED status.
Type REVISE [item] to request changes before approval.
```

Only advance to APPROVED after the user types APPROVE (or an equivalent explicit confirmation). Do not self-approve.

After approval: Update spec header to `**Status:** APPROVED`. Record approval date in Status History.

---

### QG2 — Audit Gate (Hard Gate)
**Triggered by:** `:audit`, after all 6 agents complete their passes
**Type:** HARD — all 6 agents must return PASS before advancing
**Blocks:** `:publish` will not run without AUDITED status

**The 6 audit agents:**
1. Agent 1 — Source Integrity: Verifies source registry, citation density, CRAAP scores, single-source share
2. Agent 2 — Factual Accuracy: Verifies all stated facts against sources, flags unverifiable claims
3. Agent 3 — Narrative Quality: Checks anti-patterns AP1-AP12, writing standards, temporal integrity
4. Agent 4 — Teaching Note Quality: Verifies all 12 TN sections exist, length rule satisfied, Bloom's progression
5. Agent 5 — Exhibit Integrity: Checks AP7 (exhibit orphaning), verifies all data is sourced
6. Agent 6 — Final Anti-Pattern Sweep: Comprehensive pass over all 12 anti-patterns, full document review

**HARD issues (any of these blocks AUDITED status):**
- Any HARD anti-pattern flagged and not yet resolved: AP1, AP2, AP3, AP4, AP5, AP7, AP8, AP10, AP12
- Source registry below 15 sources
- Fewer than 3 Tier 1-2 sources
- Single source exceeding 25% share
- Teaching note shorter than case narrative
- Any section of teaching note missing

**MEDIUM issues (flags for user review — user may approve or request fix):**
- AP6 (Temporal Confusion), AP9 (Present Tense Narration), AP11 (Missing Attribution)
- Minor phrasing issues in learning objectives
- Supplementary reading list under 5 items

**After QG2 resolution:**
- All HARD issues: must be fixed, then re-audited
- MEDIUM issues: present list to user. User approves each or requests fix. After all MEDIUM issues resolved or approved, advance to AUDITED.
- Update spec header to `**Status:** AUDITED`. Record audit completion date in Status History.

---

## Re-running Commands

Some commands can be re-run on later-stage specs. When re-running, reset status as specified.

| Command | Acceptable Statuses | Status After Re-run | Note |
|---------|--------------------|--------------------|------|
| `:plan` | DRAFT only | Remains DRAFT until QG1 | Cannot re-run on APPROVED or later |
| `:draft` | APPROVED or DRAFTED | Resets to DRAFTED | Forces re-audit — status advances no further without re-running `:teach` and `:audit` |
| `:teach` | DRAFTED or TN COMPLETE | Resets to TN COMPLETE | Forces re-audit — `:audit` must re-run |
| `:audit` | TN COMPLETE or AUDITED | AUDITED (if passes) | Can re-run to fix issues from previous audit cycle |
| `:publish` | AUDITED only | PUBLISHED | Terminal — cannot be undone |

When resetting status on a re-run, update the spec header and append a note to the Status History section:
`- [STATUS] reset: [DATE] — [reason for re-run, e.g., "Narrative restructured, re-audit required"]`

---

## Status Annotation in Spec File

The spec file header must always reflect current status. Update this field every time status changes:

```markdown
**Status:** DRAFT
```

Valid values: `DRAFT` | `APPROVED` | `DRAFTED` | `TN COMPLETE` | `AUDITED` | `PUBLISHED`

The Status History section at the bottom of the spec must log every transition:

```markdown
## Status History
- DRAFT: [date] — Initial research complete
- APPROVED: [date] — QG1 confirmed by user
- DRAFTED: [date] — Case narrative generated
- TN COMPLETE: [date] — Teaching note generated (TN: [N] words / Case: [N] words)
- AUDITED: [date] — All 6 agents passed, [N] MEDIUM issues approved by user
- PUBLISHED: [date] — Case packet generated
```
