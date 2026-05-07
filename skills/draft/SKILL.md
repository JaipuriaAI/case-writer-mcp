---
name: case-writer-draft
description: Phase 3 of the case-writer pipeline. Write the case narrative section by section, generate exhibits, run inline validation, and assemble the final HTML using the case template. Enforces the 4 ending modes (A/B/C/D), Goldman opening rule, past-tense narration, hedging protocol, exhibit cross-reference integrity, and 9-point HBS readiness self-check. Use after `case-writer-plan` produces an APPROVED spec.
license: MIT
---

# case-writer-draft — Phase 3: Case Narrative & HTML Assembly

> **How to load files from this skill's bundled `references/` and `assets/`:**
> When the steps below tell you to "load `references/X.md`" or "read `assets/<path>`" (e.g. `assets/templates/case-template.html`), invoke the host's `read_skill_file` tool (or equivalent) with:
> - `slug`: `case-writer-draft` — this is THIS skill's slug; do NOT use a parent name like `case-writer` (no such slug exists), and do NOT use the slug of any other connected skill (e.g. `atomic-case-writer` is a separate skill on a different connector — never load from it)
> - `path`: the path exactly as stated, e.g. `references/anti-patterns.md`
>
> The 8 valid skill slugs in this suite are: `case-writer-research`, `case-writer-plan`, `case-writer-draft`, `case-writer-teach`, `case-writer-audit`, `case-writer-publish`, `case-writer-god-mode`, `case-writer-learn`. References cited by this skill live ONLY inside this skill's folder.

> Write the case narrative section by section, generate exhibits, run inline validation, and assemble the final HTML.

## When to use

Run after `case-writer-plan` has advanced the spec to `APPROVED`. Produces the case-body HTML for student distribution. The teaching note is generated in the next phase (`case-writer-teach`).

## Output

`${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-case.html` with spec status `DRAFTED`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md` — promoted patterns. Apply throughout drafting.
2. If `./case-writer-learnings.md` exists, load it.

## References to Load

- `references/status-definitions.md` — validate APPROVED status
- `references/opening-protocol.md` — four permitted opening frames, first-paragraph rules
- `references/hedging-protocol.md` — attribution language for secondary sources
- `references/writing-standards.md` — tense rules, prose standards, international audience guidance
- `references/exhibit-design.md` — exhibit numbering, sourcing, formatting principles
- `references/anti-patterns.md` — AP1–AP15 with detection heuristics. Key risks in this phase: AP3, AP5, AP9, AP11, AP12, AP13, AP14, AP15
- The relevant case type section from `references/case-type-taxonomy.md`

**Status check:** if `**Status:**` is not `APPROVED`, stop and output the exact error message from `references/status-definitions.md`.

Reconstruct the research context from the source registry and section outline. **Every narrative claim must trace to a source in the registry.**

---

## Step 3.1 — Opening Paragraph

Write the opening paragraph in isolation before any other section. Validate immediately:

- [ ] Protagonist named with title in sentence 1
- [ ] Specific date present by sentence 2
- [ ] Dilemma surfaced by end of paragraph
- [ ] First sentence ≤ 25 words
- [ ] All past tense — no present tense outside direct quotes

If any check fails, rewrite before continuing.

The four permitted opening frames (`references/opening-protocol.md`):
- **The Call** — protagonist receives information that forces a choice
- **The Room** — protagonist at a meeting, hearing, or confrontation
- **The Number** — a specific metric or data point that crystallizes the stakes
- **The Deadline** — a specific date or time after which the choice is no longer available

---

## Step 3.2 — Section-by-Section Narrative

For each section in the structural outline:

**Prose standards** (`references/writing-standards.md`):
- Third-person, journalism-grade prose
- Past tense throughout — present tense only inside direct quotes
- No editorializing: evaluative adjectives require attribution (not "the disastrous decision" but "what [Name] later called a serious misjudgment [S3]")
- No passive voice runs — maximum two consecutive passive constructions
- International audience: spell out all currency amounts, convert local idioms
- Cite sources inline as `[S1]`, `[S2]` — every factual claim gets a citation

**Hedging protocol** (`references/hedging-protocol.md`):
For any claim about internal thoughts, motivations, or private deliberations not directly sourced, use approved hedging language. Unhedged internal states are AP11. Never write "[Name] thought" or "[Name] believed" without a source — write "[Name] later said [S4]" or "according to people familiar with the matter [S2]".

**Anti-pattern watch** (`references/anti-patterns.md`):
Apply as you write each section — do not wait for audit:
- **AP13:** No structured options in case body (Modes A–C) — verify the decision moment uses temporal freeze, not an options box
- **AP3:** No post-decision information — do not reveal outcomes in any pre-decision section
- **AP5:** Opening paragraph contains protagonist + date + dilemma
- **AP9:** No present-tense narration outside quotes
- **AP11:** No unattributed internal states
- **AP12:** No ghost quotes — every quoted phrase must trace to a source registry entry
- **AP14:** No academic theory vocabulary in case body — that lives only in the teaching note. Banned terms include: structural holes, epistemic authority, principal-agent, founder imprinting, charismatic authority, organizational identity theory, exit voice loyalty, disruptive innovation, network brokerage, resource dependence theory, agency theory, stakeholder theory, upper-echelons theory, behavioral theory of the firm
- **AP15:** Protagonist must be the primary actor in ≥ 60% of narrative paragraphs

**Narrative reference to exhibits:** when the narrative first mentions data with a corresponding exhibit, reference it inline: `(see Exhibit 1)`. Do not reference an exhibit before it has been introduced in the narrative.

---

## Step 3.3 — Decision Moment Section

For Decision Case, Critical Incident, and Mini-Case types. Read the ending mode from the spec's `## Case Architecture Decisions` section.

