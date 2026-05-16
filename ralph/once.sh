#!/usr/bin/env bash
# VoiceLoop — single Ralph iteration (Cursor HITL/AFK)
# Usage: ./ralph/once.sh [ISSUE_ID]
#   ./ralph/once.sh 008
#   ./ralph/once.sh      # lists open issues
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ISSUE_ID="${1:-}"

list_open_issues() {
  echo "Open issues (issues/*.md):"
  for f in issues/[0-9]*.md; do
    [[ -f "$f" ]] || continue
    id=$(basename "$f" .md | cut -d- -f1)
    title=$(grep -m1 '^title:' "$f" 2>/dev/null | sed 's/^title: *//' || basename "$f")
    blocked=$(grep -m1 '^blocked_by:' "$f" 2>/dev/null | sed 's/^blocked_by: *//' || echo "—")
    afk=$(grep -m1 '^afk:' "$f" 2>/dev/null | sed 's/^afk: *//' || echo "?")
    echo "  [$id] $title  (blocked_by: $blocked, afk: $afk)"
  done
  echo ""
  echo "Done issues: issues/done/"
}

if [[ -z "$ISSUE_ID" ]]; then
  echo "=== VoiceLoop Ralph — select an issue ==="
  echo ""
  list_open_issues
  echo "Recent commits:"
  git log --oneline -8 2>/dev/null || echo "(no git history)"
  echo ""
  echo "Run: ./ralph/once.sh <ID>   e.g. ./ralph/once.sh 008"
  exit 0
fi

# Normalize: 8 -> 008, 008 -> 008
ISSUE_NUM=$(printf '%03d' "$((10#$ISSUE_ID))")
ISSUE_FILE=$(find issues -maxdepth 1 -name "${ISSUE_NUM}-*.md" 2>/dev/null | head -1)

if [[ -z "$ISSUE_FILE" || ! -f "$ISSUE_FILE" ]]; then
  echo "ERROR: No issue file found for ID $ISSUE_ID (looked for ${ISSUE_NUM}-*.md)"
  list_open_issues
  exit 1
fi

# Check blocked_by dependencies
if grep -q '^blocked_by:' "$ISSUE_FILE"; then
  deps=$(grep '^blocked_by:' "$ISSUE_FILE" | sed 's/^blocked_by: *//')
  for dep in $deps; do
    dep_num=$(printf '%03d' "$((10#$dep))")
    if [[ -f "issues/${dep_num}-"*.md ]] 2>/dev/null; then
      echo "WARNING: Issue #$ISSUE_ID is blocked by #$dep (still open in issues/)"
    fi
  done
fi

echo "=== VoiceLoop Ralph Run — Issue #$ISSUE_ID ==="
echo "File: $ISSUE_FILE"
echo ""
cat "$ISSUE_FILE"
echo ""
echo "--- Recent commits ---"
git log --oneline -5 2>/dev/null || true
echo ""
echo "--- Agent instructions (ralph/prompt.md) ---"
cat ralph/prompt.md
echo ""
echo ">>> In Cursor Agent, say:"
echo "    Complete issue #$ISSUE_ID ($ISSUE_FILE). Use TDD. Commit as: feat(#$ISSUE_ID): <description>"
echo ""
echo ">>> After run: pytest -v && ruff check src tests"
