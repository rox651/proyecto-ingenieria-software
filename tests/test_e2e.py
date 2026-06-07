"""End-to-end integration: API + pipeline stub mode."""

import pytest
from fastapi.testclient import TestClient

from voiceloop.api import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_e2e_health_to_turn_to_history(client):
    health = client.get("/health")
    assert health.status_code == 200

    status_before = client.get("/status").json()
    assert status_before["state"] in ("idle", "listening", "thinking", "speaking", "stopped")

    turn = client.post("/turn")
    assert turn.status_code == 200
    body = turn.json()
    assert "hola" in body["user_text"].lower()
    assert body["assistant_text"]

    history = client.get("/history").json()
    assert len(history) == 2
    assert history[0]["role"] == "user"
    assert history[1]["role"] == "assistant"

    status_after = client.get("/status").json()
    assert status_after["turns_completed"] == 1


def test_e2e_session_start_stop(client):
    start = client.post("/session/start", params={"max_turns": 1})
    assert start.status_code == 200
    stop = client.post("/session/stop")
    assert stop.status_code == 200
