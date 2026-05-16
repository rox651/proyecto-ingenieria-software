#!/usr/bin/env bash
# Crea GitHub Issues desde los archivos en issues/
# Uso: ./scripts/create_github_issues.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if ! command -v gh &>/dev/null; then
  echo "Instala GitHub CLI: https://cli.github.com/"
  exit 1
fi

for f in issues/[0-9]*.md; do
  title=$(grep -m1 '^title:' "$f" | sed 's/^title: *//')
  echo "Creating: $title"
  gh issue create --title "$title" --body-file "$f"
  sleep 1
done

echo "Done. List issues: gh issue list"
