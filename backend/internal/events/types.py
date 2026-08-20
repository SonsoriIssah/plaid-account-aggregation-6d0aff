"""Versioned event contracts. A `version` field lets consumers evolve safely."""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass

SYNC_REQUESTED_TOPIC = "aggregation.sync.requested"


@dataclass
class SyncRequested:
    version: int
    link_id: int
    reason: str          # 'link_connected' | 'manual' | 'scheduled'
    requested_at: str    # ISO 8601 UTC

    def to_json(self) -> bytes:
        return json.dumps(asdict(self)).encode()

    @staticmethod
    def from_json(raw: bytes) -> "SyncRequested":
        return SyncRequested(**json.loads(raw))


SYNC_REQUESTED_V1 = 1
