# Known Corrections — Case Writer

> Promoted patterns from prior case writing sessions. Loaded by SessionStart hook.
> Each entry was observed >= 2 times across different cases before promotion.

---

## v1.2.0 Patterns (promoted 2026-05-06 from boeing-737-max-grounding-decision-2019)

### Use the Canonical Renderer (NEVER reinvent render scripts per case)

**Rule:** All cases must be rendered via the canonical renderer at `./scripts/render_case.py` (bootstrapped from `assets/scripts/render_case.py` in this skill repo on first run). Never create a per-case `render_html.py` or invent ad-hoc HTML/CSS in the case directory.

**Failure mode this prevents:** the boeing case was initially rendered via a custom `render_html.py` that reintroduced bugs the plugin's templates had already solved (markdown-to-html footnote regex bug, drop-cap WeasyPrint crash, brand drift to "GBA Teaching Cases" instead of Rehearsal wordmark). When templates exist in the plugin, USE THEM.

**Enforcement:** `:publish` Step 6.1 must invoke `python3 ./scripts/render_case.py "${CASE_OUTPUT_DIR:-./cases}/{slug}"` rather than expecting per-case rendering scripts.

**Source:** boeing-737-max-grounding-decision-2019 (2026-05-06).

### Footnote Regex Must Be Paragraph-Bounded

**Rule:** Markdown footnote definition extraction MUST use `(?=\n\n|\Z)` as the terminator, NOT `(?=^\[\^|\Z)` with DOTALL.

**Failure mode this prevents:** A greedy DOTALL match for footnote bodies that terminates at "next footnote OR end of document" will SLURP all case body content from the first footnote forward into footnote 1's definition. The PDF then renders Section 1 + a giant misformatted endnote, with Sections 2-N missing entirely. The bug is structural-silent: page count looks reasonable, HTML "validates," only visual PNG inspection of page 2 reveals the corruption.

**Correct regex:**
```python
fn_def = re.compile(r'^\[\^(\d+)\]:\s*(.+?)(?=\n\n|\Z)', re.MULTILINE | re.DOTALL)
```

**Source:** boeing-737-max-grounding-decision-2019 first-pass renderer; caught by visual inspection per the WeasyPrint Pagination Discipline META-RULE.

### Drop Cap via Inline Span (NOT `::first-letter` Float)

**Rule:** Drop caps in `.lead` paragraphs must use a `<span class="dropcap">` wrapper with `vertical-align` + larger `font-size`. Do NOT use `::first-letter { float: left }`.

**Failure mode this prevents:** WeasyPrint's `float_layout` raises `AssertionError: isinstance(box, boxes.BlockReplacedBox)` when `::first-letter { float: left }` is applied. The PDF generation crashes mid-render and the previous PDF on disk is silently retained — appearing as if "nothing changed" when re-rendering.

**Correct pattern:**
```html
<p class="lead"><span class="dropcap">C</span>hicago, March 12, 2019 — ...</p>
```
```css
.lead .dropcap {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 28pt; font-style: normal; font-weight: 700;
  color: #0a0a0a; line-height: 0.9; vertical-align: -4pt;
  margin-right: 2px;
}
```

**Source:** boeing-737-max-grounding-decision-2019 first WeasyPrint render attempt.

### Section Headings: Period Separator (NOT Em-Dash)

**Rule:** TN section headings use `1. Section Title` format — period separator. The pattern `Section 1 — Section Title` is BANNED.

**Failure mode this prevents:** em-dash separators in section headings violate v10.23.0 em-dash discipline (which we ourselves shipped to atom-creator earlier this session). They also signal "checklist scaffolding" rather than authored content. Canonical implementation in amodei-india-summit and boeing-737-max-grounding-decision-2019 v2 both use period separators.

**Source:** boeing-737-max-grounding-decision-2019 + amodei reference comparison.

### TN Has 9 Canonical Sections (NOT 13)

**Rule:** Teaching notes have **9 sections**, not the 13 originally specified in v1.x of teaching-note-protocol.md. The dropped sections are:

