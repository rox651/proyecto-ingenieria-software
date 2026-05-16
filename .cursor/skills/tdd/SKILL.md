---
name: tdd
description: Test-driven development for VoiceLoop. Use when implementing features in this repo.
---

# TDD Skill — VoiceLoop

## Process

1. Read the issue acceptance criteria.
2. Write **one** failing test that describes the next behavior.
3. Run `pytest` — confirm failure for the right reason.
4. Write the **minimal** code to pass.
5. Refactor if needed; keep tests green.
6. Repeat until the issue is done.

## Guidelines

- Prefer **vertical slices** (one test → one implementation) over writing all tests first.
- Mock external I/O (mic, APIs) in unit tests; use stubs in `voiceloop.stubs`.
- Async tests use `pytest.mark.asyncio`.
- API tests use `fastapi.testclient.TestClient`.

## Commands

```bash
pip install -e ".[dev]"
pytest -v
ruff check src tests
```
