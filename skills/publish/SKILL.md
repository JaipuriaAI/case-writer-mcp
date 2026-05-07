---
name: case-writer-publish
description: Phase 6 of the case-writer pipeline. Bootstrap the canonical renderer (one-time download from this skill repo), invoke it to produce publication-grade case + teaching-note PDFs via WeasyPrint with the Rehearsal brand identity (Playfair Display + Source Serif Pro + Raleway, navy INSTRUCTOR COPY banner, rainbow gradient stripe), verify output, update the case registry, and advance status to PUBLISHED. Use after `case-writer-audit` produces an AUDITED case.
license: MIT
---

# case-writer-publish — Phase 6: PDF Generation & Publication

> Bootstrap the canonical renderer, generate PDFs via WeasyPrint, verify output, update the case registry, and finalize the case.

## When to use

Run after `case-writer-audit` has advanced the spec to `AUDITED`. This is the final phase. After it completes, the case packet is ready for distribution.

## Output

PDFs at `${CASE_OUTPUT_DIR:-./cases}/{slug}/` with spec status `PUBLISHED`.

---

## Step 0 — Load Prior Learnings

1. Load `references/known-corrections.md` — check for any publish-phase learnings.
2. If `./case-writer-learnings.md` exists, load it.

## References to Load

- `references/status-definitions.md` — validate AUDITED status

**Status check:** if `**Status:**` is not `AUDITED`, stop and output the exact error message from `references/status-definitions.md`. Publishing unaudited cases violates academic integrity standards — do not offer workarounds.

---

## Step 6.0 — Bootstrap the Canonical Renderer (FIRST RUN ONLY)

The canonical renderer lives in this skill repo at `assets/scripts/render_case.py`. The first time this skill runs in a workspace, fetch it into the working directory so subsequent invocations can call it locally.

```bash
# If ./scripts/render_case.py is missing, bootstrap from this skill's repo:
mkdir -p ./scripts
if [ ! -f ./scripts/render_case.py ]; then
  # Replace <RAW_REPO_BASE> with the raw URL of this skill repo on whatever host serves it
  # e.g. https://raw.githubusercontent.com/<owner>/<repo>/main
  RAW="${SKILL_REPO_RAW:-https://raw.githubusercontent.com/$SKILL_REPO_SLUG/main}"
  curl -fSL "$RAW/assets/scripts/render_case.py" -o ./scripts/render_case.py || {
    echo "Bootstrap failed. Falling back to inline write — read assets/scripts/render_case.py from this skill's reference set and Write it to ./scripts/render_case.py."
    exit 1
  }
fi
chmod +x ./scripts/render_case.py
```

