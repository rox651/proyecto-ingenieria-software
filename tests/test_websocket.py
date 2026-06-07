import pytest
from fastapi.testclient import TestClient

from voiceloop.api import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_websocket_receives_turn_events(client):
    with client.websocket_connect("/ws/session") as ws:
        initial = ws.receive_json()
        assert initial["event"] == "state_change"

        client.post("/turn")
        events = []
        for _ in range(6):
            msg = ws.receive_json()
            events.append(msg["event"])

        assert "state_change" in events
        assert "transcript" in events
        assert "response" in events
