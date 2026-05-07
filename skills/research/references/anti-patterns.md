# Anti-Patterns Reference
**Version:** 1.0.0
**Loaded by:** `:audit` agents (especially Agent 3: Narrative Quality, Agent 6: Anti-Pattern Sweep)

Detect and fix these 13 anti-patterns before publication. HARD severity blocks publication. MEDIUM severity flags for user review.

---

## AP1 — Answer-in-the-Case Bias
**Severity:** HARD
**Description:** One option is presented with language that makes it obviously superior — the author's preferred choice shows through the framing. Students can identify the "correct" answer by reading tone rather than by analyzing trade-offs. AP1 applies to options wherever they appear: Mode C/D case body prose and TN Section 5a. In Modes A-B, there are no options in the body to check.

**Detection heuristic:** Scan all option descriptions for evaluative adjectives that appear on only one option ("brilliant", "obvious", "clearly superior", "the only viable path", "the elegant solution"). Check whether one option's risk/cost section is shorter, softer, or contains fewer drawbacks than the others.

**Correction:** Rewrite each option's trade-off section to equal rhetorical weight. Every option must have at least one genuine strength and one genuine cost of comparable severity. No option should sound like the author's favorite.

**Example:**
- BAD: "Option 3 offered the elegant solution of capturing both objectives simultaneously, while Options 1 and 2 each had serious drawbacks."
- GOOD: "Each option presented distinct trade-offs. Option 1 preserved the partnership but risked talent dispersion. Option 2 secured the talent but risked the $13 billion investment. Option 3 attempted both but required precise execution under extreme time pressure."

---

## AP2 — Data Dumping
**Severity:** HARD
**Description:** A section contains more than 500 words of facts and data without a narrative thread linking that data to the protagonist's situation. The reader receives information but no reason to care about it.

**Detection heuristic:** Count words in consecutive fact-heavy paragraphs within any single section. If any section runs 500+ words without at least one paragraph containing narrative tension or the protagonist's perspective, flag it.

**Correction:** Intercut factual paragraphs with narrative paragraphs that connect facts to the protagonist's decision context. Move excess background data to exhibits. Each factual block must earn its place by raising the stakes or sharpening the dilemma.

