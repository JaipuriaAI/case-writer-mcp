# Case Spec Template
**Version:** 1.0.0
**Loaded by:** `:research` (creates initial DRAFT), `:plan` (refines and locks structural decisions)

Copy this template verbatim when creating a new spec file. Replace all `{{PLACEHOLDER}}` values. Do not delete any section — if a field is unknown at DRAFT stage, write `[TBD]` and complete it during `:plan`.

---

```markdown
# Case Spec: {{TITLE}}
**Status:** DRAFT
**Slug:** {{SLUG}}
**Created:** {{DATE}}
**Spec Version:** 1.0

---

## Protagonist
- **Name:**
- **Title:**
- **Organization:**
- **Decision Date:**
- **Location:**

## Case Type
**Selected Type:** [Decision Case / Critical Incident / Illustrative / Descriptive / Exploratory / Mini-Case / Series / Industry Note]
**Difficulty Level:** [1 / 2 / 3 / 4 / 5]
**Target Audience:** [e.g., Core MBA Year 1, Executive Education, Elective]
**Primary Discipline(s):** [e.g., Strategy, Corporate Governance, Organizational Behavior]
**Estimated Length:** [e.g., 4,000 words narrative + 3 exhibits]

## Case Overview
**Core Tension:** [1 sentence describing the central dilemma — what two legitimate values or priorities are in conflict]
**Decision Point:** [1-2 sentences describing the exact moment the protagonist faces a choice and what that choice is]
**Why This Case?** [1-2 sentences on what this case teaches that others don't — its pedagogical distinctiveness]

## Case Architecture Decisions
[Locked after Step 2.2a Case Architecture Gate during :plan]
- Ending Mode: [A / B / C / D] — [TBD]
- Temporal Freeze Style: [Clock / Room / Weight / Question] — [TBD]
- TN Options Count: [3 / 4 / 5] — [TBD]
- Case Structure: [Standalone A / A+B Pair] — [TBD]

## Source Registry (DRAFT)
Minimum sources required: 15
Tier 1-2 sources required: at least 3
Maximum single-source share: 25%

Current status:
- Total sources confirmed: [X]
- Tier 1-2 sources confirmed: [X]
- Highest single-source share: [X%]

**CRAAP Scoring Guide:**
- Currency: Is the source recent enough for this topic?
- Relevance: Does it directly support a claim in the case?
- Authority: Is the author/publication credible in this domain?
- Accuracy: Is the information verifiable from other sources?
- Purpose: Is the source informational (not promotional)?

| ID | Citation | Tier | CRAAP | Notes |
|----|----------|------|-------|-------|
| S1 | [Full citation: Author, Title, Publication, Date, URL] | [1/2/3/4] | [Pass/Fail] | [What this source covers] |
| S2 | | | | |
| S3 | | | | |
| S4 | | | | |
| S5 | | | | |
| [Add rows to reach minimum 15] | | | | |

**Tier Reference:**
- Tier 1: Primary sources (filings, transcripts, official statements, court documents)
- Tier 2: Established journalism (NYT, FT, WSJ, Reuters, Bloomberg, The Economist)
- Tier 3: Industry publications and credentialed analysts
- Tier 4: Secondary aggregators, Wikipedia, blogs — corroboration only

## Structural Plan

### Section Outline
[Plan 4-8 sections. Include approximate word count for each. Total narrative should be 3,000-6,000 words for standard cases.]

1. **[Section Name]** — [1-line description of what happens in this section] (~[N] words)
2. **[Section Name]** — (~[N] words)
3. **[Section Name]** — (~[N] words)
4. **[Decision Moment]** — [scene: date, location, stakes, irreversibility]
   - Ending mode: [per Case Architecture Decisions]
   - Temporal freeze style: [per Case Architecture Decisions]
   - If Mode C: [cite Tier 1-2 source per option]
   - If Mode D: [list 3-5 options with trade-offs]
5. **[Section Name]** — (~[N] words)

### Exhibit Plan
[Every exhibit must be referenced in the narrative. Plan exhibits before drafting.]

| Exhibit | Title | Data to Include | Primary Source | First Referenced In |
|---------|-------|-----------------|----------------|---------------------|
| 1 | [Title] | [What data/information] | [S?] | [Section name] |
| 2 | | | | |
| 3 | | | | |

### Opening Paragraph Draft
[Draft the first paragraph of the case here. Must include: protagonist name, specific date, specific situation. See `opening-protocol.md` for the four permitted opening frames.]

[Draft:]

### Temporal Freeze Point
**The decision moment:** [Exact date and situation — this is the point after which no facts may appear in the pre-decision narrative]

## Teaching Note Outline

### Learning Objectives (3-5)
[Draft learning objectives. Must span at least 3 Bloom's levels.]

1. [Bloom's verb] [object] ([Bloom's level])
2. [Bloom's verb] [object] ([Bloom's level])
3. [Bloom's verb] [object] ([Bloom's level])
4. [optional]
5. [optional]

### Key Issues (3-6 tensions)
[Name the central tensions the case will surface]

1. **[Tension Name]:** [Brief description]
2. **[Tension Name]:** [Brief description]
3. **[Tension Name]:** [Brief description]

### Discussion Questions (4-6)
[Draft questions — pair each with its Bloom's level]

1. Q: [Question] — [Bloom's Level]
2. Q: [Question] — [Bloom's Level]
3. Q: [Question] — [Bloom's Level]
4. Q: [Question] — [Bloom's Level]
5. [optional]
6. [optional]

### Theory Connections (3-5)
[Identify academic frameworks this case illuminates]

1. [Framework] — [Author(s)] — [How it connects]
2. [Framework] — [Author(s)] — [How it connects]
3. [Framework] — [Author(s)] — [How it connects]

### Options Analysis (Instructor Only — NOT in case body unless Mode D)
[Plan N options per TN Options Count gate]
- Option 1: [Name] — [description] — [Key trade-off]
- Option 2: [Name] — [description] — [Key trade-off]
- Option 3: [Name] — [description] — [Key trade-off]
- [Option 4 if applicable]
- [Option 5 if applicable]

### Teaching Plan Duration: [75 / 90 / 120] minutes

## Decisions Made
[Locked only after QG1 approval at end of `:plan`. Leave as [TBD] at DRAFT stage.]

- Case type: [type] — [reason for selection]
- Difficulty level: [1-5] — [reason for selection]
- Protagonist: [name] — [why this protagonist over alternatives]
- Decision point: [description] — [why this moment was chosen]
- Case Architecture: [Mode] + [Freeze Style] + [N options] + [Structure]
- Opening frame: [The Call / The Room / The Number / The Deadline] — [why]

## Case B Outline (A+B Pair only — delete if Standalone A)
- **B Narrative Scope:** [What Case B covers: decision made, implementation, consequences]
- **B Word Count Target:** [e.g., 3,000-4,000 words]
- **B Source Additions:** [Any sources needed beyond Case A's registry]

## Status History
- DRAFT: {{DATE}} — Initial research complete, spec created
```

---

## Notes for `:research` (when creating this file)

Fill in what you know. Mark unknowns as `[TBD]`. The minimum viable DRAFT spec has:
- Protagonist confirmed
- Core tension articulated
- At least 5 sources identified (more required before `:plan`)
- Opening paragraph drafted
- Section outline sketched

Do not mark status APPROVED — that requires explicit user confirmation at the end of `:plan`.

## Notes for `:plan` (when refining this file)

By end of `:plan`, all `[TBD]` entries must be resolved. The spec is the contract for `:draft`. Ambiguity here = structural problems in the case.

Lock these before QG1:
- Case type (no changes after APPROVED)
- Case Architecture Decisions (all 4 gates resolved)
- Exhibit plan (no orphaned exhibits)
- Learning objectives spanning 3+ Bloom's levels
- Temporal freeze point confirmed
