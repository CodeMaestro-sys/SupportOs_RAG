"""SupportOps API.  Run from the project root:
    python -m uvicorn api:app --reload --app-dir src
then open http://127.0.0.1:8000/docs
"""
import difflib
import json
import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import Literal

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

import app_db
from textutil import to_customer_text

log = logging.getLogger("supportops")
VALID_STATUSES = {"open", "in_review", "resolved"}


@asynccontextmanager
async def lifespan(app):
    conn = app_db.get_app_connection()           # runs once when the server starts
    app_db.init_app_db(conn)
    conn.close()
    yield


app = FastAPI(title="SupportOps API", version="0.5", lifespan=lifespan)

_pipeline = None


def get_pipeline():
    """Build the real pipeline on first use (loading the embedding model takes a few seconds)."""
    global _pipeline
    if _pipeline is None:
        try:
            from pipeline import Pipeline
            _pipeline = Pipeline.from_env()
        except Exception:
            log.exception("could not build the pipeline")
            raise HTTPException(status_code=503, detail="The drafting pipeline could not start. Check the server log "
                                                        "(is GEMINI_API_KEY set in .env?).")
    return _pipeline


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


class Passage(BaseModel):
    doc_id: str
    text: str
    score: float


class SimilarOut(BaseModel):
    ticket_id: int
    intent: str
    query: str
    response: str
    score: float


class Sentence(BaseModel):
    id: int
    text: str
    label: str                  # supported, unsupported or not_factual
    rule_flags: list[str]       # numbers or contact details found in no passage


class DraftOut(BaseModel):
    draft_id: int
    ticket_id: int
    created_at: str
    outcome: str                # answered, clarify or refused
    reason: str
    draft_text: str            # raw draft with [n] citations
    reply_text: str            # the same text as the customer should read it
    passages: list[Passage]
    sentences: list[Sentence]
    model: str
    verifier_model: str
    prompt_version: str


class ResolveIn(BaseModel):
    action: Literal["accepted", "edited", "rejected"]
    final_text: str | None = Field(default=None, max_length=4000)
    draft_id: int | None = None            # defaults to the latest draft of the ticket


class ResolutionOut(BaseModel):
    resolution_id: int
    ticket_id: int
    draft_id: int | None
    agent_action: str
    final_text: str
    similarity: float | None               # 1.0 = sent exactly as drafted
    resolved_at: str


def fetch_ticket(db, ticket_id):
    row = db.execute("SELECT * FROM support_tickets WHERE ticket_id = ?", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail=f"Ticket {ticket_id} not found")
    return dict(row)


def draft_row_to_dict(row):
    d = dict(row)
    d["passages"] = json.loads(d.pop("passages_json"))
    d["sentences"] = json.loads(d.pop("sentences_json"))
    d["reply_text"] = to_customer_text(d["draft_text"])
    return d


@app.get("/", include_in_schema=False)
def root():
    return {"app": "SupportOps API", "docs": "/docs", "health": "/health"}


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


@app.post("/tickets/{ticket_id}/draft", response_model=DraftOut, status_code=201)
def create_draft(ticket_id: int, db=Depends(get_db), pipeline=Depends(get_pipeline)):
    ticket = fetch_ticket(db, ticket_id)
    if ticket["status"] == "resolved":
        raise HTTPException(status_code=409, detail="This ticket is already resolved")
    try:
        result = pipeline.run(ticket["query"])
    except Exception:
        log.exception("pipeline failed for ticket %s", ticket_id)
        raise HTTPException(status_code=502, detail="The language model or retrieval step failed. Try again later.")
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cur = db.execute(
        "INSERT INTO drafts (ticket_id, created_at, model, verifier_model, prompt_version, outcome, reason, "
        "draft_text, passages_json, sentences_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (ticket_id, now, result["model"], result["verifier_model"], result["prompt_version"], result["outcome"],
         result["reason"], result["draft_text"], json.dumps(result["passages"]), json.dumps(result["sentences"])))
    db.execute("UPDATE support_tickets SET status = 'in_review' WHERE ticket_id = ?", (ticket_id,))
    db.commit()
    row = db.execute("SELECT * FROM drafts WHERE draft_id = ?", (cur.lastrowid,)).fetchone()
    return draft_row_to_dict(row)


