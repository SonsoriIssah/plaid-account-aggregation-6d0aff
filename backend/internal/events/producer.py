"""Publishes sync events. link_id is the partition key so a link's events stay ordered."""
from __future__ import annotations

from datetime import datetime, timezone

from aiokafka import AIOKafkaProducer

from .types import SYNC_REQUESTED_TOPIC, SYNC_REQUESTED_V1, SyncRequested


class SyncProducer:
    def __init__(self, producer: AIOKafkaProducer):
        self._producer = producer

    async def request_sync(self, link_id: int, reason: str) -> None:
        event = SyncRequested(
            version=SYNC_REQUESTED_V1,
            link_id=link_id,
            reason=reason,
            requested_at=datetime.now(timezone.utc).isoformat(),
        )
        # Keying by link_id routes every event for one link to the same partition,
        # which preserves per-link ordering under at-least-once delivery.
        await self._producer.send_and_wait(
            SYNC_REQUESTED_TOPIC,
            key=str(link_id).encode(),
            value=event.to_json(),
        )
