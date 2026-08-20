"""A small, low-cardinality Prometheus metric set. Resist over-instrumenting early."""
from __future__ import annotations

from prometheus_client import Counter, Histogram

# Labels are kept low-cardinality: a bounded set of endpoints and status codes.
REQUESTS = Counter(
    "api_requests_total", "API requests", ["endpoint", "status"]
)
REQUEST_LATENCY = Histogram(
    "api_request_seconds", "Request latency", ["endpoint"]
)
SYNC_RESULT = Counter(
    "sync_total", "Sync runs", ["result"]  # result = success | failure
)
CACHE_LOOKUPS = Counter(
    "cache_lookups_total", "Cache lookups", ["outcome"]  # outcome = hit | miss
)


def record_cache(outcome: str) -> None:
    CACHE_LOOKUPS.labels(outcome=outcome).inc()


def record_sync(success: bool) -> None:
    SYNC_RESULT.labels(result="success" if success else "failure").inc()
