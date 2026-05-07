# Learnings Protocol — Case Writer Self-Evolution

> Loaded by `:learn`. Referenced by `:draft` and `:audit` for auto-capture.

---

## Lifecycle

```
CAPTURE → STAGE → PROMOTE → ENFORCE
   ^                           |
   └───── new findings ────────┘
```

- **Capture:** Draft/audit findings auto-written to `.claude/case-writer-learnings.md`
- **Stage:** Entries sit as `Status: NEW`, visible at `:learn` checkpoint
- **Promote:** When recurrence >= 2 across different cases, propose promotion
- **Enforce:** Promoted corrections embed in `shared/known-corrections.md`, loaded every session

## File Locations

| File | Purpose | Tracked in git? |
|------|---------|----------------|
| `.claude/case-writer-learnings.md` | Per-project correction log | YES |
| `.claude/case-writer-learnings.jsonl` | Per-user staging area | NO (.gitignore) |
| `shared/known-corrections.md` | Promoted corrections, loaded every session | YES (plugin source) |

## Error Taxonomy

Each finding is classified by domain prefix:

| Domain Prefix | Description | Examples |
|---------------|-------------|----------|
| `ap_theory_vocabulary` | AP14: Theory terms in case body | "structural holes", "epistemic authority" |
| `ap_protagonist_dilution` | AP15: Protagonist < 60% of paragraphs | Secondary characters dominate narrative |
| `ap_options_in_body` | AP13: Structured options in Mode A-C | Options box in interrupted case |
| `ap_dominant_option` | AP1: One option framed as superior | Rhetorical tilt toward preferred choice |
| `ap_hindsight` | AP3: Post-decision information in narrative | Outcomes revealed before decision point |
| `ap_ghost_quote` | AP12: Unattributed or fabricated quotes | Quote not traceable to source registry |
| `source_hedging` | Unhedged private company financials | "$500M revenue" without attribution |
| `source_credibility` | Source tier violations or insufficiency | Single-source share > 25% |
| `source_ghost_citation` | Non-existent study or report | "2024 Deloitte survey" not found |
| `tn_tone` | Teaching note neutrality violations | Prescriptive conclusions, moral verdicts |
| `tn_completeness` | Missing TN sections or ratio failure | Epilogue unsourced, ratio < 1.0x |
| `narrative_tense` | Present tense outside quotes | AP9 violations |
| `narrative_editorializing` | Evaluative language without attribution | "The disastrous decision" |
| `exhibit_integrity` | Orphaned exhibits or numbering errors | AP7 violations |
| `decision_design` | Mode compliance, temporal freeze quality | Wrong ending mode for spec |
| `factual_arithmetic` | Math errors in comparisons | "Seven times" when actual is 24.9x |
| `factual_currency` | Wrong currency denomination | LRS = USD not INR |
| `factual_attribution` | Wrong person credited with action | Andrew Chen vs Kevin Frisch |
| `factual_reputational` | Named person with legal/reputational issues | Dan Price assault charges |

## Entry Format (.md)

```markdown
### {date} | :{command} | {slug}
**Correction:** {what was wrong}
**Rule:** {the correction to apply going forward}
**Domain:** {domain_prefix}
**Status:** NEW
```

## Entry Format (.jsonl)

```json
{"date":"2026-03-26","command":"draft","slug":"example-slug","domain":"ap_theory_vocabulary","correction":"Used 'structural holes' in case body","rule":"Theory terms belong in TN only, never in case narrative","status":"NEW","recurrence":1}
```

## Promotion Rules

- Recurrence >= 2 across DIFFERENT cases → candidate for promotion
- `:learn` presents candidates, user approves
- Promoted entries move to `shared/known-corrections.md`
- Status changes from `NEW` → `PROMOTED → known-corrections.md`

## Auto-Capture Triggers

| Event | Captured by | Domain |
|-------|-------------|--------|
| Hook blocks a Write (theory vocab) | `:draft` Step 3.7 | `ap_theory_vocabulary` |
| Hook blocks a Write (source hedging) | `:draft` Step 3.7 | `source_hedging` |
| Hook blocks a Write (options in body) | `:draft` Step 3.3 | `ap_options_in_body` |
| Hook warns (protagonist ratio) | `:draft` Step 3.7 | `ap_protagonist_dilution` |
| Audit agent finds HARD issue | `:audit` Step 5.2 | Per agent finding |
| Audit agent finds MEDIUM issue | `:audit` Step 5.2 | Per agent finding |
