import time


class TokenBucketRateLimiter:
    def __init__(self, bucket_capacity: int, refill_rate: float):

        self.bucket_capacity = bucket_capacity
        self.refill_rate = refill_rate
        self.buckets = {}

    def is_allowed(self, ip_address: str) -> bool:
        now = time.time()
        if ip_address not in self.buckets:
            self.buckets[ip_address] = {
                "tokens": self.bucket_capacity,
                "last_refill": now,
            }

        bucket = self.buckets[ip_address]
        elapsed_time = now - bucket["last_refill"]

        tokens_to_add = elapsed_time * self.refill_rate
        bucket["tokens"] = min(self.bucket_capacity, bucket["tokens"] + tokens_to_add)

        bucket["last_refill"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        else:
            return False
