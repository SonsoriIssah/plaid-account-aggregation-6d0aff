"""A deterministic mock bank so the whole pipeline runs without a real institution."""
from __future__ import annotations

from .base import Connector, RawAccount, RawTransaction, TokenSet


class MockBankConnector(Connector):
    async def exchange_code(self, code: str) -> TokenSet:
        # A real connector POSTs to the bank's token endpoint. The mock derives
        # a deterministic token from the code so the flow is reproducible.
        return TokenSet(
            access_token=f"mock-access-{code}",
            refresh_token=f"mock-refresh-{code}",
            expires_in=3600,
        )

    async def fetch_accounts(self, access_token: str) -> list[RawAccount]:
        return [
            RawAccount(
                external_account_id="acct_checking_1",
                name="MockBank Checking",
                mask="4321",
                currency="USD",
                balance_minor=125_000,  # $1,250.00
            ),
        ]

    async def fetch_transactions(
        self, access_token: str, cursor: str | None
    ) -> tuple[list[RawTransaction], str]:
        if cursor == "cursor-2":
            return [], "cursor-2"  # nothing new since last sync
        txns = [
            RawTransaction(
                external_transaction_id="txn_1",
                account_external_id="acct_checking_1",
                amount_minor=-4_200,  # $42.00 debit
                currency="USD",
                description="Coffee Roasters",
                posted_at="2026-06-20T14:03:00Z",
            ),
        ]
        return txns, "cursor-2"
