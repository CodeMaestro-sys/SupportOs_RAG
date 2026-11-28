import re

FLOOR = 0.0    # retrieval score floor from the abstain experiment (answerable 5th percentile)

SYSTEM = """You are a support assistant for ShopEase, an online store. You write draft replies that a human support agent will review before sending.

Rules:
1. Use ONLY the numbered passages provided. Do not use outside knowledge and do not guess.
2. Every sentence that states a fact (steps, time limits, contact details, policies) must end with the number of the passage that supports it, like [1] or [2][3].
3. If the passages do not contain the information needed to answer the customer's question, reply with exactly: NOT_ENOUGH_EVIDENCE
4. Be polite and concise, at most 120 words. Do not invent order details, dates or amounts."""


def build_prompt(query, passages):
    blocks = "\n\n".join(f"[{i}] ({doc_id}) {text}"
                         for i, (doc_id, text, _score) in enumerate(passages, 1))
    return f"Passages:\n{blocks}\n\nCustomer message:\n{query}\n\nDraft reply:"


def draft(llm, retriever, query, k=4, floor=FLOOR, system=SYSTEM, extra_passages=None):
    passages = retriever.search_chunks(query, k=k) + list(extra_passages or [])
    if passages[0][2] < floor:                       # evidence is clearly unrelated: skip the LLM call
        return {"query": query, "passages": passages, "draft": "", "abstained": True,
                "reason": "low_retrieval_score", "cited": []}
    raw = llm.generate(build_prompt(query, passages), system=system).strip()
    abstained = raw.startswith("NOT_ENOUGH_EVIDENCE")
    cited = sorted({int(n) for n in re.findall(r"\[(\d+)\]", raw) if 1 <= int(n) <= len(passages)})
    return {"query": query, "passages": passages, "draft": raw, "abstained": abstained,
            "reason": "model_judgement" if abstained else "", "cited": cited}


SYSTEM_B = SYSTEM.replace(
    "3. If the passages do not contain the information needed to answer the customer's question, reply with exactly: NOT_ENOUGH_EVIDENCE",
    "3. If the passages are about a different topic from the customer's request, reply with exactly: NOT_ENOUGH_EVIDENCE. "
    "If the request is short or unclear but the passages cover its most likely meaning, answer for that meaning. "
    "If the passages cover only part of the request, answer that part and say that customer support can help with the rest. "
    "Never fill any gap with outside knowledge."
)
assert SYSTEM_B != SYSTEM

SYSTEM_C = SYSTEM_B + (" 5. If the message is too vague, or could mean more than one thing covered by the passages, "
                       "ask ONE short clarifying question instead of answering or refusing. A question needs no citation.")


def outcome(o):
    if o["abstained"]:
        return "refused"
    if not o["cited"] and "?" in o["draft"]:
        return "clarify"
    return "answered"

SYSTEM_D = SYSTEM_C + (" 6. Passages whose label starts with past-ticket are earlier replies to similar customers. "
                       "If they disagree with the policy passages, follow the policy passages. "
                       "Never repeat order numbers, names or amounts from a past ticket.")