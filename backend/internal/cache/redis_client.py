"""A thin Redis wrapper with a version prefix for global invalidation."""
from __future__ import annotations

import os

import redis.asyncio as redis

# Bumping this prefix invalidates *every* key at once — useful on schema changes.
CACHE_VERSION = "v1"

_client: redis.Redis | None = None


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(
            os.environ.get("REDIS_URL", "redis://localhost:6379"),
            decode_responses=True,
        )
    return _client


def accounts_key(user_id: int) -> str:
    return f"{CACHE_VERSION}:accounts:{user_id}"


def recent_txns_key(account_id: int) -> str:
    return f"{CACHE_VERSION}:txns:recent:{account_id}"
