from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

router = APIRouter()


@router.get("/metrics")
async def metrics() -> Response:
    """Prometheus scrape endpoint — exposes the in-process registry."""
    return Response(content=generate_latest(), media_type=CONTENT_TYPE_LATEST)
