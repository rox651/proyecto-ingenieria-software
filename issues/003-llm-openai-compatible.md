---
title: OpenAI-compatible LLM client for conversation
priority: feature
afk: true
---

# Issue 003 — LLM conversacional

## Context

Replace `StubLanguageModel` with an HTTP client to an OpenAI-compatible API.

## Acceptance criteria

- [ ] Create `src/voiceloop/llm/openai_client.py` implementing `LanguageModel`
- [ ] Use `httpx.AsyncClient` and settings from `config.py`
- [ ] Pass full `history` to the API as messages
- [ ] System prompt defines a concise Spanish voice assistant persona
- [ ] Test with mocked HTTP responses (no real API key in CI)
