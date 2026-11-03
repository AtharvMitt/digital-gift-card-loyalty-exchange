"""Stage 2: decision outcomes, thresholds, empty inputs and integration."""

import pytest

from spam_scoring import classify, filter_inbox, inbox_status, score_message


@pytest.mark.parametrize(
    "text, known, links, expected",
    [
        ("", False, 0, 0),                         # zero loop iterations
        ("   \t\n", False, 0, 0),
        ("hello there", False, 0, 0),              # ordinary words
        ("free", False, 0, 2),
        ("winner", False, 0, 2),
        ("prize", False, 0, 2),
        ("urgent", False, 0, 2),
        ("cash", False, 0, 2),
        ("FrEe! WINNER, prize. urgent cash", False, 0, 10),
        ("free free", False, 0, 4),               # count each occurrence
        ("FREE", False, 0, 2),                    # keyword precedes uppercase rule
        ("HELLO", False, 0, 1),
        ("HEY", False, 0, 0),                     # uppercase length == 3
        ("HEYA", False, 0, 1),                    # uppercase length == 4
        ("Hello", False, 0, 0),                   # not all uppercase
        ("1234", False, 0, 0),
        ("hello", False, 1, 1),                   # first positive link count
        ("hello", False, 3, 1),                   # upper end of small-link range
        ("hello", False, 4, 4),                   # first large-link count
        ("hello", True, 0, 0),                    # negative adjusted score clamps
        ("free", True, 0, 0),                     # 2 - 3 clamps
        ("FREE HELLO", True, 0, 0),               # 3 - 3: clamp is skipped
        ("free cash", True, 0, 1),                # positive score skips clamp
        ("FREE! winner, HELLO", False, 4, 9),
        ("FREE! winner, HELLO", True, 4, 6),       # sender deduction after links
    ],
)
def test_score_decisions_and_boundaries(text, known, links, expected):
    assert score_message(text, known, links) == expected


@pytest.mark.parametrize(
    "score, expected",
    [(0, "clean"), (1, "clean"), (3, "clean"), (4, "suspicious"),
     (5, "suspicious"), (7, "suspicious"), (8, "spam"), (9, "spam")],
)
def test_classification_thresholds(score, expected):
    assert classify(score) == expected


@pytest.mark.parametrize(
    "messages, expected",
    [
        ([], {"spam": 0, "suspicious": 0, "clean": 0}),
        ([("hello", False, 0)], {"spam": 0, "suspicious": 0, "clean": 1}),
        ([("free cash", False, 0)], {"spam": 0, "suspicious": 1, "clean": 0}),
        ([("free cash", False, 4)], {"spam": 1, "suspicious": 0, "clean": 0}),
        ([("hello", False, 0), ("free cash", False, 0), ("free cash", False, 4)],
         {"spam": 1, "suspicious": 1, "clean": 1}),
        ([("free cash", False, 4), ("free cash", True, 4)],
         {"spam": 1, "suspicious": 1, "clean": 0}),
    ],
)
def test_inbox_loop_and_counts(messages, expected):
    original = list(messages)
    counts = filter_inbox(messages)
    assert counts == expected
    assert sum(counts.values()) == len(messages)
    assert messages == original


@pytest.mark.parametrize(
    "counts, expected",
    [
        ({"spam": 0, "suspicious": 0, "clean": 0}, "empty"),
        ({"spam": 0, "suspicious": 0, "clean": 1}, "healthy"),
        ({"spam": 1, "suspicious": 2, "clean": 3}, "healthy"),  # below .2
        ({"spam": 1, "suspicious": 2, "clean": 2}, "healthy"),  # exactly .2
        ({"spam": 1, "suspicious": 1, "clean": 2}, "noisy"),    # above .2
        ({"spam": 2, "suspicious": 0, "clean": 3}, "noisy"),    # below .5
        ({"spam": 1, "suspicious": 0, "clean": 1}, "noisy"),    # exactly .5
        ({"spam": 3, "suspicious": 1, "clean": 1}, "flooded"),  # above .5
        ({"spam": 1, "suspicious": 0, "clean": 0}, "flooded"),
        ({"spam": 0, "suspicious": 5, "clean": 0}, "healthy"),
    ],
)
def test_status_thresholds(counts, expected):
    original = dict(counts)
    assert inbox_status(counts) == expected
    assert counts == original


def test_filter_and_status_integration():
    messages = [("free cash", False, 4)] * 3 + [("hello", True, 0)]
    assert inbox_status(filter_inbox(messages)) == "flooded"
    assert inbox_status(filter_inbox([])) == "empty"
