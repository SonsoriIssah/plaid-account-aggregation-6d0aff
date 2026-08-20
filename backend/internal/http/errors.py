"""One error shape for the whole API: {"error": {"code", "message", "details"}}."""
from __future__ import annotations

from typing import Any, Optional

from fastapi import Request
from fastapi.responses import JSONResponse


class ApiError(Exception):
    """A domain error that carries its own HTTP status and stable code."""

    def __init__(self, status: int, code: str, message: str, details: Any = None):
        self.status = status
        self.code = code
        self.message = message
        self.details = details
        super().__init__(message)


class NotFound(ApiError):
    def __init__(self, message: str = "not found", details: Any = None):
        super().__init__(404, "not_found", message, details)


class BadRequest(ApiError):
    def __init__(self, message: str = "bad request", details: Any = None):
        super().__init__(400, "bad_request", message, details)


class Unauthorized(ApiError):
    def __init__(self, message: str = "missing or invalid credentials"):
        super().__init__(401, "unauthorized", message)


def error_response(status: int, code: str, message: str, details: Any = None) -> JSONResponse:
    body: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details is not None:
        body["error"]["details"] = details
    return JSONResponse(status_code=status, content=body)


async def api_error_handler(_request: Request, exc: ApiError) -> JSONResponse:
    return error_response(exc.status, exc.code, exc.message, exc.details)
