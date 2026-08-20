"""Consumes sync events in a consumer group and dispatches each to the processor."""
from __future__ import annotations

from aiokafka import AIOKafkaConsumer

from ..events.types import SYNC_REQUESTED_TOPIC, SyncRequested
from .sync_processor import SyncProcessor


class SyncConsumer:
    def __init__(self, consumer: AIOKafkaConsumer, processor: SyncProcessor):
        self._consumer = consumer
        self._processor = processor

    async def run(self) -> None:
        async for message in self._consumer:
            event = SyncRequested.from_json(message.value)
            await self._processor.process(event.link_id)
            # Commit only after successful processing → at-least-once delivery.
            await self._consumer.commit()
