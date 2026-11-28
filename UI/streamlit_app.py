"""Agent review screen.  Start the API first, then from the project root run:
    python -m streamlit run ui/streamlit_app.py
"""
import html
import re
import sys
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parent))
import api_client as api

STATUS_ICON = {"open": "🟠", "in_review": "🟡", "resolved": "🟢"}
SENTENCE_STYLE = {                       # background, border, caption
    "supported": ("#e6f4ea", "#137333", "supported by the evidence"),
    "unsupported": ("#fce8e6", "#c5221f", "NOT supported by the evidence, check before sending"),
    "not_factual": ("#f1f3f4", "#9aa0a6", "general sentence"),
}

st.set_page_config(page_title="SupportOps", page_icon="🎧", layout="wide")


# ----------------------------------------------------------------------------- helpers
def to_html(text):
    """Escape the text, then turn **bold** markers into bold tags."""
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(text))


def render_sentence(sentence):
    background, border, caption = SENTENCE_STYLE.get(sentence["label"], SENTENCE_STYLE["not_factual"])
    flags = ""
    if sentence["rule_flags"]:
        found = ", ".join(html.escape(f) for f in sentence["rule_flags"])
        flags = f"<br><span style='color:#c5221f;font-size:0.85em'>⚠ not found in the evidence: {found}</span>"
    st.markdown(
        f"<div style='background:{background};border-left:5px solid {border};padding:8px 12px;"
        f"margin:6px 0;border-radius:4px;color:#202124'>{to_html(sentence['text'])}"
        f"<br><span style='color:#5f6368;font-size:0.8em'>{caption}</span>{flags}</div>",
        unsafe_allow_html=True)


def decide_action(draft, text, discarded):
    base = ((draft or {}).get("reply_text") or "").strip()
    if not base or discarded:
        return "rejected"
    return "accepted" if text.strip() == base else "edited"


def show_error(e):
    st.error(e.detail if isinstance(e, api.ApiError) else str(e))


# ----------------------------------------------------------------------------- sidebar
if "pending_select" in st.session_state:                       # set after creating a ticket
    st.session_state["selected_ticket"] = st.session_state.pop("pending_select")

with st.sidebar:
    st.title("SupportOps")
    st.caption("Evidence-backed replies for support agents")

    with st.form("new_ticket", clear_on_submit=True):
        new_query = st.text_area("New customer message", height=90, placeholder="I want to cancel my order ORD-12345")
        if st.form_submit_button("Create ticket"):
            try:
                created = api.create_ticket(new_query)
                st.session_state["pending_select"] = created["ticket_id"]
                st.rerun()
            except api.ApiError as e:
                show_error(e)

    status_filter = st.selectbox("Show", ["all", "open", "in_review", "resolved"])
    try:
        tickets = api.list_tickets(None if status_filter == "all" else status_filter)
    except api.ApiError as e:
        show_error(e)
        st.stop()

    by_id = {t["ticket_id"]: t for t in tickets}
    ids = sorted(by_id, reverse=True)
    if st.session_state.get("selected_ticket") not in by_id:
        st.session_state.pop("selected_ticket", None)
    selected = st.selectbox(
        "Ticket", ids, key="selected_ticket",
        format_func=lambda i: f"{STATUS_ICON[by_id[i]['status']]} #{i}  {by_id[i]['query'][:38]}") if ids else None

# ----------------------------------------------------------------------------- main panel
if selected is None:
    st.info("No tickets here yet. Create one in the sidebar.")
    st.stop()

ticket = by_id[selected]
st.subheader(f"Ticket #{ticket['ticket_id']}  {STATUS_ICON[ticket['status']]} {ticket['status'].replace('_', ' ')}")
st.caption(f"Created {ticket['created_at']}")
st.markdown("**Customer message**")
st.info(ticket["query"])

try:
    draft = api.latest_draft(selected)
    resolution = api.get_resolution(selected) if ticket["status"] == "resolved" else None
