"""Reads accounts with a cache-aside strategy: try cache, fall back to DB, backfill."""
from __future__ import annotations

import json

import asyncpg

from ..cache.redis_client import accounts_key, get_redis

ACCOUNTS_TTL_SECONDS = 60


class AccountsService:
    def __init__(self, pool: asyncpg.Pool):
        self._pool = pool

    async def list_accounts(self, user_id: int) -> list[dict]:
        cache = get_redis()
        key = accounts_key(user_id)

        cached = await cache.get(key)
        if cached is not None:
            return json.loads(cached)  # cache hit

        # Cache miss → read from Postgres, scoped to the user via the link join.
        rows = await self._pool.fetch(
            """
            SELECT a.id, i.name AS institution, a.name AS account_name,
                   a.mask, a.currency, a.balance_minor, a.updated_at
            FROM accounts a
            JOIN links l ON l.id = a.link_id
            JOIN institutions i ON i.id = l.institution_id
            WHERE l.user_id = $1
            ORDER BY a.id
            """,
            user_id,
        )
        accounts = [
            {
                "id": r["id"],
                "institution": r["institution"],
                "account_name": r["account_name"],
                "mask": r["mask"],
                "currency": r["currency"],
                "balance": r["balance_minor"] / 100,
                "updated_at": r["updated_at"].isoformat(),
            }
            for r in rows
        ]
        # Backfill the cache with a TTL so stale data self-expires.
        await cache.set(key, json.dumps(accounts), ex=ACCOUNTS_TTL_SECONDS)
        return accounts
