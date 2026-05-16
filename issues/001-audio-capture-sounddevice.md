---
title: Implement real microphone capture with sounddevice
priority: feature
afk: true
---

# Issue 001 — Audio capture (micrófono)

## Context

The pipeline uses `StubAudioCapture` which returns silence. We need real PCM chunks from the system microphone.

## Acceptance criteria

- [ ] Create `src/voiceloop/audio/capture.py` implementing `AudioCapture`
- [ ] Use `sounddevice` with configurable `sample_rate` and `channels` from `Settings`
- [ ] `read_chunk()` is async-friendly (run blocking IO in executor if needed)
- [ ] Unit test mocks sounddevice; no mic required in CI
- [ ] Update `VoicePipeline` factory or CLI flag to select real vs stub capture

## Notes

- Chunk size ~100ms at 16 kHz mono is a reasonable default
- Handle missing device gracefully with clear error message
