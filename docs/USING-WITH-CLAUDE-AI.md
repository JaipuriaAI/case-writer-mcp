# Using `case-writer` with a Claude.ai account

> Step-by-step setup for the **claude.ai web/desktop app** (not Claude Code, not the API).
> Plan required: Pro, Max, Team, or Enterprise. Free accounts cannot add custom MCP connectors.

---

## What you're connecting

`case-writer` is a [skills-over-mcp](https://skillsovermcp.com/) repo. Once published to GitHub and registered with skillsovermcp.com, it becomes an MCP endpoint at:

```
https://mcp.skillsovermcp.com/mcp/<your-github-handle>/<repo-name>
```

Claude.ai supports MCP through its **Custom Connectors** feature (sometimes labelled **Integrations** depending on UI version). When connected, all 8 case-writer skills appear in your conversation as callable tools — you invoke them by name (e.g. *"run case-writer-research on this URL"*).

---

## One-time setup (≈ 5 minutes)

### 1. Publish this repo to GitHub

```bash
cd /Users/shivakakkar/Skill-over-mcp-claude-code     # or wherever you cloned/extracted it
git init
git add .
git commit -m "Initial skill-over-mcp port of case-writer v1.2.0"

# create a *public* GitHub repo (skillsovermcp.com requires public until OAuth ships)
gh repo create case-writer-skill --public --source=. --push
# or, manually via the GitHub UI then:
git remote add origin git@github.com:<your-handle>/case-writer-skill.git
git push -u origin main
```

### 2. Register the repo with skillsovermcp.com

1. Go to <https://skillsovermcp.com/>
2. Click **Connect a repo** (or the equivalent CTA)
3. Paste your repo URL: `https://github.com/<your-handle>/case-writer-skill`
4. Confirm. The site validates the SKILL.md files and provisions the MCP endpoint.
5. Copy the resulting URL — it looks like:
   ```
   https://mcp.skillsovermcp.com/mcp/<your-handle>/case-writer-skill
   ```

### 3. Add the connector in Claude.ai

Claude.ai's UI moves around; the path is one of these depending on your version:

| Where | Steps |
|------|-------|
| **Web app** | Profile menu (bottom-left) → **Settings** → **Connectors** (or **Integrations**) → **Add custom connector** |
| **Desktop app** | Same path; menu lives behind your avatar |
| **Mobile app** | Connectors are read-only on mobile — set them up on web/desktop first; they sync automatically |

In the **Add custom connector** dialog:

| Field | Value |
|------|-------|
| Name | `case-writer` (or whatever you'd like to type when invoking) |
| URL  | the `https://mcp.skillsovermcp.com/mcp/...` URL from step 2 |
| Authentication | **None** — skills-over-mcp endpoints are public. (When OAuth ships for private repos, this will change.) |

Save. Claude.ai connects, enumerates the 8 skills, and shows them in the connector's status panel as available tools.

### 4. Enable the connector for a conversation

In a new conversation, click the **+** (attachments) or **tools** icon below the prompt → toggle on **case-writer**. The skills now load into the conversation's context.

You can confirm they're loaded by asking: *"What case-writer skills do you have access to?"* — Claude should list `case-writer-research` through `case-writer-learn`.

---

## How to actually use it

### Quickest path — full pipeline in one prompt

```
Use case-writer-god-mode to generate a complete case packet on the topic:

  "Anthropic / Claude 4 launch and pricing decision / 2025"

Pause for my approval at the source-minimum gate and the publication gate.
Save outputs to ./cases/ in the conversation workspace.
```

god-mode will:
1. Run `case-writer-research` (parallel web research, source triangulation, sufficiency gate)
2. Stop at **HARD PAUSE 1** if it can't gather ≥10 sources / ≥2 Tier 1–2 → ask you to paste more URLs
3. Run `case-writer-plan` with autonomous defaults (Mode A, The Weight, 4 options, Standalone A)
4. Run `case-writer-draft` (writes the case body, exhibits, runs HBS readiness self-check)
5. Run `case-writer-teach` (12 TN sections, tone discipline, length-ratio enforcement)
6. Run `case-writer-audit` (6 audit roles, fixes HARD findings, lists MEDIUM for review)
7. Stop at **HARD PAUSE 2** with a publication summary → you type `YES` to finalize

### Phase-by-phase (more control)

```
Run case-writer-research on this article: https://www.ft.com/...
```

Wait for the DRAFT spec, review, then:

```
Run case-writer-plan on the spec at ./cases/<slug>/<slug>-spec.md.
Use Mode A, The Weight, 4 options, Standalone A.
```

…and so on through `case-writer-draft`, `case-writer-teach`, `case-writer-audit`, `case-writer-publish`.

---

## What works fully on Claude.ai vs what needs your machine

This is the most important section to understand before relying on the workflow.

| Skill | Works in Claude.ai sandbox? | Notes |
|-------|---|---|
| `case-writer-research` | ✅ Yes | Uses Claude.ai's built-in **web search** to gather sources. Falls back to asking you to paste content if a paywall blocks fetching. |
| `case-writer-plan` | ✅ Yes | Pure reasoning + spec editing. No external dependencies. |
| `case-writer-draft` | ✅ Yes | Writes the case HTML using bundled templates from `assets/templates/`. |
| `case-writer-teach` | ✅ Yes | Same — writes the teaching note HTML. |
| `case-writer-audit` | ✅ Yes | Runs the 6 audit roles. If your conversation has the **analysis tool** enabled, audit roles can run as parallel sub-tasks; otherwise they run sequentially. Quality is identical, only wall-clock differs. |
| `case-writer-publish` | ⚠️ **Partial** | Generates HTML fine. **PDF generation requires WeasyPrint**, which is not installed in Claude.ai's sandbox. See "Publishing PDFs" below. |
| `case-writer-god-mode` | ✅ (mostly) | All phases except the PDF step at the end. The HTMLs are produced correctly; you'll need to render PDFs locally. |
| `case-writer-learn` | ✅ Yes | Outputs the unified diff for you to apply in your local clone and PR back. |

### Publishing PDFs (the one hard step)

Claude.ai's sandbox doesn't have WeasyPrint pre-installed and currently can't install system libraries (`libpango`, `libcairo`, etc.) that WeasyPrint needs. You have three options:

**Option A — Render PDFs locally** (recommended):
1. Let Claude.ai run `case-writer-publish` through Step 6.0–6.1; it will produce the HTML and stop with a clear "WeasyPrint not available" message.
2. Download the case directory (case.html, teaching-note.html, spec.md) to your laptop.
3. Install WeasyPrint once: `brew install weasyprint` (macOS) or `pip install weasyprint` (Linux).
4. Clone your skill repo and run:
   ```bash
   python3 ./assets/scripts/render_case.py /path/to/cases/<slug>
   ```
   This produces both PDFs with the canonical Rehearsal brand styling.

**Option B — Use Claude Code or Claude Desktop with the same connector**:
Claude Code on your laptop accepts the same MCP connector URL. Add it via `/connect` (or in `~/.claude.json`), then run god-mode there — the publish step works because your laptop has WeasyPrint. Skills are identical across hosts.

**Option C — Render PDFs via a hosted service**:
Wire WeasyPrint into a small Cloudflare Worker / Vercel function and have the publish skill `curl` the HTML over to it. This is a custom integration outside the scope of the default skill.

### Web search inside Claude.ai

Claude.ai has its own web search and fetch tools built in. The `case-writer-research` SKILL.md is deliberately tool-agnostic — it says *"use whatever web search and fetch tools your client exposes"* — so on Claude.ai it uses the native tools. You don't need a separate Perplexity or Tavily key.

If you want **higher-quality research** (e.g. multi-source triangulation across primary sources), you can additionally connect a Perplexity MCP, Brave-MCP, or Tavily-MCP connector in the same conversation. The skill will use whichever search tool is available; if multiple are present, it can run them in parallel.

---

## Where outputs live

Inside a Claude.ai conversation, "the working directory" is the conversation's **Files** panel (sometimes called the **artifacts** or **sandbox**). The skill writes to `./cases/<slug>/...` relative to that workspace.

To pull files out:
- Click the file in the Files panel → **Download**
- Or ask: *"Zip the entire ./cases/ folder and give me a download link"* — Claude.ai will produce a downloadable archive.

To customize the output location, set the env var when invoking:

```
Run case-writer-research with CASE_OUTPUT_DIR set to ./my-case-library/, on this article: ...
```

---

## Connector lifecycle

| Action | How |
|--------|-----|
| **Update skills** (after a `git push`) | No action needed in claude.ai — skills-over-mcp re-fetches the repo on every conversation start. New SKILL.md content is live within ~40 ms (the platform's median fetch latency). |
| **Disable temporarily** | Settings → Connectors → toggle `case-writer` off. Skills disappear from the tool list. |
| **Remove entirely** | Settings → Connectors → click the connector → **Remove**. Files in your Claude.ai workspace are unaffected. |
| **Move to a different repo** | Re-register the new repo on skillsovermcp.com, get the new URL, edit the connector in claude.ai. |

---

## Troubleshooting

**"The connector says 'unavailable'"**
Skills-over-mcp had a brief outage. Wait 30 seconds and refresh the conversation. If persistent, check <https://skillsovermcp.com/> for status.

**"I asked Claude to use case-writer-research and it said the skill isn't available"**
Make sure the connector is **enabled in this conversation** (the toggle below the prompt, not just the global Settings entry). Each conversation opts in to its tools.

**"It started searching with one tool but I want it to use Perplexity"**
Be explicit in the prompt: *"Use Perplexity for the source triangulation in case-writer-research."* The skills are tool-agnostic by design; you control which search backend gets used.

**"The audit ran but only sequentially — I expected 6 parallel agents"**
Claude.ai's tool-orchestration policy currently runs MCP-tool calls serially within a single message. The audit's 6 roles will execute in sequence. Output quality is identical; total time is ~6x longer than a parallel run on Claude Code.

**"I can't find Connectors / Integrations in my account settings"**
Custom connectors require **Claude Pro** or higher. Check Settings → Plan & Billing. (As of 2026-05, free-tier accounts cannot add custom MCP servers.)

**"WeasyPrint error during publish"**
Expected on Claude.ai (see "Publishing PDFs" above). Run the renderer locally with the HTMLs Claude.ai produced.

---

## What you give up vs Claude Code

If you've used the original `case-writer` Claude Code plugin, here's what's different on Claude.ai:

| Original plugin (Claude Code) | This skill on Claude.ai |
|---|---|
| 9 hooks fire automatically (em-dash counter, theory-vocab grep, protagonist-ratio, etc.) | Same checks run, but as model-driven self-validation at the end of each skill — slightly less reliable than runtime hooks. Mitigated by the explicit checklists in each SKILL.md. |
| 3 specialized subagents (`source-triangulator`, `tn-tone-checker`, `anti-pattern-auditor`) dispatched in parallel | Inline procedures that Claude executes itself. Same coverage; serial timing on Claude.ai. |
| Per-machine install via `/plugin install case-writer@rehearsal-dev` | Connector URL — no install, but no Claude-Code-specific features (slash commands, hooks, agent-tool dispatch). |
| Renders PDFs out of the box | Renders HTMLs; PDFs need a one-time local WeasyPrint install. |

For solo authoring at moderate volume, claude.ai is the simpler path. For high-volume case production with strict quality enforcement, Claude Code on your laptop is still the better target.

---

## Quick reference: invoking each skill on Claude.ai

```
# Phase 1 — Research
"Run case-writer-research on https://www.example.com/article"

# Phase 2 — Plan (after research)
"Run case-writer-plan on the spec at ./cases/<slug>/<slug>-spec.md"

# Phase 3 — Draft (after plan)
"Run case-writer-draft on <slug>"

# Phase 4 — Teach (after draft)
"Run case-writer-teach on <slug>"

# Phase 5 — Audit (after teach)
"Run case-writer-audit on <slug>"

# Phase 6 — Publish (after audit)
"Run case-writer-publish on <slug>"
# Note: stops at HTML; render PDFs locally with assets/scripts/render_case.py

# Full pipeline
"Run case-writer-god-mode on <topic-or-URL>"

# Promote learnings to permanent rules
"Run case-writer-learn — review accumulated learnings and produce a promotion diff"
```

That's everything. The skills handle the rest.
