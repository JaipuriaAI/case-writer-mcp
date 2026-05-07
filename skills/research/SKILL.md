---
name: case-writer-research
description: Phase 1 of the case-writer pipeline. Ingest sources for a Harvard-style MBA teaching case (URL, file, or "Company / Event / Year"), run parallel research, triangulate against the source-credibility tier hierarchy, identify the protagonist, recommend a case type, run the Research Sufficiency Gate, and write a DRAFT spec. Use when a user wants to start a new case from a topic, news article, or company event.
license: MIT
---

# case-writer-research — Phase 1: Research & DRAFT Spec

> **How to load files from this skill's bundled `references/` and `assets/`:**
> When the steps below tell you to "load `references/X.md`" or "read `assets/<path>`" (e.g. `assets/templates/case-template.html`), invoke the host's `read_skill_file` tool (or equivalent) with:
> - `slug`: `case-writer-research` — this is THIS skill's slug; do NOT use a parent name like `case-writer` (no such slug exists), and do NOT use the slug of any other connected skill (e.g. `atomic-case-writer` is a separate skill on a different connector — never load from it)
> - `path`: the path exactly as stated, e.g. `references/anti-patterns.md`
>
> The 8 valid skill slugs in this suite are: `case-writer-research`, `case-writer-plan`, `case-writer-draft`, `case-writer-teach`, `case-writer-audit`, `case-writer-publish`, `case-writer-god-mode`, `case-writer-learn`. References cited by this skill live ONLY inside this skill's folder.

> Reconstruct the event from public sources, identify the protagonist, assess case-worthiness, select a case type, and write a `DRAFT` spec.

## When to use

The user names a topic, drops a URL or pastes an article, or says "let's start a case on X." This is the entry point. Subsequent phases (`plan`, `draft`, `teach`, `audit`, `publish`) consume the spec produced here.

## Output

Write the spec to: `${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-spec.md` with `**Status:** DRAFT`.

If `${CASE_OUTPUT_DIR}` is unset, default to `./cases/` in the agent's working directory.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md` — promoted patterns from prior case-writing sessions. Apply these as active checks throughout research.
2. If `./case-writer-learnings.md` exists in the working directory, load it. Apply any NEW learnings relevant to this case's domain.

## References to Load

- `references/source-credibility.md` — tier hierarchy, CRAAP test, minimum source thresholds
- `references/case-type-taxonomy.md` — 8 case types with selection flowchart and structural specs
- `references/status-definitions.md` — status validation
- `references/case-spec-template.md` — spec document format

**No status check required** — this phase creates a new case. If a spec already exists for this slug, warn the user and confirm overwrite before continuing.

---

## Step 0.1 — Load Case Registry

Read `${CASE_OUTPUT_DIR:-./cases}/case-registry.md` for the next available GBA number and to check for slug conflicts.

If the registry does not exist, create it and start at `GBA 2026-001`.

---

## Step 1.1 — Input Detection

Classify the input using this order of precedence:

1. Starts with `http://` or `https://` → **URL** — fetch with whatever HTTP-fetch tool your client exposes (e.g. `WebFetch`), extract key facts
2. Starts with `/`, `~/`, `./` and ends with `.pdf`/`.txt`/`.md` → **File path** — read directly
3. Format `"Company / Event / Year"` (two `/` delimiters with non-empty segments) → **Structured** — parse directly
4. Anything else → **Topic string** — proceed to research as-is

For URLs and file paths: extract and summarize the core topic, key actors, and timeframe before research begins. If fetch fails (paywall, 404), ask the user to paste the text directly.

---

## Step 1.2 — Parallel Research (3 Agent Roles)

> **Tool abstraction:** the original plugin used `mcp__perplexity__perplexity_search` / `mcp__perplexity__perplexity_research`. In this skill, **use whatever web search and fetch tools your client exposes** — `WebSearch`, `WebFetch`, Perplexity-MCP, Brave-MCP, Tavily-MCP, Parallel Web, or any other. The methodology (Tier-1 first, CRAAP-tested, minimum source counts) is what matters; the specific tool is interchangeable. If your client has no web tools at all, ask the user to paste sources directly.

Run these three research roles. If your client exposes a Task / Agent / sub-agent dispatch tool, run them in parallel with the agent prompts below; otherwise run sequentially in this context.

