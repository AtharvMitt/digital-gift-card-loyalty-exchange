"""Small spam-scoring helpers with explicit fallbacks for invalid input."""

import re


_DOMAIN = re.compile(
    r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?"
    r"(?:\.[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?)*",
    re.ASCII,
)
_LINK = re.compile(
    r"\bhttps?://[^\s/?#\x00-\x1f\x7f]+[^\s\x00-\x1f\x7f]*",
    re.IGNORECASE,
)


def sender_domain(email):
    """Return a lowercase ASCII domain, or '' for unsupported/malformed input.

    This is a practical sender-field parser, not a full RFC email validator.
    Surrounding whitespace is allowed; internal whitespace/control characters,
    empty parts, multiple @ signs and malformed domain labels are rejected.
    """
    if not isinstance(email, str):
        return ""
    email = email.strip()
    if email.count("@") != 1:
        return ""
    local, domain = email.split("@")
    if not local or len(local) > 64 or not domain or len(domain) > 253:
        return ""
    if any(char.isspace() or ord(char) < 32 or ord(char) == 127 for char in email):
        return ""
    domain = domain.lower()
    return domain if _DOMAIN.fullmatch(domain) else ""


def first_link(text):
    """Return the first HTTP(S) token with a nonempty host, or ''.

    Match schemes case-insensitively and stop at any whitespace/control byte.
    The original spelling is preserved. This extracts links; it does not fetch
    them or claim that their destinations are safe or reachable.
    """
    if not isinstance(text, str):
        return ""
    match = _LINK.search(text)
    return match.group(0) if match else ""


def shout_ratio(text):
    """Return uppercase alphabetic characters / all letters, or 0.0.

    Unicode isalpha/isupper semantics are preserved. Non-string values and
    strings without letters have a neutral score and never divide by zero.
    """
    if not isinstance(text, str):
        return 0.0
    total = uppercase = 0
    for char in text:
        if char.isalpha():
            total += 1
            uppercase += char.isupper()
    return uppercase / total if total else 0.0


def main():
    print("==== Running sender_domain ====")
    user_input = input("Enter a sender email (e.g. offers@Deals.com): ")
    result = sender_domain(user_input)
    print("Sender Domain:", result)

    print("\n==== Running first_link ====")
    user_input = input("Enter a message containing a link: ")
    result = first_link(user_input)
    print("First Link:", result)

    print("\n==== Running shout_ratio ====")
    user_input = input("Enter a message (e.g. FREE prize NOW): ")
    result = shout_ratio(user_input)
    print("Uppercase Ratio:", result)


if __name__ == "__main__":
    main()
