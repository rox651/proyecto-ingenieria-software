---
title: Real-time dashboard updates via WebSocket
priority: feature
afk: true
---

# Issue 007 — Frontend en tiempo real

## Context

The dashboard polls REST endpoints. Users should see transcripts as they arrive.

## Acceptance criteria

- [ ] Add WebSocket endpoint `/ws/session` on FastAPI
- [ ] Push events: `state_change`, `transcript`, `response`
- [ ] Update `frontend/app.js` to subscribe and render live
- [ ] Fallback to polling if WebSocket unavailable