Include the Source Credibility tier hierarchy from `references/source-credibility.md` in each role's working context so they self-classify sources as they gather them.

### Role A — Event Reconstruction

Build a chronological timeline of the event: what happened, when, who made which decisions, and what the consequences were.
- Target Tier 1–2 sources first: SEC/regulatory filings, court documents, WSJ, FT, Bloomberg, Reuters, NYT, The Economist, official earnings transcripts.
- For each major claim, identify whether it has 1 source or 2+ independent sources.
- Deliverable: ordered timeline with source citations — minimum 8 sources from this role alone.

### Role B — Protagonist Research

Identify the person with the highest decision authority in the event (see protagonist qualification criteria below).
- Collect only material from the public record: named interviews, published quotes from earnings transcripts, conference keynotes, shareholder letters, regulatory testimony.
- Build a profile: title at the time of the event, career trajectory relevant to this decision, observable decision-making patterns from prior public record.
- Flag explicitly if the protagonist has insufficient public presence to support a secondary case (fewer than 3 independently sourced direct quotes, or no named coverage in Tier 1–2 sources).
- Deliverable: protagonist profile with sourced quotes.

### Role C — Industry and Competitive Context

- Market structure and size at the time of the event
- Competitive dynamics: who the key rivals were and their positions
- Regulatory environment if relevant
- Analyst and expert commentary (Tier 3 sources acceptable here)
- Deliverable: competitive landscape summary with sources

**Protagonist qualification criteria** (apply after roles return):
- Must have had actual decision authority at the moment in question (not just organizational proximity)
- Must have at least 3 directly attributed quotes from Tier 1–2 sources
- Must be named in the public record — no anonymous executives
- If research surfaces two plausible protagonists, present both to the user with a recommendation

---

## Step 1.3 — Source Registry Assembly

After all three research roles return, consolidate sources into a master registry:

1. Assign a tier to every source using `references/source-credibility.md`
2. Run the CRAAP check (Currency, Relevance, Authority, Accuracy, Purpose) on every source
3. Reject sources failing 3+ CRAAP criteria — do not include them in the registry
4. Calculate:
   - Total confirmed sources
   - Tier 1–2 source count
   - Maximum single-source share (citations from one source / total citations)

**Hard minimums** (from `references/source-credibility.md`):
- Total sources: ≥ 15 (≥ 8 for Mini-Case)
- Tier 1–2 sources: ≥ 3
- Single-source share: ≤ 25%

If minimums are not met at this stage, run an additional targeted search before proceeding. Do not write a spec that fails source minimums — `audit` will block publication.

---

## Step 1.4 — Case Type Recommendation

Run the selection flowchart from `references/case-type-taxonomy.md` against the assembled material:

1. Single incident ≤ 2 days with ethical/crisis dimension? → **Critical Incident**
2. Protagonist faces a clear strategic fork with 3+ distinct options? → **Decision Case**
3. Condensed enough for one session with one focused decision? → **Mini-Case**
4. Naturally sequences into decision → outcome → consequence phases? → **Series**
5. Designed to demonstrate one specific framework with limited ambiguity? → **Illustrative**
6. Multiple legitimate interpretations, no clear right answer, senior audience? → **Exploratory**
7. Long timeline, multiple stakeholders, evolving dynamics? → **Descriptive**
8. Multiple companies or industry-level focus? → **Industry Note**

Present the top 1–2 recommended types with rationale, target page count, exhibit count, and TN ratio. Note: `god-mode` never selects Exploratory or Series (too complex for autonomous decisions).

---

## Step 1.5 — Protagonist Confirmation (USER GATE)

Present to the user:

```
Based on research, I recommend the following:

Protagonist:        [Full Name], [Title], [Organization]
Decision moment:    [1–2 sentence description of the exact decision]
Recommended type:   [Type] ([N]–[N] pages + [N]–[N] exhibits)
Rationale:          [2–3 sentences on why this protagonist and type fit]

Source registry:
  Total sources:    [N] / 15 required
  Tier 1–2:         [N] / 3 required
  Max single-source share: [X%] / 25% maximum

Proceed with these choices, or describe what you'd like to change.
```

Wait for user confirmation before writing the spec. If invoked from `god-mode`, auto-confirm the recommended protagonist and highest-scoring case type.