except api.ApiError as e:
    show_error(e)
    st.stop()

if resolution:
    st.success(f"Resolved: reply {resolution['agent_action']}.")
    if resolution["similarity"] is not None:
        st.caption(f"Similarity between the draft and the sent reply: {resolution['similarity']:.0%}")
    st.markdown("**Reply sent**")
    st.write(resolution["final_text"])
    st.stop()

if draft is None:
    st.write("No draft yet.")
    if st.button("Generate draft", type="primary"):
        with st.spinner("Finding evidence, drafting and checking every sentence. The first request can take up to a minute."):
            try:
                api.create_draft(selected)
            except api.ApiError as e:
                show_error(e)
                st.stop()
        st.rerun()
    st.stop()

# ---- a draft exists: show it with its evidence
outcome = draft["outcome"]
if outcome == "answered":
    st.success("Draft ready.")
elif outcome == "clarify":
    st.info("The message is unclear, so the assistant suggests asking the customer a question.")
else:
    st.warning("The evidence does not cover this question. Write the reply yourself.")
st.caption(f"Drafted by {draft['model']}, checked by {draft['verifier_model']}, prompt {draft['prompt_version']}")

sentences = draft["sentences"]
needs_check = any(s["label"] == "unsupported" or s["rule_flags"] for s in sentences)
if sentences:
    unsupported = sum(s["label"] == "unsupported" for s in sentences)
    if unsupported:
        st.error(f"{unsupported} sentence(s) are not supported by the evidence.")
    elif needs_check:
        st.warning("A number or contact detail was not found in the evidence. Check the flagged sentences.")
    else:
        st.success("Every factual sentence is backed by the evidence.")
    for s in sentences:
        render_sentence(s)

left, right = st.columns([3, 2])
# The reply box is drawn first, so a slow 'similar tickets' request can never hide it.
with left:
    st.markdown("**Reply to send**")
    text = st.text_area("Edit the reply if needed", value=draft["reply_text"], height=230,
                        key=f"reply_{draft['draft_id']}", label_visibility="collapsed")
    discarded = False
    if draft["reply_text"].strip():
        discarded = st.checkbox("I discarded the draft and wrote my own reply", key=f"discard_{draft['draft_id']}")
    action = decide_action(draft, text, discarded)

    confirmed = True
    if action == "accepted" and needs_check:
        confirmed = st.checkbox("I have checked the flagged sentences against the evidence",
                                key=f"confirm_{draft['draft_id']}")

    can_send = bool(text.strip()) and confirmed
    label = {"accepted": "Send as drafted", "edited": "Send edited reply", "rejected": "Send my own reply"}[action]
    if st.button(label, type="primary", disabled=not can_send):
        try:
            api.resolve(selected, action, final_text=text, draft_id=draft["draft_id"])
        except api.ApiError as e:
            show_error(e)
            st.stop()
        st.rerun()

    if st.button("Generate a new draft"):
        with st.spinner("Drafting again..."):
            try:
                api.create_draft(selected)
            except api.ApiError as e:
                show_error(e)
                st.stop()
        st.rerun()

with right:
    st.markdown("**Evidence used**")
    for i, p in enumerate(draft["passages"], 1):
        with st.expander(f"[{i}] {p['doc_id']}  (match {p['score']:.2f})", expanded=False):
            st.markdown(p["text"])

    try:
        similar = api.similar_tickets(selected)
    except api.ApiError:
        similar = None                                 # context only: never block the agent because of it
        st.caption("Similar resolved tickets are not available right now.")
    if similar:
        st.markdown("**Similar resolved tickets**")
        st.caption("For context only. The draft is built from the policy documents, not from these replies.")
        for m in similar:
            with st.expander(f"#{m['ticket_id']}  {m['query'][:42]}  (match {m['score']:.2f})", expanded=False):
                st.markdown("**Customer:** " + m["query"])
                st.markdown("**Agent replied:** " + m["response"])