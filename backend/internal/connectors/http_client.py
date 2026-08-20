"""An httpx client with a hard timeout so a slow bank can never hang a worker forever."""
from __future__ import annotations

import httpx

# Financial APIs can be slow; a bounded timeout prevents an indefinite hang.
DEFAULT_TIMEOUT = httpx.Timeout(connect=3.0, read=10.0, write=5.0, pool=3.0)


def make_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
