"""Fuzz all three functions, then check their documented behaviour."""

import math
import re
import string

import pytest
from hypothesis import given, settings, strategies as st

from spam_scoring import first_link, sender_domain, shout_ratio


# Reproducible runs, including shrinking, without an external example database.
settings.register_profile(
    "lab7", max_examples=300, derandomize=True,
    database=None, report_multiple_bugs=False, deadline=None,
)
settings.load_profile("lab7")

INPUTS = st.one_of(
    st.text(), st.none(), st.booleans(), st.integers(), st.floats(),
    st.binary(), st.lists(st.integers(), max_size=10),
    st.dictionaries(st.text(max_size=10), st.integers(), max_size=5),
)


@given(INPUTS)
def test_sender_domain_no_crash(value):
    result = sender_domain(value)
    assert isinstance(result, str)
    assert result == result.lower()


@given(INPUTS)
def test_first_link_no_crash(value):
    result = first_link(value)
    assert isinstance(result, str)
    if result:
        assert isinstance(value, str)
        assert result in value
        assert result.lower().startswith(("http://", "https://"))
        assert not any(char.isspace() for char in result)


@given(INPUTS)
def test_shout_ratio_no_crash(value):
    result = shout_ratio(value)
    assert isinstance(result, float)
    assert math.isfinite(result)
    assert 0.0 <= result <= 1.0


LABEL = st.text(alphabet=string.ascii_letters, min_size=1, max_size=20)


@given(local=LABEL, domain=LABEL, suffix=LABEL)
def test_sender_domain_valid_addresses(local, domain, suffix):
    assert sender_domain(f"  {local}@{domain}.{suffix}  ") == (
        f"{domain}.{suffix}".lower()
    )


@given(st.text().filter(lambda value: "@" not in value))
def test_sender_domain_missing_separator(value):
    assert sender_domain(value) == ""


@given(host=LABEL, scheme=st.sampled_from(["http", "https", "HTTP", "HTTPS"]),
       separator=st.sampled_from([" ", "\t", "\n", "\r\n"]))
def test_first_link_extracts_first_url(host, scheme, separator):
    url = f"{scheme}://{host}.example/path?q=1"
    assert first_link(f"Visit {url}{separator}https://second.example") == url


@given(st.text().filter(lambda value: not re.search(r"https?://", value, re.I)))
def test_first_link_without_scheme(value):
    assert first_link(value) == ""


@given(st.text())
def test_shout_ratio_matches_unicode_definition(value):
    total = sum(char.isalpha() for char in value)
    uppercase = sum(char.isalpha() and char.isupper() for char in value)
    expected = uppercase / total if total else 0.0
    assert shout_ratio(value) == expected


@given(st.text(alphabet=string.digits + string.punctuation + string.whitespace))
def test_shout_ratio_no_letters(value):
    assert shout_ratio(value) == 0.0


@pytest.mark.parametrize("value, expected", [
    ("offers@Deals.com", "deals.com"), ("a@localhost", "localhost"),
    ("", ""), (None, ""), (42, ""), ("missing-at", ""),
    ("@example.com", ""), ("a@", ""), ("a@@example.com", ""),
    ("a b@example.com", ""), ("a@exa mple.com", ""),
    ("a@/bad", ""), ("a@.example.com", ""),
    ("a@-example.com", ""), ("a@example..com", ""),
    ("a\x00@example.com", ""), ("a@example.com/path", ""),
])
def test_sender_domain_regressions(value, expected):
    assert sender_domain(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("See https://example.com", "https://example.com"),
    ("http://first.example\nhttps://second.example", "http://first.example"),
    ("Go HTTPS://Example.com\tnow", "HTTPS://Example.com"),
    ("http is a protocol", ""), ("http://", ""), ("https://   ", ""),
    ("xhttp://bad.example", ""), ("https:///bad", ""),
    ("https://?q=1", ""), ("https://#section", ""),
    ("https:// https://valid.example", "https://valid.example"),
    ("", ""), (None, ""), (123, ""),
])
def test_first_link_regressions(value, expected):
    assert first_link(value) == expected


@pytest.mark.parametrize("value, expected", [
    ("FREE prize NOW", 7 / 12), ("abc", 0.0), ("ABC", 1.0),
    ("123 !!!", 0.0), ("", 0.0), (None, 0.0), ([], 0.0),
    ("ÉéΩω", 0.5), ("中文", 0.0),
])
def test_shout_ratio_regressions(value, expected):
    assert shout_ratio(value) == expected
