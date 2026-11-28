"""The SupportOps pipeline: retrieve passages, draft a reply, verify it sentence by sentence.
No web code here, so it can be tested without a server."""
import os
import re
import threading

from drafting import SYSTEM_C, draft, outcome
from verification import strict_rule_flags, verify

PROMPT_VERSION = "C"

# Fixed boilerplate sentences are not checked: they state no policy fact (tested separately as 'not_factual').
EXEMPT_SENTENCES = [
    "Hello!",
    "Customer support can help with the rest.",
    "Customer support can help with the rest of your request.",
    "Let us know if you need help with anything else!",
]


def _norm(text):
    return re.sub(r"\s+", " ", text.strip().lower())


EXEMPT = {_norm(s) for s in EXEMPT_SENTENCES}


class Pipeline:
    def __init__(self, retriever, drafter, verifier, prompt=SYSTEM_C, prompt_version=PROMPT_VERSION, past_index=None):
        self.retriever = retriever
        self.past_index = past_index
        self.drafter = drafter
        self.verifier = verifier
        self.prompt = prompt
        self.prompt_version = prompt_version
        self._lock = threading.Lock()          # one request at a time: simple and safe for a single-user prototype

    @classmethod
    def from_env(cls):
        """Build the real pipeline (loads the embedding model and reads .env). Imports are local so that
        tests and the API module do not need the heavy libraries."""
        from dotenv import load_dotenv
        load_dotenv(override=True)
        from db import get_connection
        from llm import LLM
        from past_tickets import PastTicketIndex
        from retrieval import DenseChunks

        conn = get_connection()
        try:
            retriever = DenseChunks(conn)
            past_index = PastTicketIndex(conn, retriever.model)       # loads cached vectors, or builds them once
        finally:
            conn.close()
        drafter = LLM(min_interval=float(os.getenv("DRAFTER_MIN_INTERVAL", "4.5")))        # model from GEMINI_MODEL
        verifier = LLM(model=os.getenv("VERIFIER_MODEL", "gemini-3.1-flash-lite"),
                       min_interval=float(os.getenv("VERIFIER_MIN_INTERVAL", "4.5")))
        return cls(retriever, drafter, verifier, past_index=past_index)

    def similar(self, query, k=3):
        """Similar resolved tickets, shown to the agent for context. They are NOT given to the drafting model:
        the past-ticket experiment showed that doing so added sentences the policy does not support."""
        if self.past_index is None:
            return []
        with self._lock:
            matches = self.past_index.search(query, k=k)
        return [{"ticket_id": m["ticket_id"], "intent": m["intent"], "query": m["query"],
                 "response": m["response"], "score": round(float(m["score"]), 3)} for m in matches]

    def run(self, query):
        with self._lock:
            d = draft(self.drafter, self.retriever, query, floor=0.0, system=self.prompt)
            kind = outcome(d)
            sentences = []
            if kind == "answered":
                for item in verify(self.verifier, d, query):
                    label = item["llm_label"]
                    if _norm(item["sentence"]) in EXEMPT:
                        label = "not_factual"
                    sentences.append({"id": item["id"], "text": item["sentence"], "label": label,
                                      "rule_flags": strict_rule_flags(item["sentence"], d["passages"], query)})
        return {
            "outcome": kind,
            "reason": d["reason"],
            "draft_text": "" if kind == "refused" else d["draft"],
            "passages": [{"doc_id": doc, "text": text, "score": round(float(score), 3)}
                         for doc, text, score in d["passages"]],
            "sentences": sentences,
            "model": getattr(self.drafter, "model", ""),
            "verifier_model": getattr(self.verifier, "model", ""),
            "prompt_version": self.prompt_version,
        }