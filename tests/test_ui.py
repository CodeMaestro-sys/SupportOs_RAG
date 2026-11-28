"""Tests for the Streamlit screen. They use Streamlit's headless AppTest and a fake API, so no server,
model or quota is needed."""
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ui"))
pytest.importorskip("streamlit")
from streamlit.testing.v1 import AppTest

import api_client

APP = str(ROOT / "ui" / "streamlit_app.py")

SUPPORTED = {"id": 1, "text": "You can cancel an order before it is dispatched [1].", "label": "supported", "rule_flags": []}
UNSUPPORTED = {"id": 2, "text": "You also get a 10% discount [1].", "label": "unsupported", "rule_flags": ["10"]}


def make_draft(sentences, outcome="answered", text="Draft text [1]."):
    return {"draft_id": 1, "ticket_id": 1, "created_at": "now", "outcome": outcome, "reason": "",
            "draft_text": text, "reply_text": text.replace(" [1]", ""), "passages": [{"doc_id": "cancel-order", "text": "Evidence text", "score": 0.8}],
            "sentences": sentences, "model": "m1", "verifier_model": "m2", "prompt_version": "C"}


class FakeBackend:
    def __init__(self, tickets=None, draft=None, status="open"):
        self.tickets = tickets if tickets is not None else [
            {"ticket_id": 1, "query": "cancel my order", "status": status, "created_at": "now"}]
        self.draft, self.resolutions, self.resolve_calls, self.created = draft, {}, [], []
        self.similar = [{"ticket_id": 7, "intent": "cancel_order", "query": "cancel my order",
                         "response": "Open My Orders and click Cancel Order.", "score": 0.91}]

    def install(self, monkeypatch):
        monkeypatch.setattr(api_client, "list_tickets", lambda status=None: [t for t in self.tickets if not status or t["status"] == status])
        monkeypatch.setattr(api_client, "latest_draft", lambda tid: self.draft)
        monkeypatch.setattr(api_client, "get_resolution", lambda tid: self.resolutions.get(tid))
        monkeypatch.setattr(api_client, "create_draft", self.create_draft)
        monkeypatch.setattr(api_client, "create_ticket", self.create_ticket)
        monkeypatch.setattr(api_client, "resolve", self.resolve)
        monkeypatch.setattr(api_client, "similar_tickets", lambda tid, k=3: self.similar)

    def create_draft(self, tid):
        self.draft = make_draft([SUPPORTED])
        self.tickets[0]["status"] = "in_review"
        return self.draft

    def create_ticket(self, query):
        t = {"ticket_id": len(self.tickets) + 1, "query": query, "status": "open", "created_at": "now"}
        self.tickets.append(t)
        self.created.append(query)
        return t

    def resolve(self, tid, action, final_text=None, draft_id=None):
        self.resolve_calls.append((tid, action, final_text))
        self.resolutions[tid] = {"agent_action": action, "final_text": final_text, "similarity": 1.0}
        for t in self.tickets:
            if t["ticket_id"] == tid:
                t["status"] = "resolved"


def button(at, label):
    matches = [b for b in at.button if b.label == label]
    assert matches, f"no button labelled {label!r}; found {[b.label for b in at.button]}"
    return matches[0]


def test_empty_queue_shows_a_hint(monkeypatch):
    FakeBackend(tickets=[]).install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert any("No tickets" in i.value for i in at.info)


def test_generate_draft_then_show_it(monkeypatch):
    backend = FakeBackend()
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    button(at, "Generate draft").click().run()
    assert not at.exception
    assert any("Every factual sentence" in s.value for s in at.success)
    assert any("Send as drafted" == b.label for b in at.button)


def test_unsupported_sentence_blocks_sending_until_checked(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED, UNSUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert any("not supported" in e.value for e in at.error)
    assert button(at, "Send as drafted").disabled
    at.checkbox(key="confirm_1").check().run()
    send = button(at, "Send as drafted")
    assert not send.disabled
    send.click().run()
    assert backend.resolve_calls == [(1, "accepted", "Draft text.")]
    assert any("Resolved" in s.value for s in at.success)


def test_changed_text_is_sent_as_edited(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    at.text_area(key="reply_1").set_value("My own improved wording.").run()
    button(at, "Send edited reply").click().run()
    assert backend.resolve_calls == [(1, "edited", "My own improved wording.")]


def test_discarding_the_draft_sends_own_reply(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    at.text_area(key="reply_1").set_value("Completely different answer.").run()
    at.checkbox(key="discard_1").check().run()
    button(at, "Send my own reply").click().run()
    assert backend.resolve_calls[0][1] == "rejected"


def test_refused_draft_needs_the_agents_own_text(monkeypatch):
    backend = FakeBackend(draft=make_draft([], outcome="refused", text=""), status="in_review")
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert any("does not cover" in w.value for w in at.warning)
    assert button(at, "Send my own reply").disabled
    at.text_area(key="reply_1").set_value("Please contact our team.").run()
    button(at, "Send my own reply").click().run()
    assert backend.resolve_calls == [(1, "rejected", "Please contact our team.")]


def test_creating_a_ticket_from_the_sidebar(monkeypatch):
    backend = FakeBackend()
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    at.text_area[0].set_value("Where is my parcel?")
    button(at, "Create ticket").click().run()
    assert not at.exception
    assert backend.created == ["Where is my parcel?"]


def test_api_down_shows_an_error_instead_of_crashing(monkeypatch):
    def down(status=None):
        raise api_client.ApiError(0, "Cannot reach the API")
    monkeypatch.setattr(api_client, "list_tickets", down)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert any("Cannot reach" in e.value for e in at.error)


def test_similar_tickets_are_shown_for_context(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert any("Similar resolved tickets" in m.value for m in at.markdown)
    assert any("not from these replies" in c.value for c in at.caption)


def test_failure_of_the_similar_search_does_not_block_the_agent(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    def broken(tid, k=3):
        raise api_client.ApiError(502, "search failed")
    monkeypatch.setattr(api_client, "similar_tickets", broken)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert any("Send as drafted" == b.label for b in at.button)


def test_reply_box_is_drawn_even_when_similar_tickets_fail(monkeypatch):
    backend = FakeBackend(draft=make_draft([SUPPORTED]), status="in_review")
    backend.install(monkeypatch)
    def down(tid, k=3):
        raise api_client.ApiError(0, "timed out")
    monkeypatch.setattr(api_client, "similar_tickets", down)
    at = AppTest.from_file(APP, default_timeout=15).run()
    assert not at.exception
    assert at.text_area(key="reply_1").value                      # the reply box exists and is filled
    assert any("not available right now" in c.value for c in at.caption)