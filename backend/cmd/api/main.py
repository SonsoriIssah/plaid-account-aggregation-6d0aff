"""API entry point: builds the FastAPI app, wires the error handler and request IDs."""
from __future__ import annotations

import uuid

from fastapi import FastAPI, Request

from internal.http.errors import ApiError, api_error_handler, error_response
from internal.http.router import api_router


def create_app() -> FastAPI:
    app = FastAPI(title="Account Aggregation API")
    app.include_router(api_router)
    app.add_exception_handler(ApiError, api_error_handler)

    @app.middleware("http")
    async def add_request_id(request: Request, call_next):
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        response = await call_next(request)
        response.headers["x-request-id"] = request_id
        return response

    @app.exception_handler(Exception)
    async def unhandled(_request: Request, _exc: Exception):
        return error_response(500, "internal", "internal server error")

    return app


app = create_app()
