"""Past resolved tickets as a second source of evidence: find earlier tickets whose question is similar."""
import hashlib
import re
from pathlib import Path

import numpy as np

ID = re.compile(r"\b(?:ord|inv|trk|ref)-?\d+\b|#\s?\d+|\b\d{4,}\b", re.I)     # same number-stripping as retrieval.py
CACHE = Path("data/past_tickets_emb.npz")


def _clean(text):
    return ID.sub(" ", text)


class PastTicketIndex:
    """Embeds the questions of all tickets with split = 'past' (once; the vectors are cached on disk)."""

    def __init__(self, conn, model, cache_path=CACHE, batch_size=64):
        rows = conn.execute("SELECT ticket_id, intent, query, response FROM tickets "
                            "WHERE split = 'past' ORDER BY ticket_id").fetchall()
        self.rows = [dict(r) for r in rows]
        self.ids = np.array([r["ticket_id"] for r in self.rows])
        self.model = model
        self.emb = self._load_or_build(Path(cache_path), batch_size)

    def _digest(self):
        return hashlib.md5("\x1f".join(r["query"] for r in self.rows).encode("utf-8")).hexdigest()

    def _load_or_build(self, cache_path, batch_size):
        digest = self._digest()
        if cache_path.exists():
            data = np.load(cache_path, allow_pickle=False)
            if np.array_equal(data["ids"], self.ids) and str(data["digest"]) == digest:
                return data["emb"]
        emb = self.model.encode([_clean(r["query"]) for r in self.rows], normalize_embeddings=True,
                                batch_size=batch_size, show_progress_bar=True)
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        np.savez(cache_path, ids=self.ids, emb=emb, digest=digest)
        return emb

    def search(self, query, k=2, exclude_ticket_id=None):
        """The k past tickets whose question is most similar. A ticket never matches itself when excluded."""
        scores = self.emb @ self.model.encode(_clean(query), normalize_embeddings=True)
        found = []
        for i in np.argsort(-scores):
            if exclude_ticket_id is not None and self.rows[i]["ticket_id"] == exclude_ticket_id:
                continue
            found.append({**self.rows[i], "score": float(scores[i])})
            if len(found) == k:
                break
        return found


def as_passages(matches):
    """Format past tickets as evidence passages: (doc_id, text, score), like the policy passages."""
    return [(f"past-ticket-{m['ticket_id']}",
             f"Earlier ticket. Customer asked: {m['query']} Agent replied: {m['response']}", m["score"])
            for m in matches]