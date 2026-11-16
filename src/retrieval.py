import re
from nltk.stem import PorterStemmer
from rank_bm25 import BM25Okapi

TOKEN = re.compile(r"[a-z0-9]+")
ID = re.compile(r"\b(?:ord|inv|trk|ref)-?\d+\b|#\s?\d+|\b\d{4,}\b", re.I)
STOP = {"i", "me", "my", "a", "an", "the", "to", "of", "in", "on", "for", "and", "or", "is",
        "it", "be", "can", "could", "would", "do", "does", "how", "what", "want", "need",
        "help", "please", "you", "your", "we", "our", "with", "that", "this", "if", "are", "am"}
_stem = PorterStemmer().stem


def tokenize_raw(text):
    return TOKEN.findall(text.lower())


def tokenize_clean(text):
    words = TOKEN.findall(ID.sub(" ", text.lower()))      # drop order/invoice/tracking numbers
    return [_stem(w) for w in words if len(w) > 1 and w not in STOP]


class BM25Docs:
    """Keyword search over the policy documents."""

    def __init__(self, conn, tokenize=tokenize_clean):
        self.tokenize = tokenize
        rows = conn.execute("SELECT doc_id, title, body FROM documents ORDER BY doc_id").fetchall()
        self.doc_ids = [r["doc_id"] for r in rows]
        self.bm25 = BM25Okapi([tokenize(r["title"] + " " + r["body"]) for r in rows])

    def search(self, query, k=5):
        scores = self.bm25.get_scores(self.tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [(self.doc_ids[i], float(scores[i])) for i in order]
import numpy as np
from sentence_transformers import SentenceTransformer

QUERY_PREFIX = "Represent this sentence for searching relevant passages: "


class DenseDocs:
    """Meaning-based search: documents and queries become vectors."""

    def __init__(self, conn, model_name="BAAI/bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_name)
        rows = conn.execute("SELECT doc_id, title, body FROM documents ORDER BY doc_id").fetchall()
        self.doc_ids = [r["doc_id"] for r in rows]
        self.emb = self.model.encode([r["title"] + ". " + r["body"] for r in rows],
                                     normalize_embeddings=True)

    def search(self, query, k=5):
        q = QUERY_PREFIX + ID.sub(" ", query)              # same number-stripping as BM25
        scores = self.emb @ self.model.encode(q, normalize_embeddings=True)
        order = np.argsort(-scores)[:k]
        return [(self.doc_ids[i], float(scores[i])) for i in order]


class HybridDocs:
    """Combine two rankings with reciprocal rank fusion (no tuning needed)."""

    def __init__(self, first, second, c=60):
        self.first, self.second, self.c = first, second, c

    def search(self, query, k=5):
        fused = {}
        for retriever in (self.first, self.second):
            for rank, (doc_id, _) in enumerate(retriever.search(query, k=18), start=1):
                fused[doc_id] = fused.get(doc_id, 0.0) + 1.0 / (self.c + rank)
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)[:k]
class DenseChunks:
    """Dense search over passages; a document's score is its best passage."""

    def __init__(self, conn, model_name="BAAI/bge-small-en-v1.5", min_words=25):
        self.model = SentenceTransformer(model_name)
        rows = conn.execute("SELECT doc_id, title, body FROM documents ORDER BY doc_id").fetchall()
        self.chunks = []                               # (doc_id, text)
        for r in rows:
            buf = ""
            for block in [b.strip() for b in r["body"].split("\n\n") if b.strip()]:
                buf = (buf + "\n\n" + block).strip()
                if len(buf.split()) >= min_words:
                    self.chunks.append((r["doc_id"], r["title"] + ". " + buf))
                    buf = ""
            if buf:
                self.chunks.append((r["doc_id"], r["title"] + ". " + buf))
        self.emb = self.model.encode([t for _, t in self.chunks], normalize_embeddings=True)

    def _scores(self, query):
        q = QUERY_PREFIX + ID.sub(" ", query)
        return self.emb @ self.model.encode(q, normalize_embeddings=True)

    def search_chunks(self, query, k=5):               # used later for citations
        scores = self._scores(query)
        return [(self.chunks[i][0], self.chunks[i][1], float(scores[i]))
                for i in np.argsort(-scores)[:k]]

    def search(self, query, k=5):
        best = {}
        for i, s in enumerate(self._scores(query)):
            d = self.chunks[i][0]
            best[d] = max(best.get(d, -1.0), float(s))
        return sorted(best.items(), key=lambda x: x[1], reverse=True)[:k]
