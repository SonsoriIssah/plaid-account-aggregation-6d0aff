from fastapi import APIRouter, Depends

from ...db.pool import get_pool
from ...events.producer import SyncProducer
from ...events.deps import get_producer
from ..errors import NotFound
from ..middleware.auth import AuthContext, current_user

router = APIRouter()


@router.post("/links/{link_id}/sync", status_code=202)
async def trigger_sync(
    link_id: int,
    ctx: AuthContext = Depends(current_user),
    producer: SyncProducer = Depends(get_producer),
) -> dict:
    """Request an async sync. Returns 202 Accepted — the work happens in the worker."""
    pool = get_pool()
    row = await pool.fetchrow(
        "SELECT status FROM links WHERE id = $1 AND user_id = $2",
        link_id,
        ctx.user_id,
    )
    if row is None:
        raise NotFound("link not found")

    await producer.request_sync(link_id, reason="manual")
    return {"link_id": link_id, "status": "sync_requested"}
