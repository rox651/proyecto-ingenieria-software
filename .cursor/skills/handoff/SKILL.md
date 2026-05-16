---
name: handoff
description: Compact context transfer between agent sessions. Use before starting a new Cursor chat after 2+ issues.
---

# Handoff Skill — VoiceLoop

When the user invokes **handoff** (or `/handoff`), produce an ultra-compact transfer summary.

## Output format

Write to `handoffs.md` (append new section with date) using this template:

```markdown
## Handoff — YYYY-MM-DD HH:MM

### Built
- bullet list of modules/files completed

### Architecture decisions
- consolidated choices (patterns, interfaces, env vars)

### Tests / CI
- what passes, known flakes

### Pending (exact)
- issue IDs still open and blocked_by status

### Next Ralph target
- recommended `./ralph/once.sh <ID>` and why
```

## Rules

- Max ~25 lines per handoff; no code dumps.
- Reference issue IDs (`#008`, `#003`).
- State which issues moved to `issues/done/`.
- Do not include secrets or `.env` values.
