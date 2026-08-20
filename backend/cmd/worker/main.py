"""Worker entry point: a separate process from the API, scaled independently."""
from __future__ import annotations

import asyncio
import os

import asyncpg
from aiokafka import AIOKafkaConsumer

from internal.connectors.mockbank import MockBankConnector
from internal.events.types import SYNC_REQUESTED_TOPIC
from internal.ingestion.consumer import SyncConsumer
from internal.ingestion.sync_processor import SyncProcessor


async def main() -> None:
    pool = await asyncpg.create_pool(dsn=os.environ["DATABASE_URL"])
    consumer = AIOKafkaConsumer(
        SYNC_REQUESTED_TOPIC,
        bootstrap_servers=os.environ.get("KAFKA_BROKERS", "localhost:9092"),
        group_id="ingestion-workers",
        enable_auto_commit=False,  # commit manually after success
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        processor = SyncProcessor(pool, MockBankConnector())
        await SyncConsumer(consumer, processor).run()
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
