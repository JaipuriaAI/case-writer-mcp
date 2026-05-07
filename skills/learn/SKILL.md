---
name: case-writer-learn
description: Review accumulated case-writing learnings from prior sessions and propose promotions to permanent rules. Reads ./case-writer-learnings.md (per-workspace) and references/known-corrections.md (permanent). Identifies learnings with recurrence ≥ 2 across cases. Outputs a unified diff against references/known-corrections.md that the user can submit as a pull request to the skill repo. Does NOT write to the hosted repo directly.
license: MIT
---

# case-writer-learn — Manage Case-Writing Learnings

> Review accumulated corrections from prior case-writing sessions. Propose promotions to permanent rules **as a unified diff** the user can submit as a PR.

## When to use

The user has run several cases and wants to consolidate recurring corrections into permanent rules — or an audit captured new learnings that should graduate. Run periodically (every 5–10 cases) or when audit complaints repeat.

## Why a diff (not a write)

In the original plugin, this command wrote directly to the plugin's `shared/known-corrections.md`. In skills-over-mcp, the skill is served from a hosted GitHub repo — the running agent **cannot** write back to it. The PR workflow keeps the canonical rule set under version control while still giving the user a one-keystroke "approve" path: the diff this skill outputs is copy-pasteable straight into `gh pr create` or a manual edit-commit-push.

## Output

A unified diff (or git-formatted patch) against `references/known-corrections.md`, plus an updated `./case-writer-learnings.md` marking promoted entries.

---

## Step 1 — Load Current State

Load `references/learnings-protocol.md` for the taxonomy, lifecycle rules, and entry format.

Then read:
1. `./case-writer-learnings.md` if it exists in the working directory
2. `./case-writer-learnings.jsonl` if it exists (machine-readable counterpart with recurrence counts)
3. `references/known-corrections.md` for already-promoted patterns

If neither learnings file exists, report:

```
No accumulated learnings found in this workspace.
The case-writer-audit skill captures NEW learnings to ./case-writer-learnings.md
during rectification. Run a few audits first.
```

…and exit.

---

## Step 2 — Report Status

Display:

```
Learnings status — ${CASE_OUTPUT_DIR:-./cases}

  ./case-writer-learnings.md
    Total entries:        [N]
    NEW (not promoted):   [N]
    PROMOTED:             [N]
    OBSOLETE:             [N]

  references/known-corrections.md (canonical, served from skill repo)
    Total promoted rules: [N]
    Last update:          [date from `## Recent Updates` section]
```

---

## Step 3 — Identify Promotion Candidates

Scan the local `.md` and `.jsonl` for entries meeting the lifecycle promotion threshold from `references/learnings-protocol.md`:
- Recurrence ≥ 2 across different cases (different slugs)
- Status: NEW
- Not a duplicate of an existing rule in `references/known-corrections.md`

Present candidates to the user:

```
PROMOTION CANDIDATES (recurrence ≥ 2):
─────────────────────────────────────
1. [source_integrity] Ghost citation pattern — seen in 2 cases (paytm, byju)
   Rule: "Every [SN] citation must trace to a verifiable source registry entry.
          During audit, scan the source registry for orphan IDs and the
          narrative for unresolved references."
   → Promote to references/known-corrections.md? (y/n/edit)

2. [narrative_quality] Protagonist dilution — seen in 3 cases
   Rule: "Protagonist must be primary actor in ≥ 60% of narrative paragraphs.
          When secondary characters dominate a section, reframe the section
          through the protagonist's decision-making lens."
   → Promote to references/known-corrections.md? (y/n/edit)
