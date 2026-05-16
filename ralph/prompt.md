# VoiceLoop Agent — Cursor AFK Prompt

You are an autonomous coding agent working on **VoiceLoop**, a minimal asyncio voice agent.

## Task selection

Read all markdown files in `issues/` (not `issues/done/`). Pick **exactly one** task per run.

Priority order:
1. **bugfix** — broken tests or runtime errors
2. **infrastructure** — tests, types, CI, dev tooling
3. **tracer-bullet** — end-to-end slice of a feature
4. **feature** — new capability
5. **polish** — UX, docs, refactors

Prefer issues tagged `afk: true` in the frontmatter. Skip issues tagged `hitl: true` unless the user is present.

## Workflow

1. Read the chosen issue completely.
2. Explore the codebase; read related modules and tests.
3. Implement using **test-driven development**: one failing test → minimal implementation → refactor.
4. Run feedback loops:
   - `pip install -e ".[dev]"` (first time)
   - `pytest`
   - `ruff check src tests`
5. Commit with a clear message describing *why*, not only *what*.
6. Move completed issues to `issues/done/` and add a short completion note at the bottom.
7. If incomplete, append a `## Progress` section to the issue with what remains.

## Rules

- Work on **one issue only** per run.
- Do not delete unrelated code or comments.
- Match existing style (protocols, stubs, async patterns).
- Never commit `.env` or secrets.
- Backend is Python (`src/voiceloop/`); frontend is `frontend/`.

## Project context

Pipeline: **Mic → STT → LLM → TTS → Speaker**

- `src/voiceloop/pipeline.py` — orchestrator
- `src/voiceloop/protocols.py` — interfaces
- `src/voiceloop/stubs.py` — dev stubs
- `src/voiceloop/api.py` — FastAPI control plane
- `frontend/` — dashboard