**Fallback if curl fails or the repo URL is unknown:** the model should read the file `assets/scripts/render_case.py` directly through whatever resource-fetch capability the MCP server exposes (e.g. `mcp__ReadMcpResourceTool` with the skill's `references://` URI), and `Write` the contents to `./scripts/render_case.py` itself. The renderer is plain Python with no external imports beyond WeasyPrint and the standard library, so a verbatim copy works.

Also bootstrap the templates if the renderer expects them in a relative `templates/` directory and they're missing:

```bash
mkdir -p ./templates
for f in case-template.html teaching-note-template.html case-style.css; do
  [ -f "./templates/$f" ] || curl -fSL "$RAW/assets/templates/$f" -o "./templates/$f"
done
```

Once `./scripts/render_case.py` and `./templates/*` exist locally, this bootstrap step is a no-op on subsequent runs.

---

## Step 6.1 — Render via the Canonical Renderer

> **v1.2.0+ rule** (per `references/known-corrections.md`): use the canonical renderer. NEVER write a per-case `render_html.py` and NEVER ad-hoc the HTML. The renderer carries baked-in fixes for the markdown-to-HTML footnote regex bug, the WeasyPrint dropcap crash, the wordmark gradient overhang, and the Rehearsal brand identity (Playfair Display titles, Source Serif Pro body, Raleway accents, navy "INSTRUCTOR COPY" banner with rainbow gradient stripe for the TN).

Invoke:

```bash
python3 ./scripts/render_case.py "${CASE_OUTPUT_DIR:-./cases}/{slug}"
```

The renderer reads `case.md`, `teaching-note.md`, and `spec.md` from the case directory and writes:
- `{slug}-case.html` + `{slug}-case.pdf`
- `{slug}-teaching-note.html` + `{slug}-teaching-note.pdf`

It also runs the **visual-inspection META-RULE** automatically: renders pages to PNG via `pdftoppm`, counts section headers, verifies they match the expected count (≥ 9 for TN), and reports any divergence. Cleans up preview pages on success.

**Override metadata via CLI args** (key=value pairs):

```bash
python3 ./scripts/render_case.py "${CASE_OUTPUT_DIR:-./cases}/{slug}" \
  case_number=GBA-2026-005 \
  rev_date="May 2026" \
  discipline="MBA — Crisis Management" \
  session_length="75 minutes"
```

Supported keys: `slug`, `case_number`, `title`, `subtitle`, `decision_date`, `setting`, `difficulty`, `discipline`, `case_type`, `rev_date`, `word_count`, `session_length`, `author`. Most are extracted automatically from `spec.md` if not provided.

**If WeasyPrint is not installed,** stop and report:

> WeasyPrint is required for PDF generation. Install with `brew install weasyprint` (the binary path is preferred over the Python module on macOS due to libgobject linkage). On Linux: `pip install weasyprint` or use your distro package. On Windows: see <https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows>. After installing, re-run this skill.

---

## Step 6.2 — Verification

After PDF generation:

```bash
ls -lh "${CASE_OUTPUT_DIR:-./cases}/{slug}"/*.pdf
```

Verify:
- Both PDFs exist
- Both are non-zero size (≥ 50 KB expected for a standard case)
- Capture page counts from WeasyPrint's stdout output and report them

If either PDF is missing or zero bytes, check the WeasyPrint output for rendering errors and fix the HTML before re-running.

---

## Step 6.3 — Case Registry Update

Read `${CASE_OUTPUT_DIR:-./cases}/case-registry.md`. Append a row:

| GBA Number | Slug | Title | Case Type | Difficulty | Published |
|-----------|------|-------|-----------|------------|-----------|
| [GBA YYYY-NNN] | [slug] | [title] | [type] | [1–5] | [date] |

Write the updated registry.

---

## Step 6.4 — Status Update and Confirmation

Update spec: `**Status:** PUBLISHED`. Append `- PUBLISHED: [date] — Case packet complete` to Status History.

Output:

```
Case published successfully.

Files:
  ${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-case.html
  ${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-case.pdf            ([X] pages)
  ${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-teaching-note.html
  ${CASE_OUTPUT_DIR:-./cases}/{slug}/{slug}-teaching-note.pdf   ([Y] pages)

GBA Case Number: [GBA YYYY-NNN]
Registered in:   ${CASE_OUTPUT_DIR:-./cases}/case-registry.md
```

---

## Self-Validation Checklist

- [ ] **AUDITED status confirmed** before any rendering work began
- [ ] **`./scripts/render_case.py` and `./templates/*` exist** in the working directory (bootstrapped if missing)
- [ ] **WeasyPrint available** — verified via a smoke test before invocation
- [ ] **Both PDFs generated** and ≥ 50 KB
- [ ] **Visual-inspection META-RULE passed** — section header count matches expected
- [ ] **Case registry updated** with the new row
- [ ] **Status advanced to PUBLISHED** with Status History line appended

## Don't

- Do not write a per-case `render_html.py` or hand-roll the HTML/CSS — the canonical renderer is the only supported path. Per-case scripts reintroduce known bugs (footnote-regex slurp, dropcap float-layout crash, gradient overhang).
- Do not skip the AUDITED status check. Publishing unaudited cases is a hard policy violation.
- Do not edit the templates in `assets/templates/` for case-specific tweaks. If brand styling needs to evolve, edit `assets/scripts/render_case.py` directly and update the canonical asset.
- Do not silently downgrade an unpublishable case (e.g. ignoring a missing PDF). Stop, report the rendering error, and ask the user how to proceed.

## Output

Both PDFs, updated case registry, spec status `PUBLISHED`.
