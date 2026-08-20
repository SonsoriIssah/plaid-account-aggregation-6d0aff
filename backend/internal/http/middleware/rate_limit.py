"""A Redis fixed-window rate limiter, keyed per user_id."""
from __future__ import annotations

from fastapi import Request

from ...cache.redis_client import CACHE_VERSION, get_redis
from ..errors import ApiError

WINDOW_SECONDS = 60
MAX_REQUESTS = 120  # per user per window


class TooManyRequests(ApiError):
    def __init__(self) -> None:
        super().__init__(429, "rate_limited", "too many requests, slow down")


async def enforce_rate_limit(request: Request) -> None:
    """Increment a per-user counter in a fixed window; reject past the cap."""
    user_id = request.headers.get("x-user-id", "anonymous")
    key = f"{CACHE_VERSION}:ratelimit:{user_id}"
    redis = get_redis()

    count = await redis.incr(key)
    if count == 1:
        # First request in this window — set the window expiry.
        await redis.expire(key, WINDOW_SECONDS)
    if count > MAX_REQUESTS:
        raise TooManyRequests()
