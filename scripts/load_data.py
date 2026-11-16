import random
import sys
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

sys.path.insert(0, "src")
from db import DB_PATH, get_connection, init_db

PROCESSED = Path("data/processed")
DOCS = Path("data/docs")


def read_doc(path):
    text = path.read_text(encoding="utf-8")
    _, header, body = text.split("---", 2)          # frontmatter between the first two ---
    meta = dict(line.split(": ", 1) for line in header.strip().splitlines())
    return meta["doc_id"], meta["title"], meta["date"], body.strip()


def main():
    if DB_PATH.exists():
        DB_PATH.unlink()                             # rebuild from scratch each run
    conn = get_connection()
    init_db(conn)

    docs = [read_doc(p) for p in sorted(DOCS.glob("*.md"))]
    conn.executemany("INSERT INTO documents VALUES (?, ?, ?, ?)", docs)

    mapping = pd.read_csv(DOCS / "intent_to_doc.csv")
    conn.executemany("INSERT INTO intent_docs VALUES (?, ?)", mapping.values.tolist())

    for split in ["past", "dev", "test", "abstain"]:
        d = pd.read_csv(PROCESSED / f"{split}_clean.csv", keep_default_na=False, encoding="utf-8")
        rows = []
        for r in d.itertuples():
            resolved = None
            if split == "past":                      # synthetic but repeatable date
                rng = random.Random(int(r.ticket_id))
                resolved = (date(2026, 1, 1) + timedelta(days=rng.randint(0, 300))).isoformat()
            rows.append((int(r.ticket_id), split, r.intent, r.category, r.flags,
                         r.instruction, r.response, resolved))
        conn.executemany("INSERT INTO tickets VALUES (?, ?, ?, ?, ?, ?, ?, ?)", rows)

    conn.commit()
    for row in conn.execute("SELECT split, COUNT(*) AS n FROM tickets GROUP BY split"):
        print(row["split"], row["n"])
    print("documents:", conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0])
    print("intent mappings:", conn.execute("SELECT COUNT(*) FROM intent_docs").fetchone()[0])


main()