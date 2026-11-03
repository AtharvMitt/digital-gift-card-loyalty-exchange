"""Default pytest entry point for the line coverage stage."""

from CodeCoverageTest_PES1UG24CS091_spam_scoring import (
    test_classification,
    test_inbox_counts_all_three_labels,
    test_inbox_status,
    test_known_sender_score_is_clamped_at_zero,
    test_plain_message_scores_zero,
    test_some_links_add_one,
    test_spam_words_and_uppercase_with_many_links,
)
