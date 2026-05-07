#!/usr/bin/env python3
"""
case-writer/scripts/render_case.py — canonical renderer for Rehearsal cases.

Reads a case packet directory containing case.md and teaching-note.md and emits:
  - {slug}-case.html
  - {slug}-case.pdf
  - {slug}-teaching-note.html
  - {slug}-teaching-note.pdf

Embeds the Rehearsal brand identity (wordmark with rainbow gradient bar) and the
canonical editorial typography (Playfair Display titles, Source Serif Pro body,
Raleway accents) into a single self-contained HTML file per output.

Usage:
    python3 render_case.py <case-directory>
    python3 render_case.py ./cases/boeing-737-max-grounding-decision-2019

The directory must contain:
    case.md             — case body markdown (sections 1-N + exhibits)
    teaching-note.md    — TN markdown (9 canonical sections per teaching-note-protocol.md)
    spec.md             — spec with case metadata (slug, title, case-number, level, length)

Output goes back into the same directory.

Bug fixes baked in (vs. pre-v1.2.0 ad-hoc renderers):
  - Footnote definition regex is paragraph-bounded (not greedy DOTALL with EOF terminator).
    Prior bug: `(.+?)(?=^__FN_|\Z)` slurped case body into footnote 1's definition.
    Fix:       `(.+?)(?=\n\n|\Z)` stops at the next blank line.
  - Drop cap is rendered via inline `<span class="dropcap">` wrapper, NOT
    `::first-letter { float: left }`. Prior bug: WeasyPrint crashed with
    AssertionError in float_layout. Fix: vertical-align + larger font-size.
  - Wordmark gradient rect width is 220 (not 280 from brand-kit master).
    The rect at 280 overshoots the actual rendered "Rehearsal" text width.
"""

import re
import sys
import shutil
import subprocess
from pathlib import Path

# ── Rehearsal Wordmark (gradient bar fitted to text width) ────────────────
WORDMARK_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 66" width="160" height="26" aria-label="Rehearsal">
<defs>
<linearGradient id="rainbow-stripe" x1="0%" y1="0%" x2="100%" y2="0%">
<stop offset="0%" stop-color="#9677f8"/>
<stop offset="33%" stop-color="#4e44fd"/>
<stop offset="66%" stop-color="#ff4859"/>
<stop offset="100%" stop-color="#00c483"/>
</linearGradient>
</defs>
<text y="46" font-family="Raleway, Helvetica, Arial, sans-serif" fill="#0a0a0a" font-size="48" letter-spacing="-1">
<tspan font-weight="400">Re</tspan><tspan font-weight="200">hearsal</tspan>
</text>
<rect x="0" y="54" width="220" height="3" rx="1.5" fill="url(#rainbow-stripe)"/>
</svg>"""


# ── Canonical Editorial CSS (Rehearsal Brand) ─────────────────────────────
CSS = """
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,500;0,700;1,400&family=Source+Serif+Pro:ital,wght@0,400;0,600;1,400&family=Raleway:wght@400;500;600;700&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: "Source Serif Pro", Georgia, "Times New Roman", serif;
  font-size: 11pt; line-height: 1.65; color: #1a1a1a; background: #fff;
}
.page { max-width: 720px; margin: 0 auto; padding: 56px 60px; }

@page {
  size: A4;
  margin: 25mm 22mm 22mm 22mm;
  @bottom-right {
    content: counter(page);
    font-size: 8pt; color: #999; font-family: "Raleway", sans-serif;
  }
}
@media print { .page { max-width: 100%; padding: 0; } }

