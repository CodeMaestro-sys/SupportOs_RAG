import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import app_db
import api


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_db, "APP_DB_PATH", tmp_path / "test_app.db")     # a fresh empty database per test
    with TestClient(api.app) as c:
        yield c


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_create_and_fetch_ticket(client):
    r = client.post("/tickets", json={"query": "I want to cancel my order ORD-12345"})
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "open" and body["ticket_id"] == 1
    assert client.get("/tickets/1").json()["query"] == "I want to cancel my order ORD-12345"


def test_missing_ticket_is_404(client):
    assert client.get("/tickets/999").status_code == 404


def test_too_short_query_is_rejected(client):
    assert client.post("/tickets", json={"query": "a"}).status_code == 422


def test_list_and_filter_by_status(client):
    client.post("/tickets", json={"query": "first question"})
    client.post("/tickets", json={"query": "second question"})
    assert len(client.get("/tickets").json()) == 2
    assert len(client.get("/tickets?status=open").json()) == 2
    assert client.get("/tickets?status=resolved").json() == []
    assert client.get("/tickets?status=nonsense").status_code == 400