- §1 Confidential Banner — the navy banner at top of the rendered TN page already conveys this; an additional prose section duplicates the warning.
- §5 Pre-Class Assignment Questions — pre-class comprehension checks duplicate the case body itself. Replaced with §9 Assignment Suggestions (post-class).
- §8 Theory Connections — duplicates §5 Analytical Framework. The single-primary-framework rule means extension theories live as a one-liner inside §5, not as a separate section.
- §12 Research Methodology Disclosure — informational only, rarely useful. Move to source-registry.md if needed.
- §13 Supplementary Reading — rarely used; instructor-specific recommendations belong outside the TN.

**The canonical 9 sections:** Case Summary, Learning Objectives (with framing prose), Key Issues (bulleted), Discussion Questions with Suggested Answers, Analytical Framework, 5a Decision Options, Board Plan, Teaching Plan, Epilogue, Assignment Suggestions.

**Source:** amodei-india-summit + boeing-737-max-grounding-decision-2019 v2 canonical implementations.

### TN Voice Patterns (Facilitator, NOT Mechanical)

**Rule:** Discussion question model answers use facilitator-voice patterns, NOT protocol-checklist phrasing.

**Banned mechanical patterns:**
- "This question executes Step X of the analytical scaffold" (checklist voice)
- "By examining the framework, students arrive at..." (didactic narration)

**Required facilitator patterns:**
- "Strong responses will surface both the surface reading... and the stress-tested reading..."
- "Students may argue that..." / "One reading of this evidence is..."
- "The instructor should let this counter-argument breathe"
- "The case rewards students who name both the moment and the specific public action"
- "The deeper question for the instructor to land is..."

**The acid test:** if two instructors with opposing views on the case's central question could both use this TN to facilitate their preferred discussion direction, the tone is correct.

**Source:** amodei-india-summit canonical implementation; boeing-737-max-grounding-decision-2019 first-pass TN failed this test (mechanical voice) and was rewritten end-to-end.

### Section Openers Are Content, NOT Meta-Explanation

**Rule:** TN sections open directly with the substantive content. They do NOT lead with a paragraph explaining what the section contains.

**Banned opener pattern (the canonical AI-tell in TN writing):**
> "Section 1 — Confidential Banner: This Teaching Note contains the case's epilogue, the four-option analytical framework, the suggested model answers, and the board plan. It is for instructor use only and must not be distributed to students. The four options analyzed in Section 5a are NOT in the case body; students must generate them during discussion before the instructor reveals this analysis."

**Why it fails:** every clause is *meta-explanation about the document* rather than content for the instructor. The navy banner already says it's confidential. Section 5a already says options aren't in the case body. The whole paragraph is scaffolding-as-prose, redundant with the document's structure. A human teaching-note author would never write this.

**Correct pattern:** start with the case summary directly. The instructor needs the content, not the explanation of where the content is.

**Source:** boeing-737-max-grounding-decision-2019 first-pass TN; user explicitly flagged "who writes like this?"

### Visual Inspection META-RULE: Verify Section Header Count

**Rule:** Before declaring `:publish` complete, count `<h3 class="section-head">` instances in the rendered HTML and verify it matches the expected section count from the markdown source. If they diverge, a markdown-to-HTML conversion bug has corrupted the body.

**Implementation in `scripts/render_case.py`:** the `visual_inspect()` function does this automatically and reports `WARN` if the section count is below the expected threshold.

**Source:** boeing-737-max-grounding-decision-2019 first-pass render shipped with body content silently slurped into footnote 1; visual inspection caught it.

---

## Anti-Pattern Enforcement

### AP14 Theory Vocabulary — Zero Tolerance in Case Body
**Rule:** The case body must contain zero academic framework names, OB jargon, or analytical labels. Theory belongs exclusively in the Teaching Note.
**Terms:** structural holes, epistemic authority, bonding capital, bridging capital, founder imprinting, principal-agent, charismatic authority, referent power, organizational identity theory, exit voice loyalty, disruptive innovation, network brokerage, legitimate authority, resource dependence theory, institutional isomorphism, transaction cost economics, agency theory, stakeholder theory, upper echelons theory, behavioral theory of the firm
**Source:** HBS expert review, March 2026. AP14 hardening.

### AP13 Options in Body — Mode A-C Prohibition
**Rule:** Modes A (Pure Interrupted), B (Implied Tension), and C (Narrative Deliberation) must NEVER contain structured options boxes, "Options Available to [Name]" headers, or Option A/B/C enumerations. Options analysis belongs in TN Section 5a only.
**Source:** Decision-point-design.md hardening, March 2026.