**Example:**
- BAD: [Six consecutive paragraphs of market share data, financial ratios, and organizational chart descriptions with no reference to what this means for the protagonist's decision]
- GOOD: [Three paragraphs of data] + [One paragraph: "These numbers put Nadella in an uncomfortable position: Microsoft's $13 billion was at risk, but pulling it back would signal weakness to every future AI partner."] + [remaining data]

---

## AP3 — Hindsight Contamination
**Severity:** HARD
**Description:** Post-decision facts appear in the pre-decision narrative. The author knows how the story ends and inadvertently telegraphs the outcome, destroying the student's ability to reason under genuine uncertainty.

**Detection heuristic:** Identify the temporal freeze point (the exact decision moment). Read every paragraph before that freeze point. Flag any sentence containing: post-decision stock prices, outcome language ("would later prove", "this decision sealed", "the gamble paid off"), or events that occurred after the decision date.

**Correction:** Remove or move all post-decision facts to the Teaching Note epilogue section. Rewrite any forward-looking or outcome-signaling language. The pre-decision narrative must end at genuine uncertainty.

**Examples of contamination to remove:**
- "This decision would prove to be Nadella's masterstroke."
- "The gamble paid off when Microsoft's share price reached..."
- "Little did the board know that within six months..."
- "In hindsight, the signs were already visible..."

---

## AP4 — Source Monoculture
**Severity:** HARD
**Description:** A single source provides more than 25% of the narrative's factual content. This creates a case that is essentially a summary of one reporter's or analyst's perspective rather than a triangulated account.

**Detection heuristic:** Count [SN] citation tags throughout the case. Tally how many cited paragraphs reference each source number. If any single [SN] appears in more than 25% of all cited paragraphs, flag it.

**Correction:** Research additional independent sources to corroborate the over-relied-upon source's information. Redistribute citations so no single source exceeds 25% of cited content. Prioritize Tier 1-2 sources for the additional research.

**Example:**
- BAD: [S1] cited in 14 of 20 cited paragraphs (70% share)
- GOOD: [S1] in 4 paragraphs, [S2] in 4 paragraphs, [S3] in 3 paragraphs, [S4] in 3 paragraphs, [S5] in 2 paragraphs, [S6] in 2 paragraphs (max 20% share)

---

## AP5 — Generic Opening
**Severity:** HARD
**Description:** The case opens with industry context, company history, market size statistics, or any sentence where the protagonist is not present and placed in a specific moment. Students feel no urgency and disengage before the dilemma becomes clear.

**Detection heuristic:** Read the first 3 sentences of the case. If the protagonist is not named and placed in a specific situation — a date, a room, a phone call, a decision — by sentence 3, flag it.

**Correction:** Rewrite the opening to lead with the protagonist's specific moment. See `opening-protocol.md` for the four permitted opening frames (The Call, The Room, The Number, The Deadline).

**Examples:**
- BAD: "The global artificial intelligence industry was valued at $142 billion in 2023, growing at 37% annually as competition intensified between technology giants."
- BAD: "Founded in 2015 as a non-profit research lab, OpenAI had become one of the most influential AI companies in the world by 2023."
- GOOD: "On November 17, 2023, Satya Nadella learned of Sam Altman's firing one minute before the public announcement. He had 72 hours to decide how Microsoft would respond."

---

## AP6 — Temporal Confusion
**Severity:** MEDIUM
**Description:** The narrative jumps more than 6 months in time within a single section without a transitional phrase explaining the time jump. Students lose their temporal footing and cannot track the sequence of events.

**Detection heuristic:** In each section, note the dates mentioned across paragraphs. Flag any paragraph-to-paragraph transition that spans more than 6 months without an explicit temporal connector at the start of the new paragraph.

**Correction:** Add temporal connector phrases at section transitions. Consider restructuring sections along a cleaner chronological spine. Examples of acceptable connectors: "Two years later...", "By mid-2023...", "Three months after the acquisition...", "In the months following..."

**Example:**
- BAD: [Paragraph ending in January 2022] → [Paragraph beginning "The board reconvened to address the situation..." — set in September 2023]
- GOOD: [Paragraph ending in January 2022] → "Twenty months later, in September 2023, the board reconvened to address the situation..."

---

## AP7 — Exhibit Orphaning
**Severity:** HARD
**Description:** An exhibit exists without being referenced in the narrative, or the narrative references an exhibit that doesn't exist. Orphaned exhibits confuse students. Phantom references create dead ends.

**Detection heuristic:** For each exhibit (Exhibit 1, 2, 3...), search the narrative for "(see Exhibit N)" or "Exhibit N appears in" — if not found in the narrative, it is orphaned. For each narrative reference to "Exhibit N", verify the exhibit document exists.

**Correction:** For orphaned exhibits — either add a narrative reference in the appropriate section or remove the exhibit entirely. For phantom references — either add the missing exhibit or remove the narrative reference.

**Example:**
- BAD: Exhibit 3 titled "Microsoft Financial Timeline" exists, but no sentence in the narrative mentions Exhibit 3.
- GOOD: In the narrative: "Microsoft's financial exposure grew significantly over the partnership period (see Exhibit 3)."

---

## AP8 — Fabricated Deliberation
**Severity:** HARD
**Description:** The case describes internal thoughts, private conversations, or mental states of living individuals without attribution to a public source. This is an academic integrity violation and a legal risk.

**Detection heuristic:** Scan all narrative text for these patterns attributed to named individuals: "[Name] thought...", "[Name] believed...", "[Name] considered...", "[Name] knew that...", "[Name] felt...", "[Name] was certain...", "[Name] decided to..." — flag every instance and verify that a public source documents this mental state or deliberation.

**Correction:** Restructure as action + source attribution. If no source documents the mental state, delete the unattributed attribution entirely and describe observable behavior instead.

**Examples:**
- BAD: "Nadella believed that losing Altman would be catastrophic for Microsoft's AI ambitions."
- GOOD: "In a subsequent interview, Nadella described the situation as 'a critical inflection point' for Microsoft's AI strategy [S4]."
- BAD: "The board felt it had no choice but to act immediately."
- GOOD: "Within 24 hours of the announcement, the board had convened an emergency session [S2]."

---

## AP9 — Present Tense Narration
**Severity:** MEDIUM
**Description:** Narrative text uses present tense outside of direct quotes. Present tense signals opinion or ongoing state, not documented historical fact. It also creates false immediacy that undermines the case's analytical credibility.

**Detection heuristic:** Scan all non-quote sentences for present tense verbs. Flag: "The company operates...", "Nadella faces...", "The board believes...", "Microsoft is...", "The challenge represents..."

**Correction:** Convert all narrative to past tense. Exception: Direct quotes retain the original speaker's tense.

**Examples:**
- BAD: "The company operates in one of the most competitive markets in technology history."
- GOOD: "The company operated in one of the most competitive markets in technology history."
- Exception (retain as-is): Nadella said, "OpenAI is the most important partnership we have."

---

## AP10 — Dominant Option Signal
**Severity:** HARD
**Description:** Similar to AP1 but more subtle. One option's trade-offs are framed with softer language, shorter word count, or fewer drawbacks than the others — without any obviously biased adjective. The imbalance is structural, not lexical. AP10 applies to TN Section 5a options analysis and Mode C/D case body passages.

**Detection heuristic:** Count the word count of each option's description section. Measure the number of distinct drawbacks listed for each option. Compare the severity language across options' risk paragraphs (words like "catastrophic", "risked", "threatened" vs. "challenging", "required", "would need"). If any option's risk section is more than 25% shorter or uses notably softer language than the strongest option, flag it.

**Correction:** Add equivalent trade-offs to the underspecified option. Ensure each option's risk paragraph is as substantive and rhetorically energetic as the strongest option's risk paragraph. Imbalance in word count or severity language is a proxy for author preference leaking through.

**Example:**
- BAD: Option 1 description = 180 words, 3 drawbacks with "catastrophic risk" language. Option 3 description = 90 words, 1 drawback with "execution challenge" language.
- GOOD: Option 1 = 175 words, 3 drawbacks. Option 3 = 165 words, 3 drawbacks. Severity language comparable across both.

---

## AP11 — Missing Attribution
**Severity:** MEDIUM
**Description:** Three or more consecutive narrative paragraphs contain factual claims without a source citation. Even well-known facts require sourcing in academic case writing to demonstrate triangulation.

**Detection heuristic:** Scan the narrative for runs of 3+ consecutive paragraphs without any [SN] citation tag. Flag each such run. Note: transition sentences, conjunctions, and narrative connectors between paragraphs count toward the run length.

**Correction:** Identify the source for the claims in the unattributed paragraphs and add citations. If information cannot be sourced, rephrase as "publicly available reports indicate..." or remove the claim.

**Example:**
- BAD: [Para 1: factual claim, no citation] [Para 2: factual claim, no citation] [Para 3: factual claim, no citation] [Para 4: factual claim, no citation]
- GOOD: [Para 1: factual claim [S1]] [Para 2: factual claim [S1, S3]] [Para 3: factual claim [S2]] [Para 4: factual claim [S4]]

---

## AP12 — Quote Fabrication
**Severity:** HARD
**Description:** A direct quote — text in quotation marks attributed to a named individual — does not appear in the source registry or cannot be traced to a published source. Fabricated quotes are an academic integrity violation and a legal risk.

**Detection heuristic:** For every direct quote in the case (text inside quotation marks attributed to a named person), verify that the source registry contains an entry matching: same speaker, same approximate time period, and a publication type that would plausibly contain this quote. If no matching source exists, flag it.

**Correction:** Option 1 — Locate the published source (interview, article, earnings call transcript, public statement), add it to the source registry, and cite it. Option 2 — Convert the fabricated quote to attributed paraphrase: "According to [Source], [Name] indicated that..." Option 3 — Delete the quote entirely.

**Example:**
- BAD: Nadella said, "We are fully committed to making this work regardless of the board's decision." [No source in registry]
- GOOD (paraphrased): According to a Financial Times report published November 20, 2023, Nadella signaled Microsoft's commitment to the partnership regardless of OpenAI's governance outcome [S7].

---

## AP13 — Structured Options in Case Body
**Severity:** HARD (Modes A-C) / N/A (Mode D)
**Description:** The case body contains a structured options section — an enumerated list of alternatives, an "Options Available to [Protagonist]" box, or any author-constructed menu of choices. In Modes A-C, this violates the interrupted narrative tradition (Gragg 1940, Naumes & Naumes). Options analysis belongs exclusively in Teaching Note Section 5a. Mode D explicitly permits structured options for scaffolded contexts.

**Detection heuristic:** Search the case body HTML for: `options-box` class, "Options Available" text, "Option A/B/C" or "Option 1/2/3" labels, or any ordered list of 3+ alternatives in the final section each beginning with a named option. Also flag any paragraph containing "three options" or "[protagonist] had [N] choices" followed by an enumerated list. Check the spec's "Case Architecture Decisions" section for the selected ending mode — if Mode D, this anti-pattern does not apply.

**Correction:** Remove the structured options section entirely. Replace with a temporal freeze ending per the selected freeze style (see `decision-point-design.md`). Move the options analysis to Teaching Note Section 5a. If the options were sourced from public reporting (documentary evidence test passes), consider switching to Mode C (narrative-embedded deliberation) instead of removing entirely.

**Mode exceptions:**
- Mode C narrative-embedded options (sourced prose, no labels) are NOT flagged by AP13
- Mode D structured fork is expected behavior — AP13 does not apply

**Example:**
- BAD (in Mode A): "Options Available to Nadella: Option 1 — Accept reinstatement. Option 2 — Negotiate conditions. Option 3 — Join Microsoft."
- GOOD (Mode A): "The careers of 770 employees, a $13 billion investment, and the future of the partnership all hung on what he said next. The choice could not wait."
- GOOD (Mode C): "According to the Financial Times, Nadella weighed three paths: accepting reinstatement on the board's terms, negotiating new governance conditions, or formalizing the offer to bring Altman to Microsoft [S7]."

---

## AP14 — Theory Vocabulary in Case Body
**Severity:** HARD
**Description:** The case body uses academic framework names, OB/strategy terminology, or analytical labels that belong in the teaching note. Academic vocabulary signals the author's interpretive frame and pre-closes the analytical work students should do themselves. The case provides evidence; the teaching note provides theory.

**Detection heuristic:** Scan case body for:
- Named frameworks: "structural holes," "principal-agent," "disruptive innovation," "founder imprinting," "organizational identity theory," "exit voice loyalty," etc.
- OB/strategy jargon: "epistemic authority," "bonding capital," "bridging capital," "network brokerage," "charismatic authority," "legitimate authority," "referent power," etc.
- Interpretive labels that package evidence into conclusions: "the idealist's trap," "the governance paradox," "the identity constraint," etc.
- Authorial conclusions disguised as description: "his authority was epistemic," "the board's concerns were substantive," "social capital proved more powerful," "the asymmetric power of social capital"

**Correction:** Replace academic vocabulary with ordinary language that describes the same phenomenon without naming the theory:
- "structural hole brokerage" → "his network connected groups that otherwise had no contact with each other"
- "epistemic authority" → "people followed him because his predictions about the technology had repeatedly proven correct"
- "the board's concerns were substantive" → "the board cited specific instances" (let the reader judge whether they were substantive)
- "bonding capital within the EA community but zero bridging capital to employees" → "strong relationships within the AI safety community but no direct channel to employees or investors"

**The test:** Could a first-year MBA student who has not yet taken OB read this sentence and understand it without recognizing it as theory? If the sentence requires knowledge of a named framework to parse, move the concept to the TN.

**Example:**
- BAD: "Altman's power derived from structural hole brokerage across employees, investors, and the media — three constituencies the board had no bridging capital to activate."
- GOOD: "Altman's network connected employees, investors, and journalists — three groups the board had no direct relationship with. The board could fire the CEO; it could not reach the people who would decide whether the firing stuck."

---

## AP15 — Protagonist Dilution
**Severity:** MEDIUM
**Description:** A secondary character receives more dramatic material, narrative space, or emotional charge than the named protagonist. This causes the reader to drift into "compare two people" rather than "decide what the protagonist should do." The case loses its single teaching spine.

**Detection heuristic:**
1. Count paragraphs where the protagonist is the grammatical subject or primary actor vs. paragraphs where a secondary character is.
2. Identify the single most dramatic scene in the case. If the protagonist is NOT the primary actor in that scene, flag it.
3. If any secondary character appears in >40% of narrative paragraphs, flag it.

**Correction:** Restructure so the protagonist's perspective frames secondary characters' actions. Instead of narrating what Altman did in November 2023, narrate what Amodei observed, concluded, or built in response. Every scene involving a secondary character should connect back to the protagonist's decision context within 1-2 paragraphs.

**The test:** Cover all sections about the secondary character. Does the remaining case still make sense and drive toward the protagonist's decision? If yes, those sections need tighter integration. If no, they are load-bearing and should be reframed through the protagonist's eyes.

**Example:**
- BAD: A 1,000-word section narrating Altman's board crisis as a self-contained drama with its own arc, characters, and resolution. The protagonist (Amodei) is absent from this section entirely.
- GOOD: A 600-word section narrating the board crisis as Amodei would have experienced it — watching from outside, drawing conclusions that shaped Anthropic's governance design. Each paragraph connects back to the protagonist's subsequent decisions.
