"""Thin client for the SupportOps API. The Streamlit app talks to the server only through this module."""
import os

import httpx

BASE_URL = os.getenv("SUPPORTOPS_API", "http://127.0.0.1:8000")


class ApiError(Exception):
    def __init__(self, status, detail):
        super().__init__(f"{status}: {detail}")
        self.status = status
        self.detail = detail


def _request(method, path, json=None, timeout=30.0):
    try:
        r = httpx.request(method, BASE_URL + path, json=json, timeout=timeout)
    except httpx.HTTPError as e:
        raise ApiError(0, f"Cannot reach the API at {BASE_URL}. Is the server running? ({type(e).__name__})")
    if r.status_code >= 400:
        try:
            detail = r.json().get("detail", r.text)
        except ValueError:
            detail = r.text
        raise ApiError(r.status_code, detail if isinstance(detail, str) else str(detail))
    return r.json()


def list_tickets(status=None):
    return _request("GET", "/tickets" + (f"?status={status}" if status else ""))


def create_ticket(query):
    return _request("POST", "/tickets", json={"query": query})


def create_draft(ticket_id):
    return _request("POST", f"/tickets/{ticket_id}/draft", timeout=240.0)      # the first request loads the model


def latest_draft(ticket_id):
    try:
        return _request("GET", f"/tickets/{ticket_id}/draft")
    except ApiError as e:
        if e.status == 404:
            return None
        raise


def get_resolution(ticket_id):
    try:
        return _request("GET", f"/tickets/{ticket_id}/resolution")
    except ApiError as e:
        if e.status == 404:
            return None
        raise


def resolve(ticket_id, action, final_text=None, draft_id=None):
    return _request("POST", f"/tickets/{ticket_id}/resolve",
                    json={"action": action, "final_text": final_text, "draft_id": draft_id})