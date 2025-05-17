import time
import redis


class RedisClient:
    def __init__(self, redis_url: str):
        self.client = redis.Redis.from_url(redis_url)

    def is_rate_limited(self, ip: str, limit: int = 10, window: int = 60) -> bool:
        key = f"rate:{ip}"
        count = self.client.incr(key)
        if count == 1:
            self.client.expire(key, window)
        return count > limit

    def increment_attempt(self, ip: str) -> int:
        key = f"brute:{ip}:count"
        time_key = f"brute:{ip}:time"
        attempts = self.client.incr(key)

        if attempts == 1:
            self.client.expire(key, 300)
            self.client.set(time_key, time.time())
        return attempts

    def get_avg_interval(self, ip: str) -> float:
        key = f"brute:{ip}:count"
        time_key = f"brute:{ip}:time"
        attempts = int(self.client.get(key) or 1)
        first_attempt_time = float(self.client.get(time_key) or time.time())
        elapsed_time = max(time.time() - first_attempt_time, 1)
        avg_interval = elapsed_time / attempts
        return round(avg_interval, 2)
