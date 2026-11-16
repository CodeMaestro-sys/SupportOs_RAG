import sqlite3
from pathlib import Path

DB_PATH = Path("data/supportops.db")

SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    doc_id    TEXT PRIMARY KEY,
    title     TEXT NOT NULL,
    doc_date  TEXT NOT NULL,
    body      TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS intent_docs (
    intent  TEXT NOT NULL,
    doc_id  TEXT NOT NULL REFERENCES documents(doc_id),
    PRIMARY KEY (intent, doc_id)
);
CREATE TABLE IF NOT EXISTS tickets (
    ticket_id     INTEGER PRIMARY KEY,
    split         TEXT NOT NULL CHECK (split IN ('past', 'dev', 'test', 'abstain')),
    intent        TEXT NOT NULL,
    category      TEXT NOT NULL,
    flags         TEXT NOT NULL,
    query         TEXT NOT NULL,
    response      TEXT NOT NULL,
    resolved_date TEXT
);
CREATE INDEX IF NOT EXISTS idx_tickets_split ON tickets(split);
"""


def get_connection(path=DB_PATH):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row          # rows behave like dictionaries
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()