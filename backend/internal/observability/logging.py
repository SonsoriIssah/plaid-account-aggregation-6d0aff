"""Structured JSON logging — every line is a parseable object, not free text."""
from __future__ import annotations

import json
import logging
import sys
from typing import Any


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        # Attach any structured context the caller passed via `extra={"context": {...}}`.
        context = getattr(record, "context", None)
        if context:
            payload.update(context)
        return json.dumps(payload)


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger


def log_sync_failure(logger: logging.Logger, link_id: int, institution: str, err: str) -> None:
    """Log with enough context to reproduce: link, institution, and the error."""
    logger.error(
        "sync failed",
        extra={"context": {"link_id": link_id, "institution": institution, "error": err}},
    )