## Source Credibility

### Private Company Financials Must Be Hedged
**Rule:** Any financial claim about a private company must include hedging language: "estimated", "approximately", "reported", "according to [source]", "analysts estimate". Unhedged dollar amounts for private companies are treated as fabrication risk.
**Source:** source-credibility.md hardening, March 2026.

### Living Executive Reputational Check
**Rule:** Never use a named living person as a POSITIVE example without checking for post-research legal/reputational issues via web search. Depersonalize to company name when the story works without the individual.
**Source:** Dan Price/Gravity Payments incident. atom-creator-learnings.md.

## Factual Verification

### Currency Denomination Verification
**Rule:** When citing regulatory limits or financial thresholds, verify the CURRENCY UNIT, not just the number. LRS = USD. GST thresholds = INR. FEMA limits = USD.
**Source:** RBI LRS denomination error in financial-advisory course.

### Arithmetic Verification for Comparisons
**Rule:** Every numerical comparison ("X times", "Y percent more") must be verified by dividing the actual numbers. Plausible-sounding multipliers are the hardest errors to catch.
**Source:** Insurance commission "seven times" when actual was 24.9x.

## Decision Design (v1.1.0 — promoted 2026-04-27)

### Option-Axis Alignment (AP4-style)
**Rule:** All options in an option-set must be substitutes on a single decision axis. Diagnostic test: "Could ONE question phrase all three options?" If yes, the axis is intact. If one option requires a different framing question, it is off-axis and must be replaced or restructured. Vocabulary check: every option's prose should overlap with the body's vocabulary; an option requiring vocabulary the body never loaded is grafted on.
**Source:** amodei-india-summit. Original Option C ("Pursue Consumer Scale in India") was on a market-strategy axis while A and B were on a comms-posture axis.

### Body-Options Time-Horizon Alignment
**Rule:** Body and options must agree on case type AND time horizon. Diagnostic: protagonist's stated decision window vs. each option's execution timeline. If options require months/quarters to execute when body specifies hours/minutes, the case has a category split. Crisis Decision cases require comms-shaped options (engage / disengage / redirect). Strategic Positioning cases tolerate multi-quarter strategy options. Mixing them confuses the teaching outcome.
**Source:** amodei-india-summit. Body framed a 40-minute press-briefing crisis; options answered multi-quarter market strategy.

### Genre Coherence Sweep on Discipline Change
**Rule:** When a case discipline/genre changes, sweep ALL of: masthead label, Sections 1-3 text, Learning Objectives, Key Issues, Q1-Q4 model answers, Section 5 theory tags, Section 5 narrative paragraph, board-plan bullets, teaching-plan rows, epilogue tone. The "leftover Q4" pattern is the canonical fingerprint of an incomplete genre swap — when re-genre'ing, audit Q4 first because it's furthest from the discipline-label edit and most likely to retain old vocabulary.
**Source:** amodei-india-summit. Reframing Strategy → Crisis Comms left Q4 still asking about consumer-scale strategy.

## TN Completeness (v1.1.0 — promoted 2026-04-27)