**Mode A — Pure Interrupted:**
Write the final section as a scene: the protagonist at the moment of decision. Convey weight, stakes, and irreversibility through narrative prose. End with the temporal freeze (selected style from spec). Do NOT list options, alternatives, or enumerated paths. Do NOT include an options box or "Options Available to [Name]" header. Leave the reader in genuine uncertainty.

**Mode B — Implied Tension:**
Write scene as Mode A. Add ONE final paragraph (2–4 sentences) acknowledging that paths exist without naming them. No specific options, no counts ("three paths"), no labels. End with temporal freeze.

**Mode C — Narrative Deliberation:**
Write the scene. Weave the protagonist's reported deliberation into the final 2–3 paragraphs as prose. No "Option A/B/C" labels. No structured format. Every option must cite a Tier 1–2 source: "According to [Source], [protagonist] weighed..." `[SN]`. End with temporal freeze. Students are expected to evaluate these AND generate alternatives the protagonist may not have considered.

**Mode D — Structured Fork:**
Restate the protagonist's information state at the decision moment: KNOWS / DOES NOT KNOW / UNCERTAIN. List each option using the format from `references/decision-point-design.md` (Mode D section). Give all options equal rhetorical weight — AP1 and AP10 prohibit a dominant framing. End with a closing paragraph.

**All modes:**
- End the case narrative at the decision point — do NOT reveal what the protagonist chose or what happened. That belongs in the teaching note epilogue only (AP3).
- For A+B pair: Case A ends here. Case B is a separate document covering post-decision events.

---

## Step 3.4 — Exhibits

For each exhibit in the exhibit plan:
- Sequential numbering matching order of first narrative reference
- Format as HTML table or structured content appropriate to the data type
- Descriptive title above the exhibit
- Source line below: `Source: [full citation from source registry]`
- Financial data: show raw numbers alongside percentages — students need both for analysis
- Temporal data: include the specific date for each data point

Refer to `references/exhibit-design.md` for formatting principles and AP7 (Exhibit Orphaning).

---

## Step 3.5 — Source Registry Compilation

Compile all `[SN]` inline citations into a numbered source registry at the end of the case:

