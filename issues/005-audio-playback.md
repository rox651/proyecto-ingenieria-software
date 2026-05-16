---
title: Speaker playback for synthesized audio
priority: feature
afk: true
---

# Issue 005 — Audio playback (altavoz)

## Context

Play TTS output through the system speaker.

## Acceptance criteria

- [ ] Create `src/voiceloop/audio/playback.py` implementing `AudioPlayback`
- [ ] Support MP3 input (decode if needed) via sounddevice or simpleaudio
- [ ] Async `play()` blocks until playback completes
- [ ] Tests verify play was invoked without requiring hardware
