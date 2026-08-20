"""The unified internal shapes — institution-independent. Connectors map *into* these."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class NormalizedAccount:
    external_account_id: str
    name: str
    mask: str | None
    currency: str
    balance_minor: int


@dataclass
class NormalizedTransaction:
    external_transaction_id: str
    account_external_id: str
    amount_minor: int
    currency: str
    description: str
    posted_at: str
