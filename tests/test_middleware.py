"""Integration tests for BruteForceMiddleware — rate limiting, payload inspection, brute force."""
import json
import pytest
from unittest.mock import AsyncMock, MagicMock


# ── Helpers ───────────────────────────────────────────────────────────────────

def _mock_redis(*, rate_limited=False, attempts=1, avg_interval=5.0):
    m = MagicMock()
    m.is_rate_limited = AsyncMock(return_value=rate_limited)
    m.increment_attempt = AsyncMock(return_value=attempts)
    m.get_avg_interval = AsyncMock(return_value=avg_interval)
    return m


# ── Clean Request ─────────────────────────────────────────────────────────────

async def test_clean_get_request_passes(client):
    response = await client.get("/ping")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


async def test_clean_post_json_passes(client):
    response = await client.post("/login", json={"username": "alice", "password": "secret"})
    assert response.status_code == 200
    assert response.json()["user"] == "alice"


# ── Rate Limiting ─────────────────────────────────────────────────────────────

async def test_rate_limited_request_blocked(mock_redis, app):
    mock_redis.is_rate_limited = AsyncMock(return_value=True)

    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/ping")

    assert response.status_code == 403
    assert response.json()["reason"] == "Rate limit exceeded"


# ── Query Param Payload Inspection ───────────────────────────────────────────

async def test_xss_in_query_param_blocked(client):
    response = await client.get("/ping", params={"q": "<script>alert(1)</script>"})
    assert response.status_code == 403
    assert "Malicious" in response.json()["reason"]


async def test_sqli_in_query_param_blocked(client):
    response = await client.get("/ping", params={"search": "' UNION SELECT * FROM users --"})
    assert response.status_code == 403
    assert "Malicious" in response.json()["reason"]


async def test_clean_query_param_passes(client):
    response = await client.get("/ping", params={"q": "hello world"})
    assert response.status_code == 200


# ── Request Body Payload Inspection ──────────────────────────────────────────

async def test_xss_in_json_body_blocked(client):
    response = await client.post(
        "/login",
        content=json.dumps({"username": "<script>alert(1)</script>"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 403
    assert "Malicious" in response.json()["reason"]


async def test_sqli_in_json_body_blocked(client):
    response = await client.post(
        "/login",
        content=json.dumps({"username": "admin' --", "password": "' OR 1=1--"}),
        headers={"Content-Type": "application/json"},
    )
    assert response.status_code == 403
    assert "Malicious" in response.json()["reason"]


async def test_sqli_in_form_body_blocked(client):
    response = await client.post(
        "/login",
        content="username=admin'--&password=secret",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 403
    assert "Malicious" in response.json()["reason"]


async def test_clean_json_body_passes(client):
    response = await client.post("/login", json={"username": "bob", "password": "p@ssw0rd"})
    assert response.status_code == 200


async def test_clean_put_json_body_passes(client):
    response = await client.put("/update", json={"field": "value"})
    assert response.status_code == 200


async def test_body_readable_by_downstream_after_inspection(client):
    """Ensure downstream route can still read body after middleware inspected it."""
    payload = {"username": "charlie", "password": "safe_pass"}
    response = await client.post("/login", json=payload)
    assert response.status_code == 200
    assert response.json()["user"] == "charlie"


# ── Brute Force Detection ─────────────────────────────────────────────────────

async def test_brute_force_high_risk_blocked(mock_redis, mock_detector, app):
    mock_redis.increment_attempt = AsyncMock(return_value=100)
    mock_redis.get_avg_interval = AsyncMock(return_value=0.2)
    mock_detector.predict = MagicMock(return_value=0.95)  # force high risk score

    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json={"username": "hacker"})

    assert response.status_code == 403
    assert response.json()["reason"] == "Brute force attempt detected"


async def test_normal_behavior_passes(mock_redis, mock_detector, app):
    mock_redis.increment_attempt = AsyncMock(return_value=2)
    mock_redis.get_avg_interval = AsyncMock(return_value=5.0)
    mock_detector.predict = MagicMock(return_value=0.1)  # safe risk score

    from httpx import AsyncClient, ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/login", json={"username": "normal_user"})

    assert response.status_code == 200