```

For each candidate, the user may:
- `y` — promote as-written
- `n` — skip (stays NEW; will resurface next time)
- `edit` — refine the rule wording before promotion

---

## Step 4 — Generate the Promotion Diff

For all approved promotions:

1. Determine the appropriate category section in `references/known-corrections.md` (read the existing structure — categories like `## Source Integrity`, `## Narrative Quality`, `## Decision Moment`, `## Exhibit Discipline`, etc.)
2. Construct each new entry per `references/learnings-protocol.md` format:
   ```markdown
   ### [N]. [Rule Title]
   
   **Pattern:** [What was wrong, with case example]
   **Rule:** [The corrective rule, action-oriented]
   **Enforcement:** [Where this rule fires — which phase/skill, which check]
   **Promoted:** [date] — recurred in [N] cases ([slug list])
   ```
3. Render the changes as a unified diff against the current `references/known-corrections.md`:

```diff
--- a/references/known-corrections.md
+++ b/references/known-corrections.md
@@ -<lineno>,<count> +<lineno>,<count> @@
 ## Source Integrity
 
 [...existing content...]
+
+### [N]. Ghost Citation Pattern
+
+**Pattern:** ...
+**Rule:** ...
+**Enforcement:** ...
+**Promoted:** [date] — recurred in 2 cases (paytm, byju)
+
 [...existing content continues...]
```

Save the diff to `./case-writer-promotion.patch` and **also** print it inline so the user can copy it.

---

## Step 5 — Update the Local Learnings File

For each promoted entry, mark it in `./case-writer-learnings.md`:

```markdown
### [old date] | audit | [slug]
**Correction:** [unchanged]
**Rule:** [unchanged]
**Applies to:** [unchanged]
**Status:** ~~NEW~~ → PROMOTED → references/known-corrections.md (PR pending)
```

This is a local file the user controls — writing to it is fine.

---

## Step 6 — Output the PR Workflow Hint

Print final instructions:

```
Generated promotion patch: ./case-writer-promotion.patch

To submit:

  cd <your local clone of the case-writer skill repo>
  git checkout -b promote-learnings-$(date +%Y%m%d)
  git apply /full/path/to/case-writer-promotion.patch
  git add references/known-corrections.md
  git commit -m "Promote [N] learnings from audit cycles"
  git push -u origin promote-learnings-$(date +%Y%m%d)
  gh pr create --title "Promote [N] case-writing learnings" \
               --body "Promotes patterns recurring in [N] cases. See diff."

Once merged, every connected agent receives the new rules instantly.
```

---

## Step 7 — Cleanup (Optional)

If the user asks, remove from `./case-writer-learnings.md`:
- Already-promoted entries (older than 30 days)
- Marked-OBSOLETE entries
- Duplicates of known corrections

Never delete entries the user hasn't approved — losing the local history makes it harder to spot regressions.

---

## Self-Validation Checklist

- [ ] **Both candidate lists checked** — `./case-writer-learnings.md` AND `./case-writer-learnings.jsonl` if it exists
- [ ] **Recurrence threshold honored** — only entries with ≥ 2 distinct case slugs in their recurrence record
- [ ] **No duplicates promoted** — checked against existing rules in `references/known-corrections.md`
- [ ] **Diff is well-formed** — applies cleanly with `git apply --check` (test locally if possible)
- [ ] **Local file updated** — promoted entries marked, not deleted
- [ ] **PR workflow hint printed** — user can act on the output without further questions

## Don't

- Do not write to `references/known-corrections.md` from the running agent — that file lives in the hosted skill repo and the agent has no write path. Always produce a diff.
- Do not promote single-occurrence learnings. Recurrence ≥ 2 is the bar — one-off corrections often turn out to be case-specific.
- Do not delete the local `./case-writer-learnings.md` after promotion. Keep it as the rolling history; mark entries promoted instead.
- Do not silently auto-edit the user's wording when they say "edit." Show the proposed refinement and confirm before generating the diff.

## Output

- `./case-writer-promotion.patch` — the unified diff against `references/known-corrections.md`
- Updated `./case-writer-learnings.md` with promoted entries marked
- PR workflow instructions printed to the user