@app.get("/tickets/{ticket_id}/draft", response_model=DraftOut)
def latest_draft(ticket_id: int, db=Depends(get_db)):
    fetch_ticket(db, ticket_id)
    row = db.execute("SELECT * FROM drafts WHERE ticket_id = ? ORDER BY draft_id DESC LIMIT 1", (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="No draft has been created for this ticket yet")
    return draft_row_to_dict(row)


@app.post("/tickets/{ticket_id}/resolve", response_model=ResolutionOut, status_code=201)
def resolve_ticket(ticket_id: int, body: ResolveIn, db=Depends(get_db)):
    ticket = fetch_ticket(db, ticket_id)
    if ticket["status"] == "resolved":
        raise HTTPException(status_code=409, detail="This ticket is already resolved")

    if body.draft_id is not None:
        draft = db.execute("SELECT * FROM drafts WHERE draft_id = ? AND ticket_id = ?",
                           (body.draft_id, ticket_id)).fetchone()
        if draft is None:
            raise HTTPException(status_code=404, detail="That draft does not belong to this ticket")
    else:
        draft = db.execute("SELECT * FROM drafts WHERE ticket_id = ? ORDER BY draft_id DESC LIMIT 1",
                           (ticket_id,)).fetchone()
    draft_text = to_customer_text(draft["draft_text"]) if draft else ""        # compare and store the customer-facing text

    if body.action == "accepted":
        if not draft_text:
            raise HTTPException(status_code=422, detail="There is no draft text to accept")
        final_text = draft_text
    else:
        final_text = (body.final_text or "").strip()
        if not final_text:
            raise HTTPException(status_code=422, detail="final_text is required for this action")
        if body.action == "edited":
            if not draft_text:
                raise HTTPException(status_code=422, detail="There is no draft to edit; use the action 'rejected'")
            if final_text == draft_text:
                raise HTTPException(status_code=422, detail="The text is unchanged; use the action 'accepted'")

    similarity = round(difflib.SequenceMatcher(None, draft_text, final_text).ratio(), 3) if draft_text else None
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    cur = db.execute(
        "INSERT INTO resolutions (ticket_id, draft_id, agent_action, final_text, resolved_at, similarity) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (ticket_id, draft["draft_id"] if draft else None, body.action, final_text, now, similarity))
    db.execute("UPDATE support_tickets SET status = 'resolved' WHERE ticket_id = ?", (ticket_id,))
    db.commit()
    return dict(db.execute("SELECT * FROM resolutions WHERE resolution_id = ?", (cur.lastrowid,)).fetchone())


@app.get("/tickets/{ticket_id}/resolution", response_model=ResolutionOut)
def get_resolution(ticket_id: int, db=Depends(get_db)):
    fetch_ticket(db, ticket_id)
    row = db.execute("SELECT * FROM resolutions WHERE ticket_id = ? ORDER BY resolution_id DESC LIMIT 1",
                     (ticket_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="This ticket has not been resolved yet")
    return dict(row)


@app.get("/tickets/{ticket_id}/similar", response_model=list[SimilarOut])
def similar_tickets(ticket_id: int, k: int = 3, db=Depends(get_db), pipeline=Depends(get_pipeline)):
    ticket = fetch_ticket(db, ticket_id)
    if not 1 <= k <= 10:
        raise HTTPException(status_code=400, detail="k must be between 1 and 10")
    try:
        return pipeline.similar(ticket["query"], k=k)
    except Exception:
        log.exception("similar-ticket search failed for ticket %s", ticket_id)
        raise HTTPException(status_code=502, detail="The similar-ticket search failed. Try again later.")