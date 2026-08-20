from fastapi import APIRouter

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    """Liveness probe for the load balancer and container healthcheck."""
    return {"status": "ok"}
