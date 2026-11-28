"""Re-run the retrieval and drafting measurements on the frozen data and log them to results/.
Run from the project root:
    python scripts/rerun_metrics.py --part retrieval     (no API calls, a few minutes)
    python scripts/rerun_metrics.py --part drafting      (about 53 drafter calls; cached ones are free)
    python scripts/rerun_metrics.py                      (both)
Check first that the data is unchanged:  python scripts/make_manifest.py --check
"""
import argparse
import csv
import os
import sys
import time
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, "src")
from dotenv import load_dotenv

load_dotenv(override=True)

RESULTS = Path("results")


def log_row(filename, header, row):
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / filename
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(header)
        w.writerow(row)


def load_gold(conn):
    gold = defaultdict(set)
    for r in conn.execute("SELECT intent, doc_id FROM intent_docs"):
        gold[r["intent"]].add(r["doc_id"])
    return gold


def evaluate(rows, searcher, gold):
    hits = {1: 0, 3: 0, 5: 0}
    rr = 0.0
    for r in rows:
        ranked = [d for d, _ in searcher.search(r["query"], k=18)]
        ranks = [i + 1 for i, d in enumerate(ranked) if d in gold[r["intent"]]]
        first = min(ranks) if ranks else 10 ** 6
        for k in hits:
            hits[k] += first <= k
        rr += 1 / first
    n = len(rows)
    return {"n": n, **{f"hit@{k}": round(v / n, 3) for k, v in hits.items()}, "MRR": round(rr / n, 3)}


def retrieval_part(conn, gold):
    from retrieval import BM25Docs, DenseChunks, DenseDocs, HybridDocs
    tune = conn.execute("SELECT intent, flags, query FROM tickets WHERE split='past' AND ticket_id % 20 = 0").fetchall()
    confirm = conn.execute("SELECT intent, flags, query FROM tickets WHERE split='past' AND ticket_id % 20 = 10").fetchall()
    bm25, dense, chunks = BM25Docs(conn), DenseDocs(conn), DenseChunks(conn)
    systems = [("bm25_clean", bm25), ("dense_doc", dense), ("dense_chunks", chunks),
               ("hybrid_rrf_equal", HybridDocs(bm25, dense))]
    for name, searcher in systems:
        for sample_name, rows in [("tuning", tune), ("confirm", confirm)]:
            m = evaluate(rows, searcher, gold)
            print(f"{name:18s} {sample_name:8s} {m}", flush=True)
            log_row("retrieval_results.csv", ["date", "system", "sample", "n", "hit@1", "hit@3", "hit@5", "MRR", "note"],
                    [date.today().isoformat(), name, sample_name, m["n"], m["hit@1"], m["hit@3"], m["hit@5"], m["MRR"],
                     "frozen data data-v1"])


def summarize_drafts(results, gold, outcome):
    counts = Counter(outcome(o) for _, o in results)
    answered = [(r, o) for r, o in results if outcome(o) == "answered"]
    cited = sum(bool(o["cited"]) for _, o in answered)
    correct = sum(any(o["passages"][i - 1][0] in gold[r["intent"]] for i in o["cited"]) for r, o in answered)
    return counts, len(answered), cited, correct


def drafting_part(conn, gold):
    from drafting import SYSTEM_C, draft, outcome
    from llm import LLM
    from retrieval import DenseChunks

    retriever = DenseChunks(conn)
    llm = LLM(min_interval=float(os.getenv("DRAFTER_MIN_INTERVAL", "4.5")))
    sets = {
        "dev (answerable)": conn.execute("SELECT ticket_id, intent, query FROM tickets WHERE split='dev'").fetchall(),
        "abstain dev": conn.execute("SELECT ticket_id, intent, query FROM tickets WHERE split='abstain' "
                                    "AND ticket_id % 3 = 0").fetchall(),
    }
    for name, rows in sets.items():
        results = []
        for n, r in enumerate(rows, 1):
            t0, before = time.time(), llm.calls
            results.append((r, draft(llm, retriever, r["query"], floor=0.0, system=SYSTEM_C)))
            src = "API" if llm.calls > before else "cache"
            print(f"  [{n:2d}/{len(rows)}] {name}: {outcome(results[-1][1]):9s} via {src} in {time.time() - t0:4.1f}s", flush=True)
        counts, answered, cited, correct = summarize_drafts(results, gold, outcome)
        print(f"{name}: n={len(rows)} {dict(counts)} | answered with citation {cited}/{answered}, "
              f"cites correct document {correct}/{answered}", flush=True)
        log_row("drafting_results.csv",
                ["date", "model", "prompt", "floor", "set", "n", "answered", "clarify", "refused", "cited", "cites_correct_doc", "note"],
                [date.today().isoformat(), llm.model, "C", 0.0, name, len(rows), counts["answered"], counts["clarify"],
                 counts["refused"], cited, correct, "frozen data data-v1"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--part", choices=["retrieval", "drafting", "all"], default="all")
    part = ap.parse_args().part
    from db import get_connection
    conn = get_connection()
    gold = load_gold(conn)
    if part in ("retrieval", "all"):
        print("== retrieval ==", flush=True)
        retrieval_part(conn, gold)
    if part in ("drafting", "all"):
        print("== drafting ==", flush=True)
        drafting_part(conn, gold)
    print("logged to", RESULTS)


if __name__ == "__main__":
    main()