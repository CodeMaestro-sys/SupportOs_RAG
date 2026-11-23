import json
import re

VERIFY_SYSTEM = """You check a draft customer-support reply against numbered source passages.
For each numbered sentence of the draft, choose one label:
- "supported": every factual claim in the sentence is stated in the passages.
- "unsupported": the sentence states a fact, step, number, time limit or policy that the passages do not state, or it contradicts them.
- "not_factual": greetings, thanks, apologies, offers of further help, questions, or sentences that only repeat details from the customer's message.
Be strict: a claim is supported only if a passage states it. Use only the passages, never outside knowledge.
Reply with ONLY a JSON list, one object per sentence, like:
[{"id": 1, "label": "supported", "passage": 2}, {"id": 2, "label": "not_factual", "passage": null}]
Use "passage": null unless the label is "supported"."""

LABELS = {"supported", "unsupported", "not_factual"}
NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
CONTACT = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+|www\.[\w.-]+")


def split_sentences(text):
    units = []
    for line in text.splitlines():
        line = re.sub(r"^\s*(?:\d+\.|[-*•])\s+", "", line).strip()      # drop list markers
        if not line:
            continue
        units.extend(p.strip() for p in re.split(r"(?<=[.!?])\s+(?=[A-Z*])", line) if p.strip())
    return units


def parse_labels(raw, n):
    raw = re.sub(r"^```(?:json)?|```$", "", raw.strip(), flags=re.M).strip()
    try:
        items = json.loads(raw[raw.index("["): raw.rindex("]") + 1])
        return {int(x["id"]): x["label"] for x in items if x.get("label") in LABELS}
    except (ValueError, KeyError, TypeError):
        return {}                                                      # caller marks these "unparsed"


def rule_check(sentence, passages_text, customer_text):
    """Numbers and contact details that appear nowhere in the passages or the customer message."""
    source = (passages_text + " " + customer_text).lower()
    s = re.sub(r"\[\d+\]", "", sentence)                               # ignore citation numbers
    found = NUM.findall(s) + CONTACT.findall(s)
    return [t for t in found if t.lower().rstrip(".,") not in source]


def verify(llm, draft_out, customer_message):
    text = draft_out["draft"]
    if draft_out["abstained"] or not text or (not draft_out["cited"] and "?" in text):
        return []                                                      # nothing factual to check
    sentences = split_sentences(text)
    passages = draft_out["passages"]
    p_block = "\n\n".join(f"[{i}] {t}" for i, (_d, t, _s) in enumerate(passages, 1))
    s_block = "\n".join(f"{i}. {s}" for i, s in enumerate(sentences, 1))
    prompt = (f"Passages:\n{p_block}\n\nCustomer message:\n{customer_message}\n\n"
              f"Draft sentences:\n{s_block}")
    labels = parse_labels(llm.generate(prompt, system=VERIFY_SYSTEM), len(sentences))
    passages_text = " ".join(t for _d, t, _s in passages)
    return [{"id": i, "sentence": s, "llm_label": labels.get(i, "unparsed"),
             "bad_tokens": rule_check(s, passages_text, customer_message)}
            for i, s in enumerate(sentences, 1)]

def strict_rule_flags(sentence, passages, customer):
    """Numbers, emails and web addresses that appear nowhere in the passages or the customer message.
    Whole-token matching (a '2' does not match inside '12'). passages: list of (doc_id, text, score)."""
    source = (" ".join(p[1] for p in passages) + " " + customer).lower()
    s = re.sub(r"\[\d+\]", "", sentence)
    bad = []
    for tok in NUM.findall(s) + CONTACT.findall(s):
        t = tok.lower().rstrip(".,")
        if not re.search(r"(?<![\d,.])" + re.escape(t) + r"(?!\d|,\d|\.\d)", source):
            bad.append(tok)
    return bad