---
name: improve-codebase-architecture
description: Mid-sprint structural review. Use after 2-3 completed issues before resuming Ralph loops.
---

# Improve Codebase Architecture — VoiceLoop

Invoke after **2–3 successful Ralph issues**. Goal: deepen shallow modules before debt compounds.

## Phase 1 — Diagnosis

Explore `src/voiceloop/` and report:

1. Shallow modules (thin wrappers, logic in wrong layer)
2. Scattered logic (same concern in 3+ files)
3. Cyclic or confusing imports
4. Coupling risks for upcoming issues (check `blocked_by` in `issues/`)

Output a **numbered list** of deepening opportunities (max 5).

## Phase 2 — Parallel proposals (simulate 3 sub-agents)

For the **team-chosen module**, document three radically different interface designs:

| Agent | Style | Focus |
|-------|-------|-------|
| A | Minimal factory | `create_pipeline(mode)` |
| B | Builder | `PipelineBuilder().with_stt(...).build()` |
| C | Registry/DI | named providers in a container |

Each proposal: public API sketch, pros, cons, fit for VoiceLoop.

## Phase 3 — Hybrid recommendation

Recommend one hybrid approach with technical justification. Implement it; keep `pytest` and `ruff` green.

## Phase 4 — Record

Append findings to `architecture-checkpoint.md` at repo root (do not overwrite prior checkpoints).
