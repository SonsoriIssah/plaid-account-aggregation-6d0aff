"""DTO serializers: stable response shapes independent of DB columns or institution."""
from __future__ import annotations

from typing import Any


def account_dto(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "institution": row["institution"],
        "account_name": row["account_name"],
        "mask": row["mask"],
        "currency": row["currency"],
        "balance": row["balance_minor"] / 100,  # minor units → major
        "updated_at": row["updated_at"].isoformat(),
    }


def transaction_dto(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": row["id"],
        "account_id": row["account_id"],
        "amount": row["amount_minor"] / 100,
        "currency": row["currency"],
        "description": row["description"],
        "posted_at": row["posted_at"].isoformat(),
    }
