"""Map raw connector data into the unified internal model.

Every institution returns its own field names; this is the one place that flattens
them into NormalizedAccount/NormalizedTransaction so the rest of the system is uniform.
"""
from __future__ import annotations

from ..connectors.base import RawAccount, RawTransaction
from .models import NormalizedAccount, NormalizedTransaction


def map_account(raw: RawAccount) -> NormalizedAccount:
    return NormalizedAccount(
        external_account_id=raw.external_account_id,
        name=raw.name,
        mask=raw.mask,
        currency=raw.currency,
        balance_minor=raw.balance_minor,
    )


def map_transaction(raw: RawTransaction) -> NormalizedTransaction:
    return NormalizedTransaction(
        external_transaction_id=raw.external_transaction_id,
        account_external_id=raw.account_external_id,
        amount_minor=raw.amount_minor,
        currency=raw.currency,
        description=raw.description,
        posted_at=raw.posted_at,
    )
