import time


class WindowCounterRateLimiter:
    def __init__(self, window_size: int, window_limit: int):

        self.window_size = window_size
        self.window_limit = window_limit
        self.fixed_window_buckets = {}

    def is_allowed(self, ip_address: str) -> bool:
        now = int(time.time())
        current_window = now - (now % self.window_size)

        key = f"{ip_address}:{current_window}"

        if key not in self.fixed_window_buckets:
            self.fixed_window_buckets[key] = 0

        self.fixed_window_buckets[key] += 1

        if self.fixed_window_buckets[key] > self.window_limit:
            return False

        return True
