"""SupportOps API.  Run from the project root:
    uvicorn api:app --reload --app-dir src
then open http://127.0.0.1:8000/docs
"""
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

import app_db

VALID_STATUSES = {"open", "in_review", "resolved"}


@asynccontextmanager
async def lifespan(app):
    conn = app_db.get_app_connection()           # runs once when the server starts
    app_db.init_app_db(conn)
    conn.close()
    yield


app = FastAPI(title="SupportOps API", version="0.1", lifespan=lifespan)


def get_db():
    """One database connection per request, always closed afterwards."""
    conn = app_db.get_app_connection()
    try:
        yield conn
    finally:
        conn.close()


class TicketIn(BaseModel):
    query: str = Field(min_length=3, max_length=2000)


class TicketOut(BaseModel):
    ticket_id: int
    query: str
    status: str
    created_at: str


def fetch_ticket(db, ticket_id):
    row = db.execute("SELECT * FROM support_tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return dict(row)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/tickets", response_model=TicketOut, status_code=201)
def create_ticket(body: TicketIn, db=Depends(get_db)):
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cur = db.execute("INSERT INTO support_tickets (query, status, created_at) VALUES (?, 'open', ?)",
                     (body.query.strip(), now))
    db.commit()
    return fetch_ticket(db, cur.lastrowid)


@app.get("/tickets", response_model=list[TicketOut])
def list_tickets(status: str | None = None, db=Depends(get_db)):
    if status is not None and status not in VALID_STATUSES:
        raise HTTPException(status_code=400, detail=f"status must be one of {sorted(VALID_STATUSES)}")
    if status:
        rows = db.execute("SELECT * FROM support_tickets WHERE status = ? ORDER BY ticket_id", (status,)).fetchall()
    else:
        rows = db.execute("SELECT * FROM support_tickets ORDER BY ticket_id").fetchall()
    return [dict(r) for r in rows]


@app.get("/tickets/{ticket_id}", response_model=TicketOut)
def get_ticket(ticket_id: int, db=Depends(get_db)):
    return fetch_ticket(db, ticket_id)