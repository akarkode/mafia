"""Shared fixtures for MAFIA test suite."""
import pytest
from unittest.mock import AsyncMock, MagicMock

from fastapi import FastAPI, Request
from httpx import AsyncClient, ASGITransport

from mafia.middleware import BruteForceMiddleware


def build_test_app() -> FastAPI:
    """Minimal FastAPI app wrapped with MAFIA middleware."""
    app = FastAPI()
    app.add_middleware(BruteForceMiddleware, redis_url="redis://localhost:6379")

    @app.get("/ping")
    def ping():
        return {"status": "ok"}

    @app.post("/login")
    async def login(request: Request):
        body = await request.json()
        return {"status": "ok", "user": body.get("username")}

    @app.put("/update")
    async def update(request: Request):
        body = await request.json()
        return {"status": "ok", "data": body}

    return app


@pytest.fixture
def mock_redis():
    """AsyncMock for RedisClient that simulates a clean (non-limited) state."""
    m = MagicMock()
    m.is_rate_limited = AsyncMock(return_value=False)
    m.increment_attempt = AsyncMock(return_value=1)
    m.get_avg_interval = AsyncMock(return_value=5.0)
    return m


@pytest.fixture
def mock_detector():
    """Mock for BruteForceDetector returning a safe risk score by default."""
    m = MagicMock()
    m.predict = MagicMock(return_value=0.1)
    return m


@pytest.fixture
def app(mock_redis, mock_detector, monkeypatch):
    """Test app with Redis and AI detector patched out."""
    monkeypatch.setattr("mafia.middleware.RedisClient", lambda url: mock_redis)
    monkeypatch.setattr("mafia.middleware.BruteForceDetector", lambda: mock_detector)
    return build_test_app()


@pytest.fixture
async def client(app):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
