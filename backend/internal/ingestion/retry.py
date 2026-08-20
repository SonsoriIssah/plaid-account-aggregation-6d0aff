"""Bounded retries with exponential backoff. Small budgets — banks are rate-limited."""
from __future__ import annotations

import asyncio
from typing import Awaitable, Callable, TypeVar

T = TypeVar("T")


async def with_retries(
    fn: Callable[[], Awaitable[T]],
    *,
    attempts: int = 3,
    base_delay: float = 0.5,
) -> T:
    """Call `fn`, retrying on exception up to `attempts` times with exponential backoff.

    Re-raises the last error once the budget is exhausted, so the caller still fails loud.
    """
    last_exc: Exception | None = None
    for attempt in range(attempts):
        try:
            return await fn()
        except Exception as exc:  # noqa: BLE001 — bounded retry of any transient failure
            last_exc = exc
            if attempt < attempts - 1:
                await asyncio.sleep(base_delay * (2 ** attempt))  # 0.5s, 1s, 2s…
    assert last_exc is not None
    raise last_exc
