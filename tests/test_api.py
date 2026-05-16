import pytest
from fastapi.testclient import TestClient

from voiceloop.api import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_status(client):
    r = client.get("/status")
    assert r.status_code == 200
    data = r.json()
    assert "state" in data
    assert data["turns_completed"] >= 0


def test_single_turn(client):
    r = client.post("/turn")
    assert r.status_code == 200
    body = r.json()
    assert "user_text" in body
    assert "assistant_text" in body
