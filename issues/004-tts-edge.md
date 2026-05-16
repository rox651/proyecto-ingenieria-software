---
title: Text-to-Speech with edge-tts
priority: feature
afk: true
---

# Issue 004 — TTS con edge-tts

## Context

Replace `StubTextToSpeech` with real audio synthesis.

## Acceptance criteria

- [ ] Create `src/voiceloop/tts/edge.py` implementing `TextToSpeech`
- [ ] Return MP3 or PCM bytes suitable for playback module
- [ ] Spanish voice configurable via `TTS_VOICE` env var
- [ ] Tests mock edge-tts network calls
