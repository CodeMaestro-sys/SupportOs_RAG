import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import api
import app_db

CANNED = {
    "outcome": "answered",
    "reason": "",
    "draft_text": "You can cancel an order before it is dispatched [1]. Customer support can help with the rest.",
    "passages": [{"doc_id": "cancel-order", "text": "You can cancel an order at any time before it is dispatched.", "score": 0.81}],
    "sentences": [
        {"id": 1, "text": "You can cancel an order before it is dispatched [1].", "label": "supported", "rule_flags": []},
        {"id": 2, "text": "Customer support can help with the rest.", "label": "not_factual", "rule_flags": []},
    ],
    "model": "fake-drafter",
    "verifier_model": "fake-verifier",
    "prompt_version": "C",
}


class FakePipeline:
    def __init__(self, result=None, error=None):
        self.result, self.error, self.calls = result or CANNED, error, 0

    def run(self, query):
        self.calls += 1
        if self.error:
            raise self.error
        return self.result


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_db, "APP_DB_PATH", tmp_path / "test_app.db")     # a fresh empty database per test
    with TestClient(api.app) as c:
        yield c
    api.app.dependency_overrides.clear()


def use_pipeline(pipeline):
    api.app.dependency_overrides[api.get_pipeline] = lambda: pipeline


def new_ticket(client, text="I want to cancel my order ORD-12345"):
    return client.post("/tickets", json={"query": text}).json()["ticket_id"]


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


def test_draft_is_stored_and_ticket_moves_to_review(client):
    pipeline = FakePipeline()
    use_pipeline(pipeline)
    tid = new_ticket(client)
    r = client.post(f"/tickets/{tid}/draft")
    assert r.status_code == 201
    body = r.json()
    assert body["outcome"] == "answered" and body["draft_id"] == 1
    assert body["sentences"][0]["label"] == "supported"
    assert body["passages"][0]["doc_id"] == "cancel-order"
    assert client.get(f"/tickets/{tid}").json()["status"] == "in_review"
    assert pipeline.calls == 1


def test_latest_draft_returns_the_newest(client):
    use_pipeline(FakePipeline())
    tid = new_ticket(client)
    client.post(f"/tickets/{tid}/draft")
    client.post(f"/tickets/{tid}/draft")
    latest = client.get(f"/tickets/{tid}/draft").json()
    assert latest["draft_id"] == 2


def test_latest_draft_before_any_draft_is_404(client):
    tid = new_ticket(client)
    assert client.get(f"/tickets/{tid}/draft").status_code == 404


def test_draft_for_missing_ticket_is_404(client):
    use_pipeline(FakePipeline())
    assert client.post("/tickets/999/draft").status_code == 404


def test_draft_for_resolved_ticket_is_409(client):
    use_pipeline(FakePipeline())
    tid = new_ticket(client)
    conn = app_db.get_app_connection()
    conn.execute("UPDATE support_tickets SET status = 'resolved' WHERE ticket_id = ?", (tid,))
    conn.commit()
    conn.close()
    assert client.post(f"/tickets/{tid}/draft").status_code == 409


def test_pipeline_failure_gives_502_and_leaves_ticket_open(client):
    use_pipeline(FakePipeline(error=RuntimeError("model overloaded")))
    tid = new_ticket(client)
    r = client.post(f"/tickets/{tid}/draft")
    assert r.status_code == 502
    assert "model overloaded" not in r.text            # internal details are not leaked
    assert client.get(f"/tickets/{tid}").json()["status"] == "open"
    assert client.get(f"/tickets/{tid}/draft").status_code == 404


# ---------------------------------------------------------------- resolving a ticket
def drafted_ticket(client):
    use_pipeline(FakePipeline())
    tid = new_ticket(client)
    client.post(f"/tickets/{tid}/draft")
    return tid


def test_accepting_a_draft_resolves_the_ticket(client):
    tid = drafted_ticket(client)
    r = client.post(f"/tickets/{tid}/resolve", json={"action": "accepted"})
    assert r.status_code == 201
    body = r.json()
    assert body["agent_action"] == "accepted" and body["similarity"] == 1.0
    assert body["final_text"] == CANNED["draft_text"] and body["draft_id"] == 1
    assert client.get(f"/tickets/{tid}").json()["status"] == "resolved"
    assert client.get(f"/tickets/{tid}/resolution").json()["resolution_id"] == body["resolution_id"]


def test_editing_a_draft_records_how_much_changed(client):
    tid = drafted_ticket(client)
    edited = "You can cancel your order before dispatch. Please quote your order number."
    r = client.post(f"/tickets/{tid}/resolve", json={"action": "edited", "final_text": edited})
    assert r.status_code == 201
    assert r.json()["final_text"] == edited and 0 < r.json()["similarity"] < 1


def test_edit_with_unchanged_text_is_rejected(client):
    tid = drafted_ticket(client)
    r = client.post(f"/tickets/{tid}/resolve", json={"action": "edited", "final_text": CANNED["draft_text"]})
    assert r.status_code == 422


def test_rejecting_needs_the_agents_own_reply(client):
    tid = drafted_ticket(client)
    assert client.post(f"/tickets/{tid}/resolve", json={"action": "rejected"}).status_code == 422
    r = client.post(f"/tickets/{tid}/resolve", json={"action": "rejected", "final_text": "Please call us."})
    assert r.status_code == 201 and r.json()["agent_action"] == "rejected"


def test_accepting_without_a_draft_is_rejected(client):
    tid = new_ticket(client)
    assert client.post(f"/tickets/{tid}/resolve", json={"action": "accepted"}).status_code == 422


def test_agent_can_answer_a_ticket_that_has_no_draft(client):
    tid = new_ticket(client)
    r = client.post(f"/tickets/{tid}/resolve", json={"action": "rejected", "final_text": "Here is your answer."})
    assert r.status_code == 201 and r.json()["draft_id"] is None and r.json()["similarity"] is None


def test_resolving_twice_is_409_and_unknown_values_are_422(client):
    tid = drafted_ticket(client)
    assert client.post(f"/tickets/{tid}/resolve", json={"action": "accepted"}).status_code == 201
    assert client.post(f"/tickets/{tid}/resolve", json={"action": "accepted"}).status_code == 409
    other = new_ticket(client, "another question")
    assert client.post(f"/tickets/{other}/resolve", json={"action": "approved"}).status_code == 422


def test_draft_of_another_ticket_is_404(client):
    t1 = drafted_ticket(client)
    t2 = new_ticket(client, "second ticket")
    r = client.post(f"/tickets/{t2}/resolve", json={"action": "accepted", "draft_id": 1})
    assert r.status_code == 404 and t1 != t2


def test_resolution_before_resolving_is_404(client):
    tid = new_ticket(client)
    assert client.get(f"/tickets/{tid}/resolution").status_code == 404


def test_migration_adds_missing_column(tmp_path):
    import sqlite3
    path = tmp_path / "old.db"
    old = sqlite3.connect(path)
    old.execute("CREATE TABLE resolutions (resolution_id INTEGER PRIMARY KEY, ticket_id INTEGER, draft_id INTEGER, "
                "agent_action TEXT, final_text TEXT, resolved_at TEXT)")
    old.commit(); old.close()
    conn = app_db.get_app_connection(path)
    app_db.init_app_db(conn)
    assert "similarity" in {row["name"] for row in conn.execute("PRAGMA table_info(resolutions)")}
    conn.close()