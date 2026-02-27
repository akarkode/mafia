import time
import redis.asyncio as aioredis


class RedisClient:
    def __init__(self, redis_url: str):
        self.client = aioredis.Redis.from_url(redis_url, decode_responses=True)

    async def is_rate_limited(self, ip: str, limit: int = 10, window: int = 60) -> bool:
        key = f"rate:{ip}"
        count = await self.client.incr(key)
        if count == 1:
            await self.client.expire(key, window)
        return count > limit

    async def increment_attempt(self, ip: str) -> int:
        key = f"brute:{ip}:count"
        time_key = f"brute:{ip}:time"
        attempts = await self.client.incr(key)

        if attempts == 1:
            await self.client.expire(key, 300)
            await self.client.set(time_key, time.time())
        return attempts

    async def get_avg_interval(self, ip: str) -> float:
        key = f"brute:{ip}:count"
        time_key = f"brute:{ip}:time"
        attempts = int(await self.client.get(key) or 1)
        first_attempt_time = float(await self.client.get(time_key) or time.time())
        elapsed_time = max(time.time() - first_attempt_time, 1)
        avg_interval = elapsed_time / attempts
        return round(avg_interval, 2)
