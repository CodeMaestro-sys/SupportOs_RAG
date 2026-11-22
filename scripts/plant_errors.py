"""Create drafts with ONE planted error each, so the verifier can be tested on known mistakes.
Run from the project root:  python scripts/plant_errors.py
Reads:  results/verification_drafts.json, results/labels_sentences.csv
Writes: results/planted_drafts.json
"""
import json
import random
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, "src")
from verification import split_sentences

SEED = 11
PER_TYPE = 6                       # 4 types x 6 = 24 planted drafts
OUT = Path("results/planted_drafts.json")


def load_sentence_labels(path="results/labels_sentences.csv"):
    with open(path, encoding="utf-8-sig") as f:
        sep = "\t" if "\t" in f.readline() else ","
    d = pd.read_csv(path, sep=sep, encoding="utf-8-sig", keep_default_na=False)
    d["label"] = d["label"].str.strip().str.lower().str.replace(" ", "_")
    assert d["label"].isin(["supported", "unsupported", "not_factual"]).all(), "invalid sentence label"
    return {(int(r.draft_id), r.sentence): r.label for r in d.itertuples()}


# ---- the four kinds of planted error --------------------------------------------------------
def bump(n):
    return n * 2 if n <= 10 else n + 15


NUMBER_PATTERNS = [
    (re.compile(r"\b(\d+) to (\d+) business days"),
     lambda m: f"{int(m.group(1)) + 3} to {int(m.group(2)) + 5} business days"),
    (re.compile(r"\b(\d+) (business days|days|hours|minutes)\b"),
     lambda m: f"{bump(int(m.group(1)))} {m.group(2)}"),
    (re.compile(r"\b(\d{1,2}) (AM|PM)\b"),
     lambda m: f"{(int(m.group(1)) % 12) + 2} {m.group(2)}"),
]

CONTACT_SWAPS = [("support@shopease.example", "help@shopease.example"),
                 ("+91 00000 00000", "+91 11111 11111"),
                 ("www.shopease.example", "www.shopease-support.example")]

CONTRADICTIONS = [("can no longer be changed", "can still be changed"),
                  ("at any time before it is dispatched", "at any time, including after it is dispatched"),
                  ("is no longer possible", "is still possible"),
                  ("cannot be added to the cart", "can still be added to the cart"),
                  ("cannot be changed online", "can always be changed online"),
                  ("will never ask you", "may ask you"),
                  ("Business days exclude Sundays", "Business days include Sundays")]

INVENTED = ["You will also receive a 10% loyalty discount on your next order",
            "You can also contact us on WhatsApp at any time, day or night",
            "Premium members are handled first and receive a reply within 1 hour",
            "A manager will call you within 30 minutes to confirm this",
            "Requests made at weekends are processed with priority"]


def corrupt_number(s):
    for pat, fn in NUMBER_PATTERNS:
        if pat.search(s):
            return pat.sub(fn, s, count=1)
    return None


def corrupt_contact(s):
    for old, new in CONTACT_SWAPS:
        if old in s:
            return s.replace(old, new, 1)
    return None


def corrupt_contradiction(s):
    for old, new in CONTRADICTIONS:
        if old in s:
            return s.replace(old, new, 1)
    return None


def build(records, labels, rng):
    candidates = {"contradiction": [], "number_change": [], "contact_change": [], "invented_fact": []}
    for rec in records:
        sents = split_sentences(rec["draft"])
        if not rec["cited"] or any(labels.get((rec["draft_id"], s)) is None for s in sents):
            continue
        if any(labels[(rec["draft_id"], s)] == "unsupported" for s in sents):
            continue                                              # keep clean negatives only
        for s in sents:
            if labels[(rec["draft_id"], s)] != "supported":
                continue
            for kind, fn in [("contradiction", corrupt_contradiction), ("number_change", corrupt_number),
                             ("contact_change", corrupt_contact)]:
                new = fn(s)
                if new and new != s:
                    candidates[kind].append((rec, s, new))
        candidates["invented_fact"].append((rec, None, None))

    planted, used = [], set()
    for kind in ["contradiction", "number_change", "contact_change", "invented_fact"]:   # scarcest first
        pool = candidates[kind][:]
        rng.shuffle(pool)
        made = 0
        for rec, old, new in pool:
            if made == PER_TYPE:
                break
            if rec["draft_id"] in used:
                continue
            draft = rec["draft"]
            if kind == "invented_fact":
                first = next(s for s in split_sentences(draft) if re.search(r"\[\d+\]", s))
                cite = rec["cited"][0]
                new = rng.choice(INVENTED) + f" [{cite}]."
                new_draft = draft.replace(first, first + " " + new, 1)
                changed = new
            else:
                if old not in draft:
                    continue
                new_draft = draft.replace(old, new, 1)
                changed = new
            new_sents = split_sentences(new_draft)
            if changed not in new_sents:                          # splitting must reproduce the planted sentence
                continue
            sent_labels = []
            for s in new_sents:
                if s == changed:
                    sent_labels.append("unsupported")
                else:
                    sent_labels.append(labels.get((rec["draft_id"], s)))
            if None in sent_labels:
                continue
            planted.append({"planted_id": len(planted) + 1, "source_draft_id": rec["draft_id"],
                            "kind": kind, "query": rec["query"], "draft": new_draft,
                            "planted_sentence": changed, "cited": rec["cited"],
                            "passages": rec["passages"],
                            "sentences": new_sents, "human_labels": sent_labels})
            used.add(rec["draft_id"])
            made += 1
    return planted


if __name__ == "__main__":
    records = json.loads(Path("results/verification_drafts.json").read_text(encoding="utf-8"))
    labels = load_sentence_labels()
    planted = build(records, labels, random.Random(SEED))
    OUT.write_text(json.dumps(planted, indent=1), encoding="utf-8")
    from collections import Counter
    print("planted drafts:", len(planted), dict(Counter(p["kind"] for p in planted)))
    for p in planted[:3]:
        print(f'\n[{p["kind"]}] draft {p["source_draft_id"]}\n   planted: {p["planted_sentence"]}')