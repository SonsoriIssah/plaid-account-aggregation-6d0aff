"""The connector interface every institution integration implements.

Keeping bank-specific logic behind this interface means the OAuth handler,
the ingestion worker, and the API never import a specific bank — only `Connector`.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class TokenSet:
    access_token: str
    refresh_token: str | None
    expires_in: int  # seconds


@dataclass
class RawAccount:
    external_account_id: str
    name: str
    mask: str | None
    currency: str
    balance_minor: int


@dataclass
class RawTransaction:
    external_transaction_id: str
    account_external_id: str
    amount_minor: int
    currency: str
    description: str
    posted_at: str  # ISO 8601


class Connector(ABC):
    @abstractmethod
    async def exchange_code(self, code: str) -> TokenSet:
        """Trade an OAuth2 authorization code for tokens."""

    @abstractmethod
    async def fetch_accounts(self, access_token: str) -> list[RawAccount]:
        ...

    @abstractmethod
    async def fetch_transactions(
        self, access_token: str, cursor: str | None
    ) -> tuple[list[RawTransaction], str]:
        """Return (transactions, next_cursor) for incremental sync."""
