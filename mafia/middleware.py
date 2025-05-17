from loguru import logger
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

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
        if self.redis_client.is_rate_limited(ip):
            logger.warning(f"Rate limit exceeded for IP: {ip}")
            return self._block_request("Rate limit exceeded")

        # Security Payload Filter
        if request.query_params:
            for value in request.query_params.values():
                if self.security_filter.is_malicious(value):
                    logger.warning(f"Malicious payload detected from IP: {ip}")
                    return self._block_request("Malicious payload detected")

        # Brute Force Detection
        attempt_count = self.redis_client.increment_attempt(ip)
        avg_interval = self.redis_client.get_avg_interval(ip)  # ✅ Get average interval

        risk_score = self.brute_force_ai.predict(attempt_count, avg_interval)

        logger.info(f"[MAFIA] Risk Score for IP {ip}: {risk_score}")
        if risk_score > 0.8:
            logger.warning(f"Brute force detected for IP: {ip}")
            return self._block_request("Brute force attempt detected")

        response = await call_next(request)
        return response

    def _block_request(self, reason: str):
        return JSONResponse(
            status_code=403,
            content={"status": "blocked", "reason": reason}
        )
