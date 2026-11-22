"""Compare the LLM check, the rule check and both together on natural and planted drafts.
Run from the project root AFTER your sentence labels are final:  python scripts/evaluate_verifier.py
Needs: results/verification_drafts.json, results/verifier_outputs.json, results/labels_sentences.csv,
       results/planted_drafts.json
"""
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, "src")
sys.path.insert(0, "scripts")
from dotenv import load_dotenv

load_dotenv(override=True)
from llm import LLM
from plant_errors import load_sentence_labels
from verification import CONTACT, NUM, verify

VERIFIER_MODEL = "gemini-3.1-flash-lite"   # MUST be the same model that made verifier_outputs.json
MIN_INTERVAL = 4.5                         # 60 / this model's requests per minute, plus a margin
OUT = Path("results/verifier_eval.json")


def strict_rule_flags(sentence, passages, customer):
    """Numbers, emails and web addresses that appear nowhere in the passages or customer message.
    Whole-token matching (a '2' does not match inside '12')."""
    source = (" ".join(p[1] for p in passages) + " " + customer).lower()
    s = re.sub(r"\[\d+\]", "", sentence)
    bad = []
    for tok in NUM.findall(s) + CONTACT.findall(s):
        t = tok.lower().rstrip(".,")
        if not re.search(r"(?<![\d,.])" + re.escape(t) + r"(?!\d|,\d|\.\d)", source):
            bad.append(tok)
    return bad


def wilson(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (max(0.0, c - h), min(1.0, c + h))


def fmt(k, n):
    if n == 0:
        return "n/a"
    lo, hi = wilson(k, n)
    return f"{k}/{n} = {k / n:.2f} (95% CI {lo:.2f} to {hi:.2f})"


def collect_rows():
    """One row per sentence: truth, llm flag, rule flag, kind, source ('natural' or 'planted')."""
    labels = load_sentence_labels()
    records = {r["draft_id"]: r for r in json.loads(Path("results/verification_drafts.json").read_text(encoding="utf-8"))}
    natural_out = json.loads(Path("results/verifier_outputs.json").read_text(encoding="utf-8"))
    planted = json.loads(Path("results/planted_drafts.json").read_text(encoding="utf-8"))
    rows = []

    for did, items in natural_out.items():
        rec = records[int(did)]
        for it in items:
            truth = labels[(int(did), it["sentence"])]
            rows.append({"src": "natural", "kind": "none", "truth": truth, "llm_label": it["llm_label"],
                         "rule": bool(strict_rule_flags(it["sentence"], rec["passages"], rec["query"])),
                         "sentence": it["sentence"], "draft": int(did)})

    llm = LLM(model=VERIFIER_MODEL, min_interval=MIN_INTERVAL)
    for n, p in enumerate(planted, 1):
        t0 = time.time()
        out = verify(llm, {"draft": p["draft"], "abstained": False, "cited": p["cited"],
                           "passages": [tuple(x) for x in p["passages"]]}, p["query"])
        print(f"[{n:2d}/{len(planted)}] planted {p['planted_id']:2d} ({p['kind']}) done in {time.time() - t0:4.1f}s", flush=True)
        assert [o["sentence"] for o in out] == p["sentences"], f'sentence mismatch in planted {p["planted_id"]}'
        for it, truth in zip(out, p["human_labels"]):
            rows.append({"src": "planted", "kind": p["kind"] if truth == "unsupported" else "none",
                         "truth": truth, "llm_label": it["llm_label"],
                         "rule": bool(strict_rule_flags(it["sentence"], p["passages"], p["query"])),
                         "sentence": it["sentence"], "draft": p["source_draft_id"]})
    print(f"verifier model: {VERIFIER_MODEL} | real calls: {llm.calls} | cache hits: {llm.cache_hits}")
    return rows


def main():
    rows = collect_rows()
    for r in rows:
        r["llm"] = r["llm_label"] == "unsupported"
        r["either"] = r["llm"] or r["rule"]

    print("\n== Natural drafts (human labels; the drafter made no unsupported sentences if the count below is 0) ==")
    nat = [r for r in rows if r["src"] == "natural"]
    print("human labels:", dict(Counter(r["truth"] for r in nat)))
    print("verifier labels:", dict(Counter(r["llm_label"] for r in nat)))
    cm = Counter((r["truth"], r["llm_label"]) for r in nat)
    for (t, v), n in sorted(cm.items()):
        print(f"   human {t:12s} -> verifier {v:12s}: {n}")
    fact = [r for r in nat if r["truth"] == "supported"]
    print("false alarms on natural supported sentences: LLM", fmt(sum(r["llm"] for r in fact), len(fact)),
          "| rule", fmt(sum(r["rule"] for r in fact), len(fact)))

    print("\n== Planted errors (known unsupported sentences) ==")
    factual = [r for r in rows if r["truth"] in ("supported", "unsupported")]
    pos = [r for r in factual if r["truth"] == "unsupported"]
    neg = [r for r in factual if r["truth"] == "supported"]
    print(f"planted sentences: {len(pos)} | clean factual sentences: {len(neg)}")
    for name in ["llm", "rule", "either"]:
        tp = sum(r[name] for r in pos)
        fp = sum(r[name] for r in neg)
        flagged = tp + fp
        print(f"  {name:6s} recall {fmt(tp, len(pos))} | precision {fmt(tp, flagged)} | false alarms {fmt(fp, len(neg))}")
    print("\n  recall by kind of error:")
    by_kind = defaultdict(list)
    for r in pos:
        by_kind[r["kind"]].append(r)
    for kind, rs in sorted(by_kind.items()):
        print(f"   {kind:15s} llm {sum(r['llm'] for r in rs)}/{len(rs)} | rule {sum(r['rule'] for r in rs)}/{len(rs)}"
              f" | either {sum(r['either'] for r in rs)}/{len(rs)}")
    print("\n  unparsed verifier answers:", sum(r["llm_label"] == "unparsed" for r in rows))

    OUT.write_text(json.dumps({"model": VERIFIER_MODEL, "rows": rows}, indent=1), encoding="utf-8")
    print("\nsaved:", OUT)


if __name__ == "__main__":
    main()