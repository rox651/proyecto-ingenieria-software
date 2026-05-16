---
title: Integrate faster-whisper for Speech-to-Text
priority: feature
afk: true
---

# Issue 002 — STT con faster-whisper

## Context

Replace `StubSpeechToText` with local transcription using `faster-whisper`.

## Acceptance criteria

- [ ] Create `src/voiceloop/stt/whisper.py` implementing `SpeechToText`
- [ ] Load model once (lazy singleton) to avoid reload per turn
- [ ] `transcribe(audio_chunk)` returns text; empty string on silence
- [ ] Config: model size via env var `WHISPER_MODEL` (default `tiny`)
- [ ] Tests use a small fixture WAV or mock the model

## References

- https://github.com/SYSTRAN/faster-whisper