.brand-header { display: table; width: 100%; margin-bottom: 18px; }
.brand-wordmark, .brand-meta { display: table-cell; vertical-align: top; }
.brand-wordmark { line-height: 0; }
.brand-meta {
  text-align: right;
  font-family: "Raleway", sans-serif;
  font-size: 8.5pt; letter-spacing: 0.04em; color: #444; line-height: 1.55;
}
.brand-meta .case-number { font-weight: 600; color: #1a1a1a; }
.brand-meta .case-rev { color: #666; }
.header-rule { border-top: 1px solid #1a1a1a; margin: 0 0 24px 0; }

.tn-banner {
  background: #0a0a0a; color: #fff; text-align: center; padding: 14px 24px;
  font-family: "Raleway", sans-serif; font-size: 8.5pt;
  letter-spacing: 0.18em; font-weight: 500; text-transform: uppercase;
}
.tn-rainbow-stripe {
  height: 4px; margin: 0 0 36px 0;
  background: linear-gradient(90deg, #9677f8 0%, #4e44fd 33%, #ff4859 66%, #00c483 100%);
}

.author-byline {
  font-family: "Raleway", sans-serif; font-size: 9pt;
  letter-spacing: 0.18em; text-transform: uppercase;
  color: #555; font-weight: 600; margin-bottom: 16px;
}
h1.case-title {
  font-family: "Playfair Display", "Source Serif Pro", Georgia, serif;
  font-size: 28pt; font-weight: 700; line-height: 1.18;
  letter-spacing: -0.005em; color: #0a0a0a; margin-bottom: 10px;
}
h2.case-subtitle {
  font-family: "Source Serif Pro", Georgia, serif;
  font-size: 13pt; font-weight: 400; font-style: italic;
  color: #444; margin-bottom: 16px; line-height: 1.4;
}
.title-rule { border-top: 1px solid #ddd; margin: 18px 0 14px 0; }
.meta-row {
  font-family: "Raleway", sans-serif; font-size: 8.5pt;
  color: #555; padding: 4px 0; border-bottom: 1px solid #ddd; margin-bottom: 28px;
}
.meta-row span { margin-right: 28px; }
.meta-row strong { color: #1a1a1a; font-weight: 600; }

p { margin-bottom: 14px; text-align: justify; hyphens: auto; }

.lead {
  font-family: "Source Serif Pro", Georgia, serif;
  font-size: 11.5pt; font-style: italic; line-height: 1.7;
  color: #1a1a1a; margin-bottom: 26px;
}
.lead .dropcap {
  /* WeasyPrint-safe drop cap: inline span, not ::first-letter float.
     Earlier ::first-letter { float: left } crashed weasyprint/layout/float.py. */
  font-family: "Playfair Display", Georgia, serif;
  font-size: 28pt; font-style: normal; font-weight: 700;
  color: #0a0a0a; line-height: 0.9; vertical-align: -4pt;
  margin-right: 2px;
}

h3.section-head {
  font-family: "Playfair Display", "Source Serif Pro", Georgia, serif;
  font-size: 14pt; font-weight: 700; color: #0a0a0a;
  margin: 32px 0 14px; letter-spacing: -0.005em;
}
h4.sub-head {
  font-family: "Source Serif Pro", Georgia, serif;
  font-size: 11.5pt; font-weight: 600; font-style: italic;
  color: #1a1a1a; margin: 20px 0 8px;
}

blockquote {
  border-left: 2px solid #4e44fd; margin: 18px 0;
  padding: 4px 0 4px 18px; font-style: italic; color: #333; font-size: 11pt;
}

sup { font-size: 7.5pt; vertical-align: super; line-height: 0; }
sup a { text-decoration: none; color: #4e44fd; font-weight: 600; }
.footnotes {
  margin-top: 36px; padding-top: 14px;
  border-top: 1px solid #1a1a1a;
  font-size: 9pt; line-height: 1.55;
}
.footnotes ol { padding-left: 18px; }
.footnotes li { margin-bottom: 7px; color: #444; }
.footnotes h3 {
  font-family: "Playfair Display", Georgia, serif;
  font-size: 11.5pt; font-weight: 700; margin-bottom: 12px; color: #0a0a0a;
}

.exhibit { page-break-before: always; margin-top: 40px; }
.exhibit-label {
  font-family: "Raleway", sans-serif; font-size: 8pt; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.12em;
  color: #4e44fd; margin-bottom: 4px;
}

table {
  width: 100%; border-collapse: collapse; font-size: 9.5pt;
  margin-bottom: 12px; font-family: "Source Serif Pro", Georgia, serif;
}
th {
  background: #0a0a0a; color: #fff; padding: 8px 10px; text-align: left;
  font-size: 8.5pt; font-weight: 600; letter-spacing: 0.04em;
  text-transform: uppercase; font-family: "Raleway", sans-serif;
}
td { padding: 7px 10px; border-bottom: 1px solid #e5e5e5; vertical-align: top; }

hr { border: none; border-top: 1px solid #e5e5e5; margin: 24px 0; }

.case-footer {
  margin-top: 42px; padding-top: 14px; border-top: 1px solid #ddd;
  font-family: "Raleway", sans-serif; font-size: 8pt;
  color: #999; font-style: italic; text-align: center;
}
"""


def md_to_html(md):
    """Convert markdown to HTML. Footnote handling is paragraph-bounded (NOT greedy DOTALL)."""
    out = md

    # Paragraph-bounded footnote definition extraction (the v1.1.0 bug fix)
    footnotes = {}
    fn_def = re.compile(r'^\[\^(\d+)\]:\s*(.+?)(?=\n\n|\Z)', re.MULTILINE | re.DOTALL)
    for m in fn_def.finditer(out):
        body = re.sub(r'\s*\n\s*', ' ', m.group(2)).strip()
        footnotes[int(m.group(1))] = body
    out = fn_def.sub('', out)

    out = re.sub(r'\[\^(\d+)\]', lambda m: f'<sup><a href="#fn-{m.group(1)}" id="ref-{m.group(1)}">{m.group(1)}</a></sup>', out)

    # Headings
    out = re.sub(r'^# (.+)$', r'<h1 class="case-title">\1</h1>', out, flags=re.MULTILINE)
    out = re.sub(r'^## (.+)$', r'<h3 class="section-head">\1</h3>', out, flags=re.MULTILINE)
    out = re.sub(r'^### (.+)$', r'<h4 class="sub-head">\1</h4>', out, flags=re.MULTILINE)
    out = re.sub(r'^#### (.+)$', r'<h5>\1</h5>', out, flags=re.MULTILINE)

    # Inline formatting
    out = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', out)
    out = re.sub(r'(?<![*])\*([^*]+)\*(?![*])', r'<em>\1</em>', out)
    out = re.sub(r'`([^`]+)`', r'<code>\1</code>', out)

    # Tables
    def render_table(t):
        lines = [l.strip() for l in t.strip().split('\n') if l.strip()]
        if len(lines) < 2:
            return t
        header = [c.strip() for c in lines[0].strip('|').split('|')]
        rows = [[c.strip() for c in r.strip('|').split('|')] for r in lines[2:]]
        h = '<table><thead><tr>' + ''.join(f'<th>{c}</th>' for c in header) + '</tr></thead><tbody>'
        for r in rows:
            h += '<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>'
        h += '</tbody></table>'
        return h
    out = re.sub(r'(\|[^\n]+\|\n\|[-: |]+\|\n(?:\|[^\n]+\|\n?)+)', lambda m: render_table(m.group(1)), out, flags=re.MULTILINE)

    # Blockquotes
    out = re.sub(r'((?:^> [^\n]*\n)+)',
                 lambda m: '<blockquote>' + re.sub(r'^> ', '', m.group(1), flags=re.MULTILINE).strip() + '</blockquote>\n',
                 out, flags=re.MULTILINE)

    # Lists
    out = re.sub(r'((?:^\d+\. [^\n]*\n)+)',
                 lambda m: '<ol>' + ''.join(f'<li>{re.sub(r"^\d+\.\s*", "", l)}</li>' for l in m.group(1).strip().split('\n')) + '</ol>\n',
                 out, flags=re.MULTILINE)
    out = re.sub(r'((?:^- [^\n]*\n)+)',
                 lambda m: '<ul>' + ''.join(f'<li>{l[2:].strip()}</li>' for l in m.group(1).strip().split('\n') if l.startswith('- ')) + '</ul>\n',
                 out, flags=re.MULTILINE)

    # HRs
    out = re.sub(r'^---$', '<hr>', out, flags=re.MULTILINE)

    # Wrap remaining text in <p>
    paras = []
    for blk in out.split('\n\n'):
        blk = blk.strip()
        if not blk:
            continue
        if blk.startswith('<') and not blk.startswith(('<strong>', '<em>')):
            paras.append(blk)
        else:
            paras.append(f'<p>{blk}</p>')
    out = '\n\n'.join(paras)

    # Endnotes section
    if footnotes:
        fh = '<div class="footnotes"><h3>Notes</h3><ol>'
        for n in sorted(footnotes.keys()):
            fh += f'<li id="fn-{n}">{footnotes[n].strip()} <a href="#ref-{n}">↩</a></li>\n'
        fh += '</ol></div>'
        out += '\n\n' + fh
    return out


def parse_spec(spec_path):
    """Extract metadata from spec.md."""
    if not spec_path.exists():
        return {}
    text = spec_path.read_text()
    meta = {}
    # Slug from filename or spec
    m = re.search(r'\*\*Slug:\*\*\s*(\S+)', text)
    if m: meta['slug'] = m.group(1)
    # Case number
    m = re.search(r'(GBA|RHL)[\s-]?(\d{4}-\d{3})', text)
    if m: meta['case_number'] = f"{m.group(1)}-{m.group(2)}"
    # Title
    m = re.search(r'^# Case Spec:\s*(.+)$', text, re.MULTILINE)
    if m: meta['title'] = m.group(1).strip()
    # Difficulty
    m = re.search(r'\*\*Difficulty Level:\*\*\s*(\d)', text)
    if m: meta['difficulty'] = m.group(1)
    # Decision date
    m = re.search(r'\*\*Decision Date:\*\*\s*([^\n]+)', text)
    if m: meta['decision_date'] = m.group(1).strip()
    # Setting / Location
    m = re.search(r'\*\*Location:\*\*\s*([^\n]+)', text)
    if m: meta['setting'] = m.group(1).strip()
    return meta


def render_case(case_dir, meta, opening_pattern=None):
    """Render the case markdown into HTML + PDF."""
    md = (case_dir / "case.md").read_text()
    # Strip duplicate title block from markdown body (it's in the HTML wrapper)
    md = re.sub(r'^# .+\n\n\*\*[^\n]*\n.*?\n\n---\n\n', '', md, count=1, flags=re.DOTALL)

    # Wrap the lead paragraph with a drop cap span (WeasyPrint-safe approach)
    if opening_pattern:
        def wrap_lead(m):
            head = m.group(1)
            body = m.group(2)
            body = re.sub(r'^(\s*)(\w)', r'\1<span class="dropcap">\2</span>', body, count=1)
            return head + '<p class="lead">' + body + '</p>' + m.group(3)
        md = re.sub(opening_pattern, wrap_lead, md, count=1, flags=re.DOTALL)

    body = md_to_html(md)

    title = meta.get('title', 'Untitled Case')
    case_num = meta.get('case_number', 'RHL-XXXX-XXX')
    subtitle = meta.get('subtitle', '')
    decision_date = meta.get('decision_date', '')
    setting = meta.get('setting', '')
    difficulty = meta.get('difficulty', '?')
    discipline = meta.get('discipline', 'MBA')
    case_type = meta.get('case_type', 'Decision Case')
    rev_date = meta.get('rev_date', 'Current')
    word_count = meta.get('word_count', '~3,200 words + exhibits')
    author = meta.get('author', 'Dr. Shiva Kakkar')

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>{title} · {case_num}</title>
<style>{CSS}</style></head><body><div class="page">

<div class="brand-header">
<div class="brand-wordmark">{WORDMARK_SVG}</div>
<div class="brand-meta">
<div class="case-number">{case_num}</div>
<div class="case-rev">REV: {rev_date}</div>
<div>{discipline}</div>
<div>{case_type}</div>
</div></div>
<hr class="header-rule">

<div class="author-byline">{author}</div>
<h1 class="case-title">{title}</h1>
{f'<h2 class="case-subtitle">{subtitle}</h2>' if subtitle else ''}
<hr class="title-rule">
<div class="meta-row">
<span>Decision date: <strong>{decision_date}</strong></span>
<span>Setting: <strong>{setting}</strong></span>
<span>Difficulty: <strong>{difficulty} of 5</strong></span>
<span>Length: <strong>{word_count}</strong></span>
</div>

{body}

<div class="case-footer">
This case was developed for educational discussion. Outcomes are addressed only in the Teaching Note.
Published by Rehearsal &middot; By Gradeless AI.
</div>
</div></body></html>"""

    out_html = case_dir / f"{meta['slug']}-case.html"
    out_html.write_text(html)
    return out_html


def render_tn(case_dir, meta):
    """Render the teaching note markdown into HTML + PDF."""
    md = (case_dir / "teaching-note.md").read_text()
    md = re.sub(r'^# Teaching Note.*?\n\n', '', md, count=1, flags=re.DOTALL)
    body = md_to_html(md)

    title = meta.get('title', 'Untitled Case')
    case_num = meta.get('case_number', 'RHL-XXXX-XXX')
    subtitle = meta.get('subtitle', '')
    discipline = meta.get('discipline', 'MBA')
    rev_date = meta.get('rev_date', 'Current')
    session_length = meta.get('session_length', '75 minutes')
    author = meta.get('author', 'Dr. Shiva Kakkar')

    html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<title>Teaching Note · {title} · {case_num}</title>
<style>{CSS}</style></head><body><div class="page">

<div class="tn-banner">
Instructor Copy &nbsp;&middot;&nbsp; Confidential &nbsp;&middot;&nbsp; Not For Distribution To Students
</div>
<div class="tn-rainbow-stripe"></div>

<div class="brand-header">
<div class="brand-wordmark">{WORDMARK_SVG}</div>
<div class="brand-meta">
<div class="case-number">Teaching Note &nbsp;&middot;&nbsp; {case_num}</div>
<div class="case-rev">{rev_date}</div>
</div></div>
<hr class="header-rule">

<div class="author-byline">{author}</div>
<h1 class="case-title">{title}</h1>
{f'<h2 class="case-subtitle">{subtitle}</h2>' if subtitle else ''}
<hr class="title-rule">
<div class="meta-row">
<span>Session: <strong>{session_length}</strong></span>
<span>Level: <strong>{discipline}</strong></span>
<span>Last updated: <strong>{rev_date}</strong></span>
</div>

{body}

<div class="case-footer">
End of Teaching Note. The full Source Registry accompanies this packet.
Published by Rehearsal &middot; By Gradeless AI.
</div>
</div></body></html>"""

    out_html = case_dir / f"{meta['slug']}-teaching-note.html"
    out_html.write_text(html)
    return out_html


def generate_pdf(html_path):
    """Run weasyprint on the HTML."""
    pdf_path = html_path.with_suffix('.pdf')
    result = subprocess.run(
        ['weasyprint', str(html_path), str(pdf_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠ WeasyPrint warnings/errors:\n{result.stderr[:500]}")
    return pdf_path


def visual_inspect(pdf_path, expected_section_count=None):
    """Per known-corrections.md META-RULE: render PDF pages to PNG and verify section count.

    Returns dict with page count + section count + verdict.
    """
    preview_dir = pdf_path.parent / ".preview-pages"
    preview_dir.mkdir(exist_ok=True)
    # Clear old previews
    for f in preview_dir.glob(f"{pdf_path.stem}-*.png"):
        f.unlink()
    # Render pages to PNG
    subprocess.run(['pdftoppm', '-png', '-r', '110', str(pdf_path), str(preview_dir / pdf_path.stem)],
                   capture_output=True)
    # Count pages
    pdf_pages = len(list(preview_dir.glob(f"{pdf_path.stem}-*.png")))
    # Count section headers in the source HTML
    html_path = pdf_path.with_suffix('.html')
    html = html_path.read_text() if html_path.exists() else ''
    section_count = len(re.findall(r'<h3 class="section-head">', html))
    verdict = 'PASS' if section_count > 0 and (expected_section_count is None or section_count >= expected_section_count) else 'WARN'
    return {
        'pages': pdf_pages,
        'sections': section_count,
        'verdict': verdict,
    }


def cleanup_previews(case_dir):
    """Remove the .preview-pages/ directory after verification."""
    preview_dir = case_dir / ".preview-pages"
    if preview_dir.exists():
        shutil.rmtree(preview_dir)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    case_dir = Path(sys.argv[1]).resolve()
    if not case_dir.is_dir():
        print(f"ERROR: not a directory: {case_dir}")
        sys.exit(1)

    spec = case_dir / "spec.md"
    if not spec.exists():
        print(f"ERROR: missing spec.md in {case_dir}")
        sys.exit(1)

    meta = parse_spec(spec)
    if 'slug' not in meta:
        # Use directory name as slug
        meta['slug'] = case_dir.name

    # Allow overrides from CLI args (key=value)
    for arg in sys.argv[2:]:
        if '=' in arg:
            k, v = arg.split('=', 1)
            meta[k.strip()] = v.strip()

    print(f"=== Rendering {meta['slug']} ===")
    print(f"  Case directory: {case_dir}")
    print(f"  Title: {meta.get('title', '?')}")
    print(f"  Case number: {meta.get('case_number', '?')}")

    # Render case
    case_html = render_case(case_dir, meta)
    print(f"  ✓ Case HTML: {case_html.name}")
    case_pdf = generate_pdf(case_html)
    print(f"  ✓ Case PDF: {case_pdf.name}")

    # Render TN
    tn_html = render_tn(case_dir, meta)
    print(f"  ✓ TN HTML: {tn_html.name}")
    tn_pdf = generate_pdf(tn_html)
    print(f"  ✓ TN PDF: {tn_pdf.name}")

    # Visual inspection (per known-corrections.md META-RULE)
    print("\n=== Visual inspection (META-RULE) ===")
    case_check = visual_inspect(case_pdf)
    tn_check = visual_inspect(tn_pdf, expected_section_count=9)
    print(f"  Case: {case_check['pages']} pages, {case_check['sections']} sections — {case_check['verdict']}")
    print(f"  TN:   {tn_check['pages']} pages, {tn_check['sections']} sections — {tn_check['verdict']}")

    # Cleanup
    cleanup_previews(case_dir)
    print("\n✓ Render complete.")


if __name__ == "__main__":
    main()
