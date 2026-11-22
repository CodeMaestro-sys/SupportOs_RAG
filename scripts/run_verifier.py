"""Run the LLM verifier on the 50 labelled drafts and save the outputs.
Run from the project root:  python scripts/run_verifier.py
Safe to re-run after a 503/429 error: finished calls come from the cache and cost no quota.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, "src")
from dotenv import load_dotenv

load_dotenv(override=True)
from llm import LLM
from verification import verify

VERIFIER_MODEL = "gemini-3.1-flash-lite"   # keep identical to VERIFIER_MODEL in evaluate_verifier.py
MIN_INTERVAL = 4.5                         # 60 / this model's requests per minute, plus a margin
MAX_FAILS_IN_A_ROW = 3
OUT = Path("results/verifier_outputs.json")

records = json.loads(Path("results/verification_drafts.json").read_text(encoding="utf-8"))
llm = LLM(model=VERIFIER_MODEL, min_interval=MIN_INTERVAL)
print(f"model: {llm.model} | drafts: {len(records)} | expect about "
      f"{len(records) * (MIN_INTERVAL + 3) / 60:.0f} minutes on a first run", flush=True)

outputs, fails_in_a_row, start = {}, 0, time.time()
for n, rec in enumerate(records, 1):
    t0, calls_before = time.time(), llm.calls
    draft_out = {"draft": rec["draft"], "abstained": False, "cited": rec["cited"],
                 "passages": [tuple(p) for p in rec["passages"]]}
    try:
        outputs[rec["draft_id"]] = verify(llm, draft_out, rec["query"])
        fails_in_a_row = 0
        source = "API" if llm.calls > calls_before else "cache"
        print(f"[{n:2d}/{len(records)}] draft {rec['draft_id']:2d} ok via {source} in {time.time() - t0:4.1f}s", flush=True)
    except Exception as e:
        fails_in_a_row += 1
        print(f"[{n:2d}/{len(records)}] draft {rec['draft_id']:2d} FAILED after {time.time() - t0:.0f}s: "
              f"{getattr(e, 'code', type(e).__name__)}", flush=True)
        if fails_in_a_row >= MAX_FAILS_IN_A_ROW:
            print("stopping: the service is overloaded or the quota is used up. Re-run later; finished calls are cached.")
            break

if len(outputs) == len(records):
    OUT.write_text(json.dumps(outputs, indent=1), encoding="utf-8")
    print(f"saved {OUT} | verified: {len(outputs)} | real calls: {llm.calls} | "
          f"cache hits: {llm.cache_hits} | total {time.time() - start:.0f}s")
else:
    print(f"incomplete ({len(outputs)}/{len(records)}), nothing saved")