"""Tests for async RedisClient — rate limiting, attempt tracking, interval calc."""
import time
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from mafia.utils.redis_client import RedisClient


@pytest.fixture
def redis_client():
    """RedisClient with a fully mocked aioredis connection."""
    client = RedisClient.__new__(RedisClient)
    client.client = MagicMock()
    return client


# ── Rate Limiting ─────────────────────────────────────────────────────────────

async def test_rate_limit_not_exceeded(redis_client):
    redis_client.client.incr = AsyncMock(return_value=5)
    redis_client.client.expire = AsyncMock()

    result = await redis_client.is_rate_limited("1.2.3.4", limit=10)
    assert result is False


async def test_rate_limit_exceeded(redis_client):
    redis_client.client.incr = AsyncMock(return_value=11)
    redis_client.client.expire = AsyncMock()

    result = await redis_client.is_rate_limited("1.2.3.4", limit=10)
    assert result is True


async def test_rate_limit_sets_expiry_on_first_request(redis_client):
    redis_client.client.incr = AsyncMock(return_value=1)
    redis_client.client.expire = AsyncMock()

    await redis_client.is_rate_limited("1.2.3.4", limit=10, window=60)
    redis_client.client.expire.assert_called_once_with("rate:1.2.3.4", 60)


async def test_rate_limit_no_expiry_on_subsequent_requests(redis_client):
    redis_client.client.incr = AsyncMock(return_value=5)
    redis_client.client.expire = AsyncMock()

    await redis_client.is_rate_limited("1.2.3.4", limit=10)
    redis_client.client.expire.assert_not_called()


# ── Attempt Tracking ──────────────────────────────────────────────────────────

async def test_increment_attempt_returns_count(redis_client):
    redis_client.client.incr = AsyncMock(return_value=3)
    redis_client.client.expire = AsyncMock()
    redis_client.client.set = AsyncMock()

    count = await redis_client.increment_attempt("1.2.3.4")
    assert count == 3


async def test_increment_attempt_sets_expiry_on_first(redis_client):
    redis_client.client.incr = AsyncMock(return_value=1)
    redis_client.client.expire = AsyncMock()
    redis_client.client.set = AsyncMock()

    await redis_client.increment_attempt("1.2.3.4")
    redis_client.client.expire.assert_called_once_with("brute:1.2.3.4:count", 300)


# ── Average Interval ──────────────────────────────────────────────────────────

async def test_avg_interval_calculation(redis_client):
    past_time = time.time() - 10  # 10 seconds ago
    redis_client.client.get = AsyncMock(side_effect=["5", str(past_time)])

    avg = await redis_client.get_avg_interval("1.2.3.4")
    # 10s elapsed / 5 attempts ≈ 2.0s
    assert 1.5 <= avg <= 2.5


async def test_avg_interval_fallback_on_missing_data(redis_client):
    redis_client.client.get = AsyncMock(return_value=None)

    avg = await redis_client.get_avg_interval("1.2.3.4")
    # Falls back to 1 attempt, elapsed ≈ 0 → clamped to 1 → interval = 1.0
    assert avg >= 1.0
