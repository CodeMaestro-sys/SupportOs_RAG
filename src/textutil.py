"""Text helpers shared by the API and the tests."""
import re


def to_customer_text(draft_text):
    """The draft as the customer should read it: no [1] citation markers and no **bold** marks.
    The raw draft (with citations) is kept for the evidence view and the sentence checks."""
    text = re.sub(r"\s*\[\d+\](?:\s*\[\d+\])*", "", draft_text)      # ' [1]' and ' [2][3]'
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()