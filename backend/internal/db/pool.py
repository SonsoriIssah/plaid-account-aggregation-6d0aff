"""A lazily-initialized asyncpg connection pool shared across the process."""
from __future__ import annotations

import os

import asyncpg

_pool: asyncpg.Pool | None = None


async def init_pool() -> None:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(
            dsn=os.environ.get("DATABASE_URL", "postgres://localhost/aggregation"),
            min_size=2,
            max_size=10,
        )


def get_pool() -> asyncpg.Pool:
    if _pool is None:
        raise RuntimeError("pool not initialized — call init_pool() at startup")
    return _pool
