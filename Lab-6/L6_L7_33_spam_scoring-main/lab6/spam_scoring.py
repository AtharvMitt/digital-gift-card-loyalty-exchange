SPAM_WORDS = {"free", "winner", "prize", "urgent", "cash"}


def score_message(text, sender_known, link_count):
    score = 0
    for word in text.split():
        if word.lower().strip("!.,") in SPAM_WORDS:
            score += 2
        elif word.isupper() and len(word) > 3:
            score += 1
    if link_count > 3:
        score += 4
    elif link_count > 0:
        score += 1
    if sender_known:
        score -= 3
        if score < 0:
            score = 0
    return score


def classify(score):
    if score >= 8:
        return "spam"
    if score >= 4:
        return "suspicious"
    return "clean"


def filter_inbox(messages):
    counts = {"spam": 0, "suspicious": 0, "clean": 0}
    for text, known, links in messages:
        label = classify(score_message(text, known, links))
        counts[label] += 1
    return counts


def inbox_status(counts):
    total = sum(counts.values())
    if total == 0:
        return "empty"
    ratio = counts["spam"] / total
    if ratio > 0.5:
        return "flooded"
    if ratio > 0.2:
        return "noisy"
    return "healthy"
