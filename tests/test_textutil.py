import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from textutil import to_customer_text


def test_citations_and_bold_marks_are_removed():
    raw = ("You can cancel an order before it is dispatched [1]. Open **My Orders** and click **Cancel Order** [1][2]. "
           "Call +91 00000 00000 (Monday to Friday, 9 AM to 6 PM) [3].")
    assert to_customer_text(raw) == ("You can cancel an order before it is dispatched. Open My Orders and click Cancel Order. "
                                     "Call +91 00000 00000 (Monday to Friday, 9 AM to 6 PM).")


def test_list_lines_and_plain_text_are_kept():
    raw = "Steps:\n1. Sign in [1].\n2. Click **Save** [2]."
    assert to_customer_text(raw) == "Steps:\n1. Sign in.\n2. Click Save."
    assert to_customer_text("Hello!") == "Hello!"
    assert to_customer_text("") == ""