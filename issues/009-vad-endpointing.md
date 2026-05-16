---
title: Voice activity detection and turn endpointing
priority: feature
afk: false
hitl: true
blocked_by: 001
---

# Issue 009 — VAD y detección de fin de turno

## Context

Instead of fixed chunk counts, detect when the user stops speaking.

## Acceptance criteria

- [ ] Integrate simple energy-based VAD or `webrtcvad`
- [ ] End capture when silence exceeds threshold (e.g. 700ms)
- [ ] Configurable thresholds via settings
- [ ] Document tuning process in issue notes
