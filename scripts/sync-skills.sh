#!/usr/bin/env bash
# sync-skills.sh — fan out canonical /references/ and /assets/ into every skill folder.
#
# WHY THIS SCRIPT EXISTS
# ──────────────────────
# skillsovermcp.com (and the MCP skill resolver in general) scopes file paths
# inside a SKILL.md to the SKILL's own directory. So `references/anti-patterns.md`
# in `skills/research/SKILL.md` resolves to `skills/research/references/anti-patterns.md`,
# NOT `references/anti-patterns.md` at the repo root.
#
# But maintaining 14 protocol files × 8 skills = 112 hand-edited copies is insane.
# Solution: keep ONE canonical copy at the repo root (`/references/`, `/assets/`),
# then run this script before every push to refresh per-skill folders.
#
# USAGE
# ─────
#   ./scripts/sync-skills.sh            # sync everything, idempotent
#   ./scripts/sync-skills.sh --check    # dry run; non-zero exit if anything is stale
#
# The script reads each `skills/*/SKILL.md`, extracts every `references/*.md` and
# `assets/...` path it cites, and copies the matching files from the repo root into
# the skill's folder. Files NOT cited are not copied — keeps each skill minimal.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

CHECK_ONLY=0
[[ "${1:-}" == "--check" ]] && CHECK_ONLY=1

declare -i copied=0 skipped=0 stale=0

sync_one() {
  local src="$1" dst="$2"
  if [[ ! -f "$src" ]]; then
    echo "  ✗ MISSING source: $src (cited but not in repo root)" >&2
    return 1
  fi
  if [[ -f "$dst" ]] && cmp -s "$src" "$dst"; then
    skipped+=1
    return 0
  fi
  if (( CHECK_ONLY )); then
    echo "  STALE: $dst differs from $src"
    stale+=1
    return 0
  fi
  mkdir -p "$(dirname "$dst")"
  cp "$src" "$dst"
  echo "  ✓ $dst"
  copied+=1
}

for skill_dir in skills/*/; do
  skill="${skill_dir%/}"
  skill_md="$skill/SKILL.md"
  [[ -f "$skill_md" ]] || continue

  echo ""
  echo "── ${skill#skills/} ──"

  # Extract every `references/*.md` and `assets/<dir>/<file>` cited in the SKILL.md.
  # Strict rules:
  #   - Path must end in a real extension (.md, .html, .css, .py, .json, .txt) OR be a
  #     bare directory like `assets/templates/` (handled by the directory expansion below).
  #   - Reject placeholder filenames that look pathlike but are documentation examples
  #     (e.g. `references/X.md`, `assets/<path>`, `references/foo.bar.baz`).
  cited=$(grep -hoE '(references|assets)/[a-zA-Z0-9_-][a-zA-Z0-9._/-]*\.(md|html|css|py|json|txt)|(references|assets)/[a-zA-Z0-9_-]+/' "$skill_md" \
            | sed 's:/$::' \
            | sort -u \
            | grep -vE '/X\.[a-z]+$|/<[a-z]+>' || true)

  while IFS= read -r path; do
    [[ -z "$path" ]] && continue

    # If the path is a directory (e.g. "assets/templates"), expand it to all files inside.
    if [[ -d "$REPO_ROOT/$path" ]]; then
      while IFS= read -r f; do
        rel="${f#$REPO_ROOT/}"
        sync_one "$f" "$skill/$rel"
      done < <(find "$REPO_ROOT/$path" -type f)
    else
      sync_one "$REPO_ROOT/$path" "$skill/$path"
    fi
  done <<< "$cited"
done

echo ""
echo "────────────────────────"
if (( CHECK_ONLY )); then
  if (( stale > 0 )); then
    echo "FAIL: $stale file(s) stale. Run ./scripts/sync-skills.sh to fix." >&2
    exit 1
  fi
  echo "OK: all per-skill copies match canonical sources."
else
  echo "Synced. copied=$copied  unchanged=$skipped"
fi
