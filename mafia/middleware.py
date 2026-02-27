from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.datastructures import Headers
from starlette.types import Scope, Receive, Send
import json

from .security import SecurityFilter
from .aimodel import BruteForceDetector
from .utils.redis_client import RedisClient

class BruteForceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis_url: str = "redis://localhost:6379"):
        super().__init__(app)
        self.redis_client = RedisClient(redis_url)
        self.brute_force_ai = BruteForceDetector()
        self.security_filter = SecurityFilter()

    async def dispatch(self, request: Request, call_next):
        ip = request.client.host
        path = request.url.path
        logger.info(f"[MAFIA] Incoming request from IP: {ip} to {path}")

        # Rate Limiting
        if await self.redis_client.is_rate_limited(ip):
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return self._block_request("Rate limit exceeded")

        # Security Payload Filter — Query Params
        if request.query_params:
            for value in request.query_params.values():
                if self.security_filter.is_malicious(value):
                    logger.warning(f"Malicious payload detected in query params from IP: {ip}")
                    return self._block_request("Malicious payload detected")

        # Security Payload Filter — Request Body (POST/PUT/PATCH)
        if request.method in ("POST", "PUT", "PATCH"):
            body_bytes = await request.body()

            # Re-inject body so downstream handlers can still read it after we consumed the stream
            async def _receive() -> dict:
                return {"type": "http.request", "body": body_bytes, "more_body": False}
            request._receive = _receive  # type: ignore[attr-defined]

            if body_bytes:
                body_values = self._extract_body_values(body_bytes, request.headers.get("content-type", ""))
                for value in body_values:
                    if self.security_filter.is_malicious(value):
                        logger.warning(f"Malicious payload detected in request body from IP: {ip}")
                        return self._block_request("Malicious payload detected")

        # Brute Force Detection
        attempt_count = await self.redis_client.increment_attempt(ip)
        avg_interval = await self.redis_client.get_avg_interval(ip)

        risk_score = self.brute_force_ai.predict(attempt_count, avg_interval)

        logger.info(f"[MAFIA] Risk Score for IP {ip}: {risk_score}")
        if risk_score > 0.8:
            logger.warning(f"Brute force detected for IP: {ip}")
            return self._block_request("Brute force attempt detected")

        response = await call_next(request)
        return response

    def _extract_body_values(self, body_bytes: bytes, content_type: str) -> list:
        """Extract string values from request body for inspection."""
        values = []
        try:
            if "application/json" in content_type:
                body = json.loads(body_bytes.decode("utf-8", errors="ignore"))
                values = self._flatten_json(body)
            elif "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
                # Decode as raw string and split by common delimiters
                raw = body_bytes.decode("utf-8", errors="ignore")
                values = [v.split("=", 1)[-1] for v in raw.split("&") if "=" in v]
            else:
                values = [body_bytes.decode("utf-8", errors="ignore")]
        except Exception:
            pass
        return values

    def _flatten_json(self, obj, values=None) -> list:
        """Recursively extract all string values from a JSON object."""
        if values is None:
            values = []
        if isinstance(obj, dict):
            for v in obj.values():
                self._flatten_json(v, values)
        elif isinstance(obj, list):
            for item in obj:
                self._flatten_json(item, values)
        elif isinstance(obj, str):
            values.append(obj)
        return values

    def _block_request(self, reason: str):
        return JSONResponse(
            status_code=403,
            content={"status": "blocked", "reason": reason}
        )
