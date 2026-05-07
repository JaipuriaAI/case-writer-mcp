# case-writer — a Skill-Over-MCP for Harvard-style teaching cases

> Generate publication-grade Harvard-style MBA teaching cases (case body + teaching note + PDFs) from a single prompt — research, plan, draft, teach, audit, publish.
>
> Distributed as a [skills-over-mcp](https://skillsovermcp.com/) repo: any MCP client (Claude Code, Cursor, Codex, Claude Desktop) connected to the URL below loads all eight skills automatically.

---

## What this gives you

Eight composable skills that together form a 6-phase HBS-quality case-writing pipeline:

| Skill | Phase | What it does |
|------|-------|--------------|
| `research` | 1 | Triangulate sources, identify protagonist, pick case type, write DRAFT spec |
| `plan` | 2 | Lock structural decisions (case type, options, exhibits, learning objectives) — HARD approval gate |
| `draft` | 3 | Write the case narrative section by section, generate exhibits, assemble HTML |
| `teach` | 4 | Write all 12 teaching-note sections (model answers, board plan, theory connections, epilogue) |
| `audit` | 5 | Run 6 parallel quality auditors (source integrity, narrative quality, decision moment, exhibits, TN depth, anti-patterns AP1–AP15) |
| `publish` | 6 | Bootstrap the canonical renderer, generate publication-grade PDFs via WeasyPrint, update the case registry |
| `god-mode` | all | Orchestrator: runs phases 1–6 autonomously with sensible default decisions; pauses only at source-minimum and publication |
| `learn` | meta | Review accumulated learnings, propose promotions to permanent rules as a unified diff |

Quality is enforced through:
- **15 anti-patterns** (AP1–AP15) with detection heuristics — each affected SKILL.md ends with a self-validation checklist that bakes the original plugin's hooks into mandatory model checks
- **Source-credibility tier hierarchy** + CRAAP test with hard minimums (≥15 sources, ≥3 Tier 1–2, ≤25% single-source share)
- **Teaching-note tone discipline** — no banned phrases, no moral verdicts, no asymmetric advocacy
- **Mode-aware decision-moment design** (A: Pure Interrupted / B: Implied Tension / C: Narrative Deliberation / D: Structured Fork)

---

## Connect it

1. Visit <https://skillsovermcp.com/> and connect this repo (`<your-fork>/Skill-over-mcp-claude-code`).
2. Add the generated MCP URL to your client:
   ```
   https://mcp.skillsovermcp.com/mcp/<owner>/<repo>
   ```
3. The eight skills appear with names like `case-writer-research`, `case-writer-plan`, etc. Invoke them by name.

That's it. There is no per-machine install, no secret to provision, no cron, no cluster. Push a change to `main` and every connected agent has it on next invocation.

### Client-specific guides

- **Claude.ai (web / desktop, Pro+ plans):** [`docs/USING-WITH-CLAUDE-AI.md`](docs/USING-WITH-CLAUDE-AI.md) — covers Connectors UI, conversation enablement, the WeasyPrint sandbox limit on `publish`, and a quick-reference of invocation prompts.
- **Claude Code, Cursor, Codex:** add the MCP URL through your client's standard MCP-server configuration. All eight skills appear automatically; no per-client adjustments needed.

---

## How this differs from the original plugin

This repo started as the `case-writer` plugin v1.2.0 in the [rehearsal](https://rehearsal.app) Claude Code marketplace. Porting to skills-over-mcp made eight intentional changes:

| Original plugin | This skill repo |
|-----------------|-----------------|
| `${CLAUDE_PLUGIN_ROOT}/shared/X.md` | `references/X.md` (root-level, single canonical copy) |
| `/Users/shivakakkar/cases/{slug}` (hardcoded) | `${CASE_OUTPUT_DIR:-./cases}/{slug}` (cwd-relative) |
| `mcp__perplexity__perplexity_search`, `mcp__claude_ai_Parallel_Web__*` | "use whatever web search/fetch tool your client exposes" — methodology, not vendor |
| 9 hooks (PostToolUse / PreToolUse / SessionStart) | Inline **Self-Validation Checklist** at the end of each affected skill |
| 3 specialized subagents (`source-triangulator`, `tn-tone-checker`, `anti-pattern-auditor`) | Inline prompts inside the skills that used them, with optional Task-tool dispatch fallback |
| 8 slash commands `/case-writer:research` etc. | 8 SKILL.md files — invoked by name through any MCP client |
| `scripts/render_case.py` baked into plugin install | Bootstrapped on first run by `publish` (curl → `./scripts/render_case.py`) |
| `learn` writes back to plugin's `shared/known-corrections.md` | `learn` outputs a unified diff against `references/known-corrections.md` for the user to submit as a PR |

Everything else — anti-pattern definitions, source tier hierarchy, decision-point design rules, teaching-note 12-section protocol, the canonical Rehearsal brand identity in the renderer (Playfair Display + Source Serif Pro + Raleway, navy "INSTRUCTOR COPY" banner, rainbow gradient stripe) — is preserved verbatim.

---

## Repo layout (chosen explicitly: root-level `references/`)

The skills-over-mcp specification is layout-agnostic. This repo intentionally stores the 14 shared protocol files **once** at the repo root rather than duplicating them inside every skill folder. This keeps the canonical knowledge in a single place; updating `anti-patterns.md` flows to all eight skills automatically.

```
.
├─ README.md                                # this file
├─ LICENSE                                  # MIT
├─ references/                              # 14 canonical protocols, loaded by SKILL.md files
│  ├─ anti-patterns.md                      # AP1–AP15 with detection heuristics
│  ├─ case-spec-template.md                 # the spec document format
│  ├─ case-type-taxonomy.md                 # 8 case types + selection flowchart
│  ├─ decision-point-design.md              # ending modes A/B/C/D, temporal freeze, options
│  ├─ difficulty-calibration.md             # 5-level Bloom-mapped calibration
│  ├─ exhibit-design.md                     # exhibit numbering, sourcing, formatting
│  ├─ hedging-protocol.md                   # attribution language for secondary sources
│  ├─ known-corrections.md                  # promoted patterns from prior sessions
│  ├─ learnings-protocol.md                 # capture-stage-promote lifecycle
│  ├─ opening-protocol.md                   # 4 permitted opening frames + first-paragraph rules
│  ├─ source-credibility.md                 # tier hierarchy + CRAAP + minimums
│  ├─ status-definitions.md                 # spec status validation + transitions
│  ├─ teaching-note-protocol.md             # 12 mandatory TN sections, tone discipline
│  └─ writing-standards.md                  # tense, prose, international audience
├─ assets/
│  ├─ templates/
│  │  ├─ case-template.html
│  │  ├─ teaching-note-template.html
│  │  └─ case-style.css
│  └─ scripts/
│     └─ render_case.py                     # canonical renderer (Markdown→HTML→PDF, bootstrapped on first publish)
└─ skills/
   ├─ research/SKILL.md
   ├─ plan/SKILL.md
   ├─ draft/SKILL.md
   ├─ teach/SKILL.md
   ├─ audit/SKILL.md
   ├─ publish/SKILL.md
   ├─ god-mode/SKILL.md
   └─ learn/SKILL.md
```

Every reference file inside a SKILL.md uses a path relative to the repo root: `references/anti-patterns.md`, `assets/templates/case-template.html`, etc. There is no `${CLAUDE_PLUGIN_ROOT}` or other host-specific token.

---

## Output location

All generated cases land at `${CASE_OUTPUT_DIR:-./cases}/{slug}/` in the directory the agent is running from. Override by exporting `CASE_OUTPUT_DIR=/your/path` before invoking the skill.

A case directory contains:
```
cases/{slug}/
├─ {slug}-spec.md                # spec with Status (DRAFT → APPROVED → DRAFTED → TN COMPLETE → AUDITED → PUBLISHED)
├─ {slug}-case.html              # rendered case body
├─ {slug}-case.pdf               # PDF for student distribution
├─ {slug}-teaching-note.html     # rendered TN
└─ {slug}-teaching-note.pdf      # instructor copy
```

A `cases/case-registry.md` table tracks every published case across the workspace.

---

## Acknowledgements

- The skills-over-mcp pattern and supporting MCP infrastructure: <https://skillsovermcp.com/>
- The original `case-writer` plugin and its 1.2.0 hardening cycle (paytm-fintech-crossroads, boeing-737-max-grounding-decision, jnj-tylenol-tragedy, zomato-blinkit-quick-commerce, amodei-india-summit, byju-empire-collapse) — every promoted correction in `references/known-corrections.md` is a lesson from a real case
- Harvard Business School case-method tradition; CRAAP source evaluation framework; Bloom's taxonomy

License: MIT.