### Single Primary Framework Rule
**Rule:** TN Section 5 should name ONE primary analytical framework, explain its constituent parts in 3-4 sentences (with the strategic insight beyond intuition explicitly stated), provide a step-by-step decision scaffold students can walk through, then list secondary theories as a SINGLE one-line "Extension theories for instructors who wish to deepen" paragraph. Diagnostic test: "Could a student walk out and apply this framework to a different case tomorrow?" If they only learned 6+ names → TN failed (credentialed via pluralism, didn't transfer a usable model). If they learned ONE usable mental model → TN succeeded. HBS canonical pattern. Multi-theory pluralism is legitimate ONLY for upper-level seminar courses where comparing lenses IS the learning outcome.
**Enforced by:** `hooks/check-theory-tag-cap.sh` — warns when 6+ `.theory-tag` spans appear in any single TN paragraph.
**Source:** amodei-india-summit. TN Section 5 originally listed 9 theory tags as a chip cloud + 3 per-question Bring-in theory paragraphs introducing more frameworks (~8 total).

## TN Tone (v1.1.0 — promoted 2026-04-27)

### "Connect to Scaffold" Naming
**Rule:** When a TN has a primary analytical framework (Section 5), Q1/Q2/Q3 model answers should reference it by step number using the heading "Connect to scaffold:" not "Bring-in theory:". Example: "Connect to scaffold: This question executes Step 1 of the analytical scaffold (Section 5)…" Why: "Bring-in" implies the framework is external and gets imported when needed (creates encyclopedic theorists). "Connect to scaffold" implies the framework is the session's spine and each question is an application of it (creates practitioners).
**Enforced by:** `hooks/check-bring-in-theory-naming.sh` — warns when "Bring-in theory:" appears in TN HTML.
**Source:** amodei-india-summit. Q1/Q2/Q3 each had Bring-in theory paragraphs introducing new frameworks per question.

## Presentation Visual Design (v1.1.0 — promoted 2026-04-27)

### Editorial Flow Over Boxed Containers
**Rule:** Container elements in case + TN PDFs should use thin (2px) left-edge accent lines for left-anchored content (Q-blocks, scaffold, options, blockquotes, epilogue, extension theories) OR top accent rules for section dividers (board panels, source registry). NO 4-sided borders. NO background tints. Visual hierarchy is preserved through accent-line color, typography weight, italic headings, and bold lead-words. Pattern: card-based UI is for catalog browsing; editorial layout is for sustained reading. Case PDFs are the latter — readers spend 20-90 minutes per document, not 30 seconds skimming.
**Source:** amodei-india-summit. User explicitly flagged 4-sided container borders + tinted backgrounds as creating a "disjointed" card-stack look.

### Em-Dash Overuse in Case Body
**Rule:** Heavy em-dash use is the #1 AI prose signature in 2024-2026. For each em-dash in case body prose, ask what relationship it marks: introduction (use colon), apposition (use comma), true parenthetical aside (use parens), separable thought (use period). The journalistic dateline em-dash ("New Delhi, February 20, 2026 — Dario Amodei woke...") is the only legitimate body use — keep ONE such dateline; remove all others.
**Enforced by:** `hooks/check-em-dash-overuse.sh` — warns at >5 em-dashes in case body, blocks at >15.
**Source:** amodei-india-summit. Initial case had 20+ em-dashes flagged by user as "too many em-dashes."

## Presentation Pagination (v1.1.0 — promoted 2026-04-27)

### WeasyPrint Pagination Discipline
**Rule:** When generating case + TN PDFs via WeasyPrint:
1. **Avoid `display: flex`** for any container whose content might overflow one page; use stacked block layout instead. WeasyPrint cannot paginate flex containers — it fragments them into narrow columns broken across pages.
2. **Use `page-break-inside: avoid` ONLY on elements smaller than one page** (sub-bullets, individual options, panel-purpose blocks). Never on question-blocks or other multi-paragraph units — forces white-space cascades when block can't fit.
3. **HTML keep-together wrappers** (parent div with page-break-inside: avoid) work only when the wrapped content fits on one page; for taller content, allow internal splits via the natural break points of sub-elements.
4. **META-RULE:** Before declaring PDF formatting "done," render via WeasyPrint, convert all pages to PNG via `pdftoppm -png -r 100`, visually inspect every page for orphans / widows / excess white space, iterate. Never rely on CSS reasoning alone — the renderer's heuristics are more conservative than rule semantics suggest. This protocol is enforced by the `/pdf` skill.
**Source:** amodei-india-summit. Multiple iterations where formatting was declared "done" without visual verification, then user reported new orphan/white-space bugs from over-aggressive page-break rules and unpaginatable flex containers.

### Orphan .options-box CSS After Mode Conversion
**Rule:** When converting from Mode D (options in body) to Mode A-C (options in TN Section 5a), strip the `.options-box`, `.option`, `.options-box h4`, `.option strong`, `.option p` CSS rules from the case HTML. The AP13 hook (`check-options-in-body.sh`) pattern-matches CSS class names anywhere in the file and will produce false-positive blocks on dead CSS.
**Enforced by:** `hooks/check-orphan-options-css.sh` — warns when `.options-box {` CSS rule exists but no `<div class="options-box">` is present in body.
**Source:** amodei-india-summit. After Mode D → Mode A-C conversion, residual `.options-box` CSS triggered false-positive AP13 blocks on subsequent edits until the dead CSS was stripped.
