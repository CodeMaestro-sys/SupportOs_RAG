import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from pipeline import Pipeline
from verification import split_sentences, strict_rule_flags

PASSAGES = [("cancel-order", "You can cancel an order at any time before it is dispatched. Refunds take 5 to 7 business days.", 0.8),
            ("contact-support", "Call +91 00000 00000 or write to support@shopease.example.", 0.7)]


class FakeRetriever:
    def search_chunks(self, query, k=4):
        return PASSAGES


class FakeLLM:
    def __init__(self, text=None, labels=None):
        self.text, self.labels, self.calls, self.model = text, labels, 0, "fake"

    def generate(self, prompt, system=None):
        self.calls += 1
        if self.labels is not None:                                     # acting as the verifier
            return json.dumps([{"id": i, "label": lab, "passage": None} for i, lab in enumerate(self.labels, 1)])
        return self.text                                                # acting as the drafter


def make(draft_text, labels=None):
    drafter, verifier = FakeLLM(text=draft_text), FakeLLM(labels=labels or [])
    return Pipeline(FakeRetriever(), drafter, verifier), drafter, verifier


def test_answered_draft_is_verified_and_boilerplate_is_exempt():
    text = "Hello! You can cancel an order before it is dispatched [1]. Customer support can help with the rest."
    pipe, _, verifier = make(text, labels=["not_factual", "supported", "unsupported"])   # verifier wrongly flags the 3rd
    out = pipe.run("I want to cancel")
    assert out["outcome"] == "answered"
    labels = [s["label"] for s in out["sentences"]]
    assert labels == ["not_factual", "supported", "not_factual"]        # the hand-off sentence is exempt
    assert verifier.calls == 1


def test_number_missing_from_passages_is_flagged_by_the_rule_check():
    text = "Refunds take 9 business days [1]."
    pipe, _, _ = make(text, labels=["supported"])
    out = pipe.run("how long do refunds take")
    assert out["sentences"][0]["rule_flags"] == ["9"]


def test_refusal_skips_verification():
    pipe, _, verifier = make("NOT_ENOUGH_EVIDENCE", labels=["supported"])
    out = pipe.run("what is the cancellation fee")
    assert out["outcome"] == "refused" and out["draft_text"] == "" and out["sentences"] == []
    assert out["reason"] == "model_judgement"
    assert verifier.calls == 0


def test_clarifying_question_is_kept_and_not_verified():
    pipe, _, verifier = make("Do you want to change the delivery address or the invoice address?")
    out = pipe.run("correcting the address")
    assert out["outcome"] == "clarify" and "?" in out["draft_text"]
    assert verifier.calls == 0


def test_passages_are_returned_with_scores():
    pipe, _, _ = make("NOT_ENOUGH_EVIDENCE")
    out = pipe.run("anything")
    assert out["passages"][0] == {"doc_id": "cancel-order", "text": PASSAGES[0][1], "score": 0.8}


def test_whole_number_matching_in_rule_check():
    passages = [("p", "Support hours are 9 AM to 6 PM. The limit is 12 PM.", 0.5)]
    assert strict_rule_flags("Changes take 2 days.", passages, "") == ["2"]          # '2' is not inside '12'
    assert strict_rule_flags("Hours are 9 AM to 6 PM.", passages, "") == []


def test_sentence_splitting_keeps_citations():
    assert split_sentences("Hello! You can cancel [2]. Done.") == ["Hello!", "You can cancel [2].", "Done."]


def test_similar_tickets_come_from_the_past_ticket_index_and_are_rounded():
    class FakeIndex:
        def search(self, query, k=3):
            return [{"ticket_id": 4, "intent": "cancel_order", "query": "cancel", "response": "reply", "score": 0.912345}][:k]
    pipe = Pipeline(FakeRetriever(), FakeLLM(text="x"), FakeLLM(labels=[]), past_index=FakeIndex())
    out = pipe.similar("cancel my order", k=1)
    assert out == [{"ticket_id": 4, "intent": "cancel_order", "query": "cancel", "response": "reply", "score": 0.912}]


def test_similar_tickets_without_an_index_is_an_empty_list():
    pipe, _, _ = make("x")
    assert pipe.similar("anything") == []