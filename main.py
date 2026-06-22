from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import PlainTextResponse
import uvicorn
import time
from rateLimiters.tokenBucket import TokenBucketRateLimiter
from rateLimiters.fixedCounter import WindowCounterRateLimiter
from rateLimiters.slidingWindowLog import SlidingWindowLog

app = FastAPI(title="Rate limiter Challenge")

token_bucket_limiter = TokenBucketRateLimiter(bucket_capacity=10, refill_rate=1)
window_counter_limiter = WindowCounterRateLimiter(window_size=10, window_limit=5)
sliding_window_log_algo = SlidingWindowLog(window_size=10, max_requests=5)


@app.get("/unlimited")
async def unlimited():
    return PlainTextResponse("Unlimited, let's Go!")


@app.get("/limited")
async def limited(request: Request):
    ip_address = request.client.host

    if not sliding_window_log_algo.is_allowed(ip_address):
        raise HTTPException(status_code=429, detail="too many requests")

    return PlainTextResponse("Limited, don't overuse me!")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080)
