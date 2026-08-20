"""Hardened ingestion: fetch with retries, record last_error on failure for the UI."""
from __future__ import annotations

from datetime import datetime

import asyncpg

from ..connectors.base import Connector
from ..ingestion.retry import with_retries
from ..normalization.mapper import map_account, map_transaction
from ..observability.metrics import record_sync
from ..security.crypto import decrypt


class SyncProcessor:
    def __init__(self, pool: asyncpg.Pool, connector: Connector):
        self._pool = pool
        self._connector = connector

    async def process(self, link_id: int) -> None:
        link = await self._pool.fetchrow(
            "SELECT access_token, sync_cursor FROM links WHERE id = $1", link_id
        )
        if link is None or link["access_token"] is None:
            return

        access_token = decrypt(link["access_token"])
        try:
            await self._run(link_id, access_token, link["sync_cursor"])
            record_sync(success=True)
        except Exception as exc:  # noqa: BLE001
            # Record the failure on the link so the dashboard can surface it.
            await self._pool.execute(
                "UPDATE links SET status = 'error', last_error = $1 WHERE id = $2",
                str(exc), link_id,
            )
            record_sync(success=False)
            raise

    async def _run(self, link_id: int, access_token: str, cursor: str | None) -> None:
        # Each network call is wrapped in bounded retries with backoff.
        raw_accounts = await with_retries(
            lambda: self._connector.fetch_accounts(access_token)
        )
        ext_to_account_id: dict[str, int] = {}
        for raw in raw_accounts:
            acct = map_account(raw)
            account_id = await self._pool.fetchval(
                """
                INSERT INTO accounts
                    (link_id, external_account_id, name, mask, currency, balance_minor, updated_at)
                VALUES ($1, $2, $3, $4, $5, $6, now())
                ON CONFLICT (link_id, external_account_id)
                DO UPDATE SET balance_minor = EXCLUDED.balance_minor,
                              name = EXCLUDED.name, updated_at = now()
                RETURNING id
                """,
                link_id, acct.external_account_id, acct.name,
                acct.mask, acct.currency, acct.balance_minor,
            )
            ext_to_account_id[acct.external_account_id] = account_id

        raw_txns, next_cursor = await with_retries(
            lambda: self._connector.fetch_transactions(access_token, cursor)
        )
        for raw in raw_txns:
            txn = map_transaction(raw)
            account_id = ext_to_account_id.get(txn.account_external_id)
            if account_id is None:
                continue
            await self._pool.execute(
                """
                INSERT INTO transactions
                    (account_id, external_transaction_id, amount_minor, currency, description, posted_at)
                VALUES ($1, $2, $3, $4, $5, $6)
                ON CONFLICT (account_id, external_transaction_id)
                DO UPDATE SET amount_minor = EXCLUDED.amount_minor,
                              description = EXCLUDED.description, posted_at = EXCLUDED.posted_at
                """,
                account_id, txn.external_transaction_id, txn.amount_minor,
                txn.currency, txn.description, datetime.fromisoformat(txn.posted_at),
            )

        await self._pool.execute(
            "UPDATE links SET sync_cursor = $1, status = 'connected', last_error = NULL WHERE id = $2",
            next_cursor, link_id,
        )
