"""Fingerprint of the frozen data and settings.
Create:  python scripts/make_manifest.py
Verify:  python scripts/make_manifest.py --check
"""
import hashlib
import json
import os
import sys
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

load_dotenv(override=True)
OUT = Path("results/data_manifest.json")

SETTINGS = {                                   # edit these to match what you actually used
    "split_seed": 42,
    "left_out_intents": ["newsletter_subscription", "check_cancellation_fee", "switch_account", "review"],
    "test_per_intent": 4,
    "dev_per_intent": 2,
    "abstain_dev_rule": "ticket_id % 3 == 0",
    "retrieval": "BAAI/bge-small-en-v1.5, passage chunks, no retrieval floor",
    "prompt": "C",
    "llm_model": os.getenv("GEMINI_MODEL"),
}


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build():
    clean = sorted(Path("data/processed").glob("*_clean.csv"))
    docs = sorted(p for p in Path("data/docs").glob("*") if p.is_file())
    return {
        "files": {p.as_posix(): sha256(p) for p in clean + docs},
        "rows": {p.name: len(pd.read_csv(p, keep_default_na=False, encoding="utf-8")) for p in clean},
        "settings": SETTINGS,
    }


if __name__ == "__main__":
    current = build()
    if "--check" in sys.argv:
        saved = json.loads(OUT.read_text(encoding="utf-8"))
        changed = [f for f, h in current["files"].items() if saved["files"].get(f) != h]
        missing = [f for f in saved["files"] if f not in current["files"]]
        print("DATA UNCHANGED" if not changed and not missing else f"CHANGED: {changed} MISSING: {missing}")
    else:
        OUT.parent.mkdir(exist_ok=True)
        OUT.write_text(json.dumps(current, indent=2), encoding="utf-8")
        print("manifest written:", OUT, "|", current["rows"])