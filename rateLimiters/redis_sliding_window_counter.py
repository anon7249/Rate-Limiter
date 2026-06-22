import time
from redis.asyncio import Redis


class RedisSlidingWindowCounter:
    def __init__(self, redis: Redis, window_size: int, max_requests: int):
        self.redis = redis
        self.window_size = window_size
        self.max_requests = max_requests

    async def is_allowed(self, client_id: str) -> bool:
        now = int(time.time())
        current_window = now - (now % self.window_size)
        previous_window = current_window - self.window_size

        current_key = f"rate_limit:{client_id}:{current_window}"
        previous_key = f"rate_limit:{client_id}:{previous_window}"

        current_count = await self.redis.get(current_key)
        previous_count = await self.redis.get(previous_key)

        current_count = int(current_count) if current_count else 0
        previous_count = int(previous_count) if previous_count else 0

        time_into_current_window = now - current_window
        time_remaining = self.window_size - time_into_current_window

        previous_window_weight = time_remaining / self.window_size

        estimated_count = previous_count * previous_window_weight + current_count

        if estimated_count >= self.max_requests:
            return False

        await self.redis.incr(current_key)
        await self.redis.expire(current_key, self.window_size * 2)

        return True