| ID | Citation | Tier | CRAAP | Role in case |
|----|----------|------|-------|--------------|
| S1 | [Author, Title, Publication, Date, URL] | [1–4] | Pass | [What this source supports] |

Every `[SN]` reference in the narrative must appear here. Every entry here must be referenced at least once. No orphans.

---

## Step 3.6 — Inline Validation (6 Checks)

Run after narrative and exhibits are complete, before HTML assembly:

1. **Past-tense sweep** — scan all narrative text outside quotation marks. Flag any present-tense verb in a declarative narrative sentence. Convert to past tense automatically.
2. **Hedging check** — flag any sentence with "[Name] thought/believed/felt/considered/wanted/hoped" without an adjacent `[SN]` citation. Add hedging from `references/hedging-protocol.md` or add the source citation.
3. **Exhibit cross-reference check** — every exhibit has a `(see Exhibit N)` reference; every reference has a matching exhibit. Flag mismatches; auto-fix numbering if exhibits are out of sequence relative to first narrative reference.
4. **Citation density check** — no run of 3+ consecutive narrative paragraphs without an `[SN]` citation. If found, identify which factual claims could carry a citation.
5. **Opening paragraph check** — re-run the 5 opening criteria. If any fail after the full pass, rewrite.
6. **Word count check** — count narrative words (excluding exhibits and source registry). Compare to the case type target range. If outside ±15%, flag to the user with a specific adjustment recommendation — do not silently truncate.

After all checks pass, proceed to HTML assembly.

---

## Step 3.7 — HTML Assembly

Read `assets/templates/case-template.html`. Replace every `{{PLACEHOLDER}}` with generated content.

**Cover page tokens:** `{{TITLE}}`, `{{CASE_NUMBER}}`, `{{DISCIPLINE_TAGS}}`, `{{CASE_TYPE_LABEL}}`, `{{SUBTITLE}}`, `{{EVENT_DATE}}`, `{{SETTING}}`, `{{WORD_COUNT}}`, `{{LEVEL}}`, `{{ABSTRACT}}` (80–120 word cover abstract), `{{PUBLISH_DATE}}`, `{{PUBLISH_YEAR}}`.

**Body tokens:**
- `{{OPENING_PARAGRAPH}}` — italic lead paragraph (drop cap applied automatically)
- `{{SECTION_N_HEADING}}` / `{{SECTION_N_BODY}}` — repeat for sections 1–4
- **Modes A–C:** `{{DECISION_MOMENT_HEADING}}` / `{{DECISION_MOMENT_BODY}}` / `{{TEMPORAL_FREEZE}}` / `{{FREEZE_STYLE_CLASS}}` / `{{CLOSING_PARAGRAPH}}`
- **Mode D only:** `{{DECISION_FORK_HEADING}}` / `{{DECISION_FORK_INTRO}}` / `{{PROTAGONIST_NAME}}` / `{{OPTION_A_LABEL}}` / `{{OPTION_A_BODY}}` (repeat for B, C, D) / `{{CLOSING_PARAGRAPH}}`

**Exhibits:** `{{EXHIBIT_N_TITLE}}` / `{{EXHIBIT_N_TABLE}}` / `{{EXHIBIT_N_CAPTION}}` for each.

**Source registry:** `{{SOURCE_REGISTRY}}` — render as `.source-entry` divs with `.tier-badge` pills:
```html
<div class="source-entry">[S1] Author, "Title," Publication, URL, Date. <span class="tier-badge tier-1">Tier 1</span></div>
```
Tier badge classes: `tier-1` (black), `tier-2` (black), `tier-3` (gray).

**Note:** Do NOT replace `{{INLINE_CSS}}` — handled by `case-writer-publish` Step 6.1.

Save as `${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-case.html`.

Update spec: `**Status:** DRAFTED`. Append `- DRAFTED: [date] — Case narrative generated ([N] words + [N] exhibits)` to Status History.

---