---

## Step 1.6 — Write DRAFT Spec

Using `references/case-spec-template.md`, create `${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-spec.md`.

Populate every section the research supports. Mark unknowns as `[TBD]` — they must be resolved in Phase 2 (`plan`). Set `**Status:** DRAFT`.

The minimum viable DRAFT spec contains:
- Protagonist confirmed with title, organization, and decision date
- Core tension articulated in one sentence
- At least 8 sources identified (full 15 required before `draft` begins)
- **Research Sufficiency Gate passed** (Step 1.X)
- Opening paragraph drafted
- Section outline sketched with estimated word counts

Append the full source registry table. Log the DRAFT transition in the Status History section.

---

## Step 1.X — Research Sufficiency Gate (USER GATE — skipped only by `god-mode`)

After completing research and triangulation, evaluate whether the material supports a case-worthy teaching vehicle. Present the assessment to the user BEFORE proceeding to `plan`.

Score each dimension PASS / WEAK / FAIL:

| Dimension | PASS | WEAK | FAIL |
|-----------|------|------|------|
| **Decision clarity** | Specific, documentable protagonist decision with real stakes and time pressure | Decision is diffuse or lacks documented urgency | No clear decision point |
| **Source depth** | ≥ 3 Tier 1–2 sources with on-record quotes from principals | Tier 2–3 only; no direct protagonist quotes | Only Tier 3–5 sources |
| **Protagonist access** | Protagonist has given interviews, speeches, testimony revealing reasoning | Voice is thin — limited public statements | Protagonist has never spoken publicly about this |
| **Genuine trade-offs** | ≥ 3 defensible options, each with distinct stakeholder winners and real costs | One option obviously dominant | Binary or no visible alternatives |
| **Pedagogical value** | Teaches frameworks not easily accessible through textbook examples | Interesting but discussion would converge quickly | News story, not a teaching vehicle |

**Scoring:**
- **5 PASS:** Strong case. Proceed to `plan`.
- **4 PASS + 1 WEAK:** Viable with adjustments. Proceed but note the weakness in the spec.
- **3 PASS + 2 WEAK:** Marginal. Recommend the user reconsider scope or angle.
- **Any FAIL:** Recommend against proceeding and propose an alternative angle.

**In `god-mode`:** skip the user gate but still run the evaluation. Log warnings under `## Research Limitations` in the spec. If 2+ dimensions FAIL, HALT even in god-mode and present the assessment to the user.

**Why this gate matters:** A compelling news story is not automatically a case. Cases require a protagonist with documented decision authority, genuine trade-offs that resist single-answer resolution, and enough source material to write neutrally. Without these, the model compensates by inventing deliberation (AP8), editorializing (AP14), or constructing options the protagonist never actually faced (AP13). This gate catches structural weaknesses before they contaminate the draft.

---

## Self-Validation Checklist

Before declaring this skill's output complete, verify each item below. If any fails, fix and re-check.

- [ ] **Slug uniqueness** — no existing entry in `case-registry.md` collides with this slug
- [ ] **Status set correctly** — spec contains exactly `**Status:** DRAFT`
- [ ] **Source minimums** — registry shows ≥ 15 total sources (≥ 8 for Mini-Case), ≥ 3 Tier 1–2, ≤ 25% single-source share
- [ ] **Protagonist qualification** — named protagonist has ≥ 3 directly attributed Tier 1–2 quotes
- [ ] **Sufficiency gate documented** — all 5 dimensions scored, score recorded in spec
- [ ] **No `${CLAUDE_PLUGIN_ROOT}` or absolute user paths** in the spec — all paths cwd-relative
- [ ] **Status History line appended** — `- DRAFT: [ISO date] — Research complete, [N] sources collected`

## Don't

- Do not invent quotes, paraphrase as direct quotes, or attribute statements not in the public record
- Do not include sources failing 3+ CRAAP criteria, no matter how relevant they look
- Do not select Exploratory or Series when this skill is invoked from `god-mode`
- Do not skip the Research Sufficiency Gate — even when the material seems obviously strong, run the evaluation and record the score
- Do not write a spec while sources are below minimum — run another targeted search round instead

## Output

`${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-spec.md` with `**Status:** DRAFT`.
