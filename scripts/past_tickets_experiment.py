"""Do past resolved tickets help? Compare drafts from policy passages only (prompt C) with drafts that also see the
two most similar past tickets (prompt D) on the dev tickets and the development abstain tickets.
Run from the project root:   python scripts/past_tickets_experiment.py
Costs about 53 new drafter calls plus up to about 40 verifier calls; repeats come from the cache."""
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

sys.path.insert(0, "src")
from dotenv import load_dotenv

load_dotenv(override=True)

N_POLICY = 4
OUT = Path("results/past_tickets_experiment.json")


def doc_unsupported(verifier, out, query, verify, exempt, norm):
    """Verify the draft against the POLICY passages only: sentences that rely on a past ticket show up as unsupported."""
    policy = out["passages"][:N_POLICY]
    items = verify(verifier, {"draft": out["draft"], "abstained": False, "cited": out["cited"], "passages": policy}, query)
    return [i for i in items if i["llm_label"] == "unsupported" and norm(i["sentence"]) not in exempt], items


def run_experiment(conn, index, retriever, drafter, verifier, log=print):
    from drafting import SYSTEM_C, SYSTEM_D, draft, outcome
    from past_tickets import as_passages
    from pipeline import EXEMPT, _norm
    from verification import verify

    sets = {
        "dev (answerable)": conn.execute("SELECT ticket_id, intent, query FROM tickets WHERE split='dev'").fetchall(),
        "abstain dev": conn.execute("SELECT ticket_id, intent, query FROM tickets WHERE split='abstain' "
                                    "AND ticket_id % 3 = 0").fetchall(),
    }
    report, saved = {}, []
    for set_name, rows in sets.items():
        stats = {"C": Counter(), "D": Counter()}
        same_intent = cites_past = bad_c = bad_d = ans_c = ans_d = 0
        examples = []
        for n, r in enumerate(rows, 1):
            past = index.search(r["query"], k=2)
            same_intent += past[0]["intent"] == r["intent"]
            out_c = draft(drafter, retriever, r["query"], floor=0.0, system=SYSTEM_C)
            out_d = draft(drafter, retriever, r["query"], floor=0.0, system=SYSTEM_D, extra_passages=as_passages(past))
            kc, kd = outcome(out_c), outcome(out_d)
            stats["C"][kc] += 1
            stats["D"][kd] += 1
            record = {"set": set_name, "ticket_id": r["ticket_id"], "intent": r["intent"], "query": r["query"],
                      "C": {"outcome": kc, "draft": out_c["draft"]},
                      "D": {"outcome": kd, "draft": out_d["draft"], "cited": out_d["cited"]},
                      "past_ticket_ids": [m["ticket_id"] for m in past]}
            if kc == "answered":
                bad, _ = doc_unsupported(verifier, out_c, r["query"], verify, EXEMPT, _norm)
                ans_c += 1
                bad_c += bool(bad)
                record["C"]["not_in_policy"] = [b["sentence"] for b in bad]
            if kd == "answered":
                cites_past += any(i > N_POLICY for i in out_d["cited"])
                bad, _ = doc_unsupported(verifier, out_d, r["query"], verify, EXEMPT, _norm)
                ans_d += 1
                bad_d += bool(bad)
                record["D"]["not_in_policy"] = [b["sentence"] for b in bad]
                for b in bad:
                    if len(examples) < 6:
                        examples.append({"customer": r["query"], "sentence": b["sentence"]})
            saved.append(record)
            log(f"  [{n:2d}/{len(rows)}] {set_name}: C {kc:9s} D {kd:9s}", flush=True)
        report[set_name] = {
            "n": len(rows), "C": dict(stats["C"]), "D": dict(stats["D"]),
            "top1_past_ticket_has_same_intent": f"{same_intent}/{len(rows)}",
            "D_answered_citing_a_past_ticket": f"{cites_past}/{ans_d}",
            "C_answered_with_a_sentence_not_in_the_policy": f"{bad_c}/{ans_c}",
            "D_answered_with_a_sentence_not_in_the_policy": f"{bad_d}/{ans_d}",
            "examples_D_not_in_policy": examples}
    return report, saved


def main():
    from db import get_connection
    from llm import LLM
    from past_tickets import PastTicketIndex
    from retrieval import DenseChunks

    conn = get_connection()
    retriever = DenseChunks(conn)
    index = PastTicketIndex(conn, retriever.model)
    drafter = LLM(min_interval=float(os.getenv("DRAFTER_MIN_INTERVAL", "4.5")))
    verifier = LLM(model=os.getenv("VERIFIER_MODEL", "gemini-3.1-flash-lite"),
                   min_interval=float(os.getenv("VERIFIER_MIN_INTERVAL", "4.5")))
    t0 = time.time()
    report, saved = run_experiment(conn, index, retriever, drafter, verifier)
    OUT.write_text(json.dumps({"report": report, "drafts": saved, "drafter": drafter.model,
                               "verifier": verifier.model}, indent=1), encoding="utf-8")
    print(json.dumps(report, indent=1))
    print(f"saved {OUT} | drafter calls {drafter.calls} | verifier calls {verifier.calls} | {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()