## Step 3.8 — HBS Readiness Self-Check (MANDATORY)

Verify the case against these 9 checks before proceeding. Fix any failures.

1. [ ] **DECISION PLACEMENT** — protagonist's decision established by the end of page 1? (Goldman Rule)
2. [ ] **NO THEORY IN BODY** — case body contains zero academic framework names, OB jargon, or analytical labels? (AP14 — HARD)
3. [ ] **PROTAGONIST DOMINANCE** — protagonist is primary actor in ≥ 60% of narrative paragraphs? (AP15 — MEDIUM)
4. [ ] **MODE COMPLIANCE** — ending matches the selected Mode from the spec; no options box in Modes A–C? (AP13 — HARD)
5. [ ] **SOURCE HEDGING** — all private company financials hedged with "estimated"/"approximately"/named source inline?
6. [ ] **NO VERDICTS** — case body contains zero evaluative conclusions in author's voice? No "concerns were substantive," no "proved more powerful," no "had become a trap."
7. [ ] **SINGLE ASK** — case ends with ONE decision, not multiple parallel questions?
8. [ ] **LIVING EXECUTIVE NOTE** — if the case involves living executives, "Note on Sources" paragraph present before the source registry?
9. [ ] **WORD COUNT** — narrative within ±15% of the target range for this case type?

If any check fails, revise and re-run the check. Do not proceed to `case-writer-teach` with failures.

---

## Self-Validation Checklist (replaces 9 plugin hooks)

The original case-writer plugin enforced these checks via runtime hooks. Without hooks here, **you (the model) must run them manually before declaring this skill complete**:

- [ ] **No theory vocabulary in case body** — grep the body for: structural holes, epistemic authority, bonding/bridging capital, founder imprinting, principal-agent, charismatic authority, referent power, organizational identity theory, exit voice loyalty, disruptive innovation, network brokerage, legitimate authority, resource dependence theory, institutional isomorphism, transaction cost economics, agency theory, stakeholder theory, upper-echelons theory, behavioral theory of the firm. **Zero hits required.**
- [ ] **Source hedging present** for any private-company financial claim (revenue, valuation, headcount, etc.) — "estimated," "approximately," or named-source attribution
- [ ] **No structured options in body** for Modes A–C — grep for `Option A`, `Option B`, `class="options-box"`, "Options Available," enumerated alternative lists. Mode D body and TN Section 5a are the only places these belong.
- [ ] **Em-dash density** — count em-dashes (`—`) in narrative body. If > 1 per 250 words, soften with parentheticals or commas. Em-dash overuse is a pattern flagged by the original plugin.
- [ ] **Theory-tag cap** — body should have ≤ 0 academic-theory tags; TN may use them but capped at the limit set in `references/anti-patterns.md`
- [ ] **No orphan options-CSS** — if body has no options box, ensure no leftover `<style>` referring to `.options-box` clutters the document
- [ ] **No "bring in theory" naming** — body sections must not have headings like "Bringing in [Framework Name]" — that's a teaching-note construct
- [ ] **Protagonist ratio ≥ 60%** — count narrative paragraphs containing the protagonist's full name or surname; verify ratio
- [ ] **Past tense sweep clean** — narrative outside quotations is past tense
- [ ] **All `[SN]` citations resolve** to source registry entries; no orphan registry entries

## Don't

- Do not reveal post-decision outcomes anywhere in the case body. The reader must finish the case in genuine uncertainty (Mode A) or with paths-but-no-resolution (Mode B/C). AP3 violations require a full rewrite of the offending section.
- Do not use academic theory vocabulary in the case body. Cases describe what happened in plain English; theory lives in the teaching note (AP14).
- Do not invent quotes. Every quoted phrase must trace to a source registry entry (AP12).
- Do not include enumerated options ("Option A/B/C") in the body for Modes A–C (AP13).
- Do not silently truncate narrative to hit a word count — flag it to the user instead.

## Output

`${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-case.html` with spec status `DRAFTED`.
