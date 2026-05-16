#!/usr/bin/env bash
# VoiceLoop — single agent iteration (HITL with Cursor)
# Adapted from https://www.aihero.dev/running-your-afk-agent-a9l1u
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== VoiceLoop Agent Run ==="
echo ""
echo "Open issues:"
find issues -maxdepth 1 -name '*.md' ! -path 'issues/done/*' 2>/dev/null | sort || true
echo ""
echo "Recent commits:"
git log --oneline -5 2>/dev/null || echo "(no git history yet)"
echo ""
echo "--- Agent instructions (ralph/prompt.md) ---"
cat ralph/prompt.md
echo ""
echo "---"
echo "In Cursor: open Agent mode, paste the prompt above, and say:"
echo '  "Pick the highest-priority AFK issue in issues/ and complete one task."'
echo ""
echo "After the run: pytest && ruff check src tests"
