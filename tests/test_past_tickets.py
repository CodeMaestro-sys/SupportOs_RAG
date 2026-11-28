import importlib.util
import json
import sqlite3
import sys
import zlib
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from drafting import SYSTEM_D, draft
from past_tickets import PastTicketIndex, as_passages


class FakeModel:
    """Turns words into a small vector so that similar sentences get similar vectors."""
    def __init__(self):
        self.calls = 0

    def encode(self, texts, normalize_embeddings=True, batch_size=64, show_progress_bar=False):
        self.calls += 1
        single = isinstance(texts, str)
        out = []
        for t in ([texts] if single else texts):
            v = np.zeros(256)
            for w in t.lower().split():
                v[zlib.crc32(w.strip("?.,!").encode()) % 256] += 1       # deterministic, unlike hash()
            out.append(v / (np.linalg.norm(v) or 1))
        return out[0] if single else np.array(out)


@pytest.fixture()
def conn():
    c = sqlite3.connect(":memory:")
    c.row_factory = sqlite3.Row
    c.execute("CREATE TABLE tickets (ticket_id INTEGER, split TEXT, intent TEXT, query TEXT, response TEXT)")
    rows = [(1, "past", "cancel_order", "i want to cancel my order ORD-12345", "Open My Orders and click Cancel Order."),
            (2, "past", "track_order", "where is my parcel", "Open My Orders and click Track Order."),
            (3, "past", "get_refund", "how do i get my money back", "Open My Orders and click Return or Refund."),
            (4, "dev", "cancel_order", "cancel my order please", "dev reply"),
            (5, "abstain", "review", "can i write a review", "abstain reply")]
    c.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?)", rows)
    yield c
    c.close()


def test_most_similar_past_ticket_is_found_and_only_past_rows_are_indexed(conn, tmp_path):
    index = PastTicketIndex(conn, FakeModel(), cache_path=tmp_path / "emb.npz")
    assert len(index.rows) == 3                                   # dev and abstain tickets are never indexed
    hit = index.search("cancel my order", k=1)[0]
    assert hit["ticket_id"] == 1 and hit["intent"] == "cancel_order"


def test_a_ticket_can_be_excluded_from_its_own_results(conn, tmp_path):
    index = PastTicketIndex(conn, FakeModel(), cache_path=tmp_path / "emb.npz")
    ids = [m["ticket_id"] for m in index.search("i want to cancel my order", k=3, exclude_ticket_id=1)]
    assert 1 not in ids and len(ids) == 2


def test_embeddings_are_cached_on_disk(conn, tmp_path):
    path = tmp_path / "emb.npz"
    first = FakeModel()
    PastTicketIndex(conn, first, cache_path=path)
    assert first.calls == 1 and path.exists()
    second = FakeModel()
    index = PastTicketIndex(conn, second, cache_path=path)
    assert second.calls == 0                                      # loaded from the file, nothing re-encoded
    index.search("cancel", k=1)
    assert second.calls == 1                                      # only the query itself is encoded


def test_cache_is_rebuilt_when_the_data_changes(conn, tmp_path):
    path = tmp_path / "emb.npz"
    PastTicketIndex(conn, FakeModel(), cache_path=path)
    conn.execute("UPDATE tickets SET query = 'something completely different' WHERE ticket_id = 2")
    model = FakeModel()
    PastTicketIndex(conn, model, cache_path=path)
    assert model.calls == 1


def test_past_tickets_become_labelled_passages(conn, tmp_path):
    index = PastTicketIndex(conn, FakeModel(), cache_path=tmp_path / "emb.npz")
    passages = as_passages(index.search("cancel my order", k=1))
    doc_id, text, score = passages[0]
    assert doc_id == "past-ticket-1" and "Customer asked:" in text and "Agent replied:" in text and score > 0


class FakeRetriever:
    def search_chunks(self, query, k=4):
        return [("cancel-order", f"policy passage {i}", 0.8) for i in range(1, k + 1)]


class FakeLLM:
    model = "fake"

    def __init__(self, reply):
        self.reply, self.prompts = reply, []

    def generate(self, prompt, system=None):
        self.prompts.append((prompt, system))
        return self.reply


def test_draft_appends_extra_passages_after_the_policy_passages():
    llm = FakeLLM("You can cancel before dispatch [1]. Earlier customers did the same [5].")
    extra = [("past-ticket-9", "Earlier ticket. Customer asked: x Agent replied: y", 0.9)]
    out = draft(llm, FakeRetriever(), "cancel", floor=0.0, system=SYSTEM_D, extra_passages=extra)
    assert len(out["passages"]) == 5 and out["passages"][4][0] == "past-ticket-9"
    assert out["cited"] == [1, 5]
    assert "[5] (past-ticket-9)" in llm.prompts[0][0]


def test_draft_without_extra_passages_is_unchanged():
    out = draft(FakeLLM("Fine [1]."), FakeRetriever(), "cancel", floor=0.0)
    assert len(out["passages"]) == 4


def test_prompt_d_tells_the_model_to_prefer_policy_passages():
    assert "follow the policy passages" in SYSTEM_D and "past-ticket" in SYSTEM_D


def test_experiment_runs_end_to_end_with_fakes(conn, tmp_path):
    spec = importlib.util.spec_from_file_location("exp", ROOT / "scripts" / "past_tickets_experiment.py")
    exp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(exp)

    index = PastTicketIndex(conn, FakeModel(), cache_path=tmp_path / "emb.npz")

    class Drafter:
        model = "fake-drafter"

        def generate(self, prompt, system=None):
            if "past-ticket" in (system or "") and "[5]" in prompt:          # prompt D sees past tickets
                return "Hello! You can cancel before dispatch [1]. Earlier customers got a discount [5]."
            return "Hello! You can cancel before dispatch [1]."

    class Verifier:
        model = "fake-verifier"

        def generate(self, prompt, system=None):
            sentences = [l for l in prompt.split("Draft sentences:\n")[1].splitlines() if l.strip()]
            labels = []
            for i, line in enumerate(sentences, 1):
                lab = "not_factual" if "Hello" in line else ("unsupported" if "discount" in line else "supported")
                labels.append({"id": i, "label": lab, "passage": None})
            return json.dumps(labels)

    report, saved = exp.run_experiment(conn, index, FakeRetriever(), Drafter(), Verifier(), log=lambda *a, **k: None)
    dev = report["dev (answerable)"]
    assert dev["n"] == 1 and dev["C"] == {"answered": 1} and dev["D"] == {"answered": 1}
    assert dev["C_answered_with_a_sentence_not_in_the_policy"] == "0/1"
    assert dev["D_answered_with_a_sentence_not_in_the_policy"] == "1/1"      # the discount comes from a past ticket
    assert dev["D_answered_citing_a_past_ticket"] == "1/1"
    assert dev["top1_past_ticket_has_same_intent"] == "1/1"
    assert dev["examples_D_not_in_policy"][0]["sentence"].startswith("Earlier customers")