"""Stage 1: exercise every executable line of the supplied application."""

import pytest

from spam_scoring import classify, filter_inbox, inbox_status, score_message


def test_plain_message_scores_zero():
    assert score_message("hello there", False, 0) == 0


def test_spam_words_and_uppercase_with_many_links():
    assert score_message("FREE! winner, HELLO", False, 4) == 9


def test_some_links_add_one():
    assert score_message("hello", False, 1) == 1


def test_known_sender_score_is_clamped_at_zero():
    assert score_message("hello", True, 0) == 0


@pytest.mark.parametrize("score, expected", [(1, "clean"), (4, "suspicious"), (8, "spam")])
def test_classification(score, expected):
    assert classify(score) == expected


def test_inbox_counts_all_three_labels():
    messages = [("hello", False, 0), ("free cash", False, 0), ("free cash", False, 4)]
    assert filter_inbox(messages) == {"spam": 1, "suspicious": 1, "clean": 1}


@pytest.mark.parametrize(
    "counts, expected",
    [
        ({"spam": 0, "suspicious": 0, "clean": 0}, "empty"),
        ({"spam": 3, "suspicious": 0, "clean": 1}, "flooded"),
        ({"spam": 1, "suspicious": 1, "clean": 1}, "noisy"),
        ({"spam": 0, "suspicious": 1, "clean": 3}, "healthy"),
    ],
)
def test_inbox_status(counts, expected):
    assert inbox_status(counts) == expected
