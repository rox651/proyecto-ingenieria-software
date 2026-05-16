---
title: Streaming pipeline with asyncio queues
priority: tracer-bullet
afk: false
hitl: true
---

# Issue 006 — Pipeline en streaming

## Context

Current `run_turn()` buffers fixed chunks then processes. Real-time agents use queues between stages.

## Acceptance criteria

- [ ] Refactor pipeline to use `asyncio.Queue` between capture → STT → LLM → TTS → playback
- [ ] Background tasks per stage with cancellation on stop
- [ ] State transitions remain accurate (`LISTENING`, `THINKING`, `SPEAKING`)
- [ ] Existing tests updated or extended; no regression in `/turn` API

## HITL note

Requires manual testing with mic/speaker — run with user present.
