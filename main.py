from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
import time
from rateLimiters.tokenBucket import TokenBucketRateLimiter
from rateLimiters.fixedCounter import WindowCounterRateLimiter
from rateLimiters.slidingWindowLog import SlidingWindowLog
from rateLimiters.slidingWindowCounter import SlidingWindowCounter
from rateLimiters.redis_sliding_window_counter import RedisSlidingWindowCounter
from redis.asyncio import Redis

app = FastAPI(title="Rate limiter Challenge")


redis = Redis(host="localhost", port=6379, decode_responses=True)

rate_limiter = RedisSlidingWindowCounter(
    redis=redis,
    window_size=60,
    max_requests=60,
)

token_bucket_limiter = TokenBucketRateLimiter(bucket_capacity=10, refill_rate=1)
window_counter_limiter = WindowCounterRateLimiter(window_size=10, window_limit=5)
sliding_window_log = SlidingWindowLog(window_size=10, max_requests=5)
sliding_window_counter = SlidingWindowCounter(window_size=10, max_requests=5)


@app.get("/unlimited")
async def unlimited():
    return PlainTextResponse("Unlimited, let's Go!")


@app.get("/limited")
async def limited(request: Request):
    ip_address = request.client.host

    if not await rate_limiter.is_allowed(ip_address):
        raise HTTPException(status_code=429, detail="too many requests")

    return PlainTextResponse("Limited, don't overuse me!")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
