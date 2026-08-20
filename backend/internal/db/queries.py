"""Thin typed query helpers over an asyncpg pool. No ORM — explicit SQL."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

import asyncpg


@dataclass
class Link:
    id: int
    user_id: int
    institution_id: int
    status: str
    sync_cursor: Optional[str]


async def get_link(pool: asyncpg.Pool, link_id: int, user_id: int) -> Optional[Link]:
    """Fetch a link, scoped to its owner so one user can't read another's link."""
    row = await pool.fetchrow(
        """
        SELECT id, user_id, institution_id, status, sync_cursor
        FROM links
        WHERE id = $1 AND user_id = $2
        """,
        link_id,
        user_id,
    )
    return Link(**row) if row else None


async def upsert_transaction(
    pool: asyncpg.Pool,
    account_id: int,
    external_id: str,
    amount_minor: int,
    currency: str,
    description: str,
    posted_at: datetime,
) -> None:
    """Idempotent insert: re-running a sync updates in place instead of duplicating."""
    await pool.execute(
        """
        INSERT INTO transactions
            (account_id, external_transaction_id, amount_minor, currency, description, posted_at)
        VALUES ($1, $2, $3, $4, $5, $6)
        ON CONFLICT (account_id, external_transaction_id)
        DO UPDATE SET amount_minor = EXCLUDED.amount_minor,
                      description  = EXCLUDED.description,
                      posted_at    = EXCLUDED.posted_at
        """,
        account_id,
        external_id,
        amount_minor,
        currency,
        description,
        posted_at,
    )
