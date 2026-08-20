"""After a successful sync, invalidate the user's cached reads so the next read is fresh."""
from __future__ import annotations

import asyncpg

from ..cache.redis_client import accounts_key, get_redis


async def invalidate_link(pool: asyncpg.Pool, link_id: int) -> None:
    """Coarse invalidation: drop the owning user's account cache after a write.

    MVP keeps it simple — blow away the whole user's accounts key rather than
    surgically patching individual entries.
    """
    user_id = await pool.fetchval("SELECT user_id FROM links WHERE id = $1", link_id)
    if user_id is None:
        return
    await get_redis().delete(accounts_key(user_id))
