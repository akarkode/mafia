"""Tests for SecurityFilter — XSS, SQLi, and clean payload detection."""
import pytest
from mafia.security import SecurityFilter


@pytest.fixture(scope="module")
def sf():
    return SecurityFilter()


# ── XSS ──────────────────────────────────────────────────────────────────────

def test_xss_script_tag_blocked(sf):
    assert sf.is_malicious("<script>alert(1)</script>") is True


def test_xss_onerror_blocked(sf):
    assert sf.is_malicious("<img onerror=alert(1)>") is True


def test_xss_clean_html_like_string_passes(sf):
    # plain angle brackets without script/onerror should not be flagged
    assert sf.is_malicious("<b>hello</b>") is False


# ── SQLi ──────────────────────────────────────────────────────────────────────

def test_sqli_union_select_blocked(sf):
    assert sf.is_malicious("' UNION SELECT * FROM users --") is True


def test_sqli_drop_blocked(sf):
    assert sf.is_malicious("'; DROP TABLE users;--") is True


def test_sqli_comment_blocked(sf):
    assert sf.is_malicious("admin'--") is True


# ── Clean payloads ────────────────────────────────────────────────────────────

def test_clean_username_passes(sf):
    assert sf.is_malicious("john_doe") is False


def test_clean_email_passes(sf):
    assert sf.is_malicious("user@example.com") is False


def test_empty_string_passes(sf):
    assert sf.is_malicious("") is False


def test_numeric_string_passes(sf):
    assert sf.is_malicious("123456") is False
