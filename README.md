# Rate Limiter 

A FastAPI project implementing different rate limiting algorithms, including an in-memory limiter and a Redis-backed distributed sliding window counter.

This project was built to understand how rate limiting works, how different algorithms compare, and how rate limiting can be shared across multiple servers using Redis.

## Features

- FastAPI web server
- Unlimited test endpoint
- Limited endpoint with rate limiting
- Token Bucket rate limiter
- Fixed Window Counter rate limiter
- Sliding Window Log rate limiter
- Sliding Window Counter rate limiter
- Redis-backed Sliding Window Counter for distributed rate limiting
- Supports testing across multiple server instances

## Tech Stack

- Python
- FastAPI
- Uvicorn
- Redis
- Docker
