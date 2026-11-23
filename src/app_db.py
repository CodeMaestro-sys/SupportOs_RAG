"""Application database: tickets, drafts and resolutions created while the app runs.
It is a separate file from data/supportops.db (the reference data that scripts/load_data.py
deletes and rebuilds), so rebuilding the reference data never erases agent activity."""
import sqlite3
from pathlib import Path

APP_DB_PATH = Path("data/app.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS support_tickets (
    ticket_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    query      TEXT NOT NULL,
    status     TEXT NOT NULL DEFAULT 'open' CHECK (status IN ('open', 'in_review', 'resolved')),
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS drafts (
    draft_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id       INTEGER NOT NULL REFERENCES support_tickets(ticket_id),
    created_at      TEXT NOT NULL,
    model           TEXT NOT NULL,
    verifier_model  TEXT NOT NULL,
    prompt_version  TEXT NOT NULL,
    outcome         TEXT NOT NULL CHECK (outcome IN ('answered', 'clarify', 'refused')),
    reason          TEXT NOT NULL DEFAULT '',
    draft_text      TEXT NOT NULL,
    passages_json   TEXT NOT NULL,
    sentences_json  TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS resolutions (
    resolution_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id     INTEGER NOT NULL REFERENCES support_tickets(ticket_id),
    draft_id      INTEGER REFERENCES drafts(draft_id),
    agent_action  TEXT NOT NULL CHECK (agent_action IN ('accepted', 'edited', 'rejected')),
    final_text    TEXT NOT NULL,
    resolved_at   TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_support_tickets_status ON support_tickets(status);
CREATE INDEX IF NOT EXISTS idx_drafts_ticket ON drafts(ticket_id);
"""


def get_app_connection(path=None):
    path = Path(path or APP_DB_PATH)             # looked up at call time, so tests can point it elsewhere
    path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_app_db(conn):
    conn.executescript(SCHEMA)
    # Migration: CREATE TABLE IF NOT EXISTS never changes a table that already exists, so columns added
    # later are added here with ALTER TABLE if they are missing.
    columns = {row["name"] for row in conn.execute("PRAGMA table_info(resolutions)")}
    if "similarity" not in columns:
        conn.execute("ALTER TABLE resolutions ADD COLUMN similarity REAL")
    conn.commit()