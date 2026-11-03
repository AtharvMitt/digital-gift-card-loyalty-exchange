import pytest
from spam_scoring import score_message, classify, filter_inbox, inbox_status

#Example test cases:
def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0

def test_low_score_is_clean():
    assert classify(1) == "clean"

#Write the rest of the test cases so that the code is 90- 100% covered.
