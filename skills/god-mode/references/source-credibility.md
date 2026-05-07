# Source Credibility Protocol
# Loaded by: atomic-case-writer during research and drafting phases
# Apply these rules during every phase that involves sourcing or citing information.

---

## 7-Tier Source Hierarchy

You must classify every source against this hierarchy before using it. The tier determines how you may use the source and how much weight it carries.

| Tier | Type | Examples | Usage |
|------|------|----------|-------|
| 1 | Legally mandated filings | SEC 10-K, 10-Q, proxy statements, court filings, regulatory orders, Hansard | Financial data, governance, legal obligations — state as fact, no corroboration needed |
| 2 | Major wire services & record papers | WSJ, FT, Bloomberg, Reuters, NYT, The Economist, BBC | Industry context, events, market dynamics — high weight |
| 3 | Industry analyst reports | McKinsey, BCG, Gartner, Forrester, S&P, Moody's, IBISWorld | Market sizing, benchmarking, trend analysis |
| 4 | Academic journals | Peer-reviewed publications, SSRN working papers | Theoretical frameworks, validated findings |
| 5 | Trade publications | TechCrunch, The Information, trade-specific outlets | Technical detail, niche context — requires corroboration from another source |
| 6 | Company communications | Press releases, earnings transcripts, CEO letters, corporate blogs | Announcements, strategy statements — always attribute ("the company stated") |
| 7 | Social media & forums | Twitter/X, Reddit, LinkedIn, Glassdoor | Documented public statements only — never use for factual claims |

**Never treat a Tier 5–7 source as your primary evidence for a key factual claim.** Always seek corroboration from Tier 1–3 before including the claim in the case narrative.

---

## CRAAP Test

Apply the CRAAP test to every source during the research phase. Reject any source that fails 3 or more criteria.

- **Currency:** How recent is the source? For events in fast-moving industries (tech, finance, crypto), prefer sources published within 6 months of the case's decision point.
- **Relevance:** Does this source directly address the case subject, protagonist, or decision? Tangential sources do not count toward your minimum source count.
- **Authority:** Is there a named author with verifiable credentials? Does the outlet have editorial standards and a correction policy?
- **Accuracy:** Can the claims within this source be cross-verified against another independent source? Does the source itself cite its own sources?
- **Purpose:** Is this source informational or promotional? Promotional sources (press releases, sponsored content, native advertising) are downweighted — treat them as Tier 6 regardless of publication.

---

## Source Volume Rules

You must meet these minimums before drafting any case section. Do not draft with incomplete sourcing.

- Decision Case, Descriptive, Exploratory: **minimum 15 independent sources**
- Mini-Case or Caselet: **minimum 8 independent sources**
- Series Cases (all parts combined): **minimum 20 independent sources**
- No single source may provide more than **25% of the narrative's factual foundation**
- Every case must include **at least 3 Tier 1 or Tier 2 sources**

"Independent" means published by different organizations with no editorial overlap. Two articles from the same newspaper count as one source unless authored independently on separate dates.

---

## Triangulation Requirements

Every key factual claim in the case must pass triangulation before inclusion.

- **Convergent triangulation:** Two or more independent sources must confirm each key factual claim. A single source is insufficient for claims about revenue, headcount, market share, strategic decisions, or personnel actions.
- **Complementary triangulation:** Where possible, combine quantitative data (financial filings, stock data) with qualitative accounts (interviews, reporting). A claim supported by both carries maximum weight.
- **Divergent acknowledgment:** When two sources conflict on the same fact, you must present both versions in the case narrative and note the discrepancy explicitly. Never silently pick one version and suppress the other.
- **Temporal triangulation:** Cross-reference same-event accounts from different time periods. Early reporting and retrospective analysis often reveal details the other misses.
- **Direct quotes:** Every direct quote must cite a specific published source with publication name and date. Never write "reportedly said" for an attributed direct quote — you either have the source or you drop the quote.

---

## Internet Source Techniques

Use these sources for primary document retrieval before resorting to news interpretation:

- **SEC EDGAR** (edgar.sec.gov) — US public company 10-K, 10-Q, proxy filings, S-1s
- **Wayback Machine** (web.archive.org) — historical snapshots of company pages, press releases, and product pages at a specific date
- **Earnings call transcripts** — Seeking Alpha, Motley Fool, or the company's own investor relations page. These are verbatim and cite the speaker directly.
- **CEO letters in annual reports** — often the richest source of protagonist voice and strategic reasoning. Pull quotes and cite year and page.
- **Congressional records and parliamentary Hansard** — for regulatory, legislative, or policy cases. These are Tier 1 sources.
- **Court dockets** — PACER (pacer.gov) for US federal court cases. Exhibits filed in litigation are Tier 1.

---

## Red Flags — Reject These Sources

Reject any source exhibiting one or more of the following:

- Single-source story with no independent corroboration anywhere in the public record
- Revenue or financial claims for a private company without a named, documented source
- Attribution to "industry sources," "people familiar with the matter," or "sources close to the company" without any named corroboration elsewhere
- Blog posts, Substack newsletters, or opinion columns presented as news reporting
- Information older than 3 years for fast-moving industries (tech, fintech, crypto, AI) unless the claim is historical context that has not changed
- Native advertising, sponsored content, or branded research (regardless of publication)
- Wikipedia as a primary source — you may use it to identify primary sources, then retrieve those primary sources directly

If a source you want to use triggers any red flag, find a clean corroborating source before including the claim. If no corroborating source exists, cut the claim.

---

## Private Company Financial Claims — Extra Hedging Required

When the case involves a private company (no public financial filings), apply these additional constraints:

1. **In-prose hedging is mandatory** for every financial figure:
   - "estimated at approximately $14 billion" NOT "$14 billion"
   - "reportedly valued at" NOT "valued at"
   - "according to [Source], revenue reached" NOT "revenue reached"

2. **Source naming is mandatory** for every financial claim:
   - Each financial figure must name its source in the prose itself, not just in the source registry
   - "Epoch.ai estimated that Anthropic's annualized revenue had reached approximately $14 billion" — source named inline

3. **Exhibit disclaimers** must state:
   - "Figures are estimates based on analyst reports and press coverage; not derived from audited financial statements."
   - NOT just "not independently audited" — specify what they ARE derived from

4. **Conflicting estimates** must be surfaced:
   - If two sources give different revenue figures, present both with attribution, don't silently pick one

---

## Living Executive Caution

Cases about living executives carry additional legal and reputational exposure. Apply these constraints in addition to the standard hedging protocol:

1. Never characterize personality, leadership style, or moral character beyond what documented sources support (see `shared/hedging-protocol.md`)
2. Allegations by other individuals (e.g., board members accusing a CEO of lying) must ALWAYS be attributed with source citation, never presented as established fact
3. The word "lying" should appear only inside quotation marks attributed to a named source — never in the author's voice
4. Include a "Note on Sources" paragraph at the end of the case body, before the source registry:
   "This case relies on publicly available information. The subjects of this case were not interviewed. Characterizations of individuals' motivations and internal deliberations are drawn from published interviews and court materials as cited."
