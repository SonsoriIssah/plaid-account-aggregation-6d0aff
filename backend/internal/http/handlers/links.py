from fastapi import APIRouter, Depends

from ...connectors.registry import get_institution
from ...db.pool import get_pool
from ...validation.schemas import CreateLinkRequest
from ..errors import BadRequest
from ..middleware.auth import AuthContext, current_user

router = APIRouter()


@router.post("/links", status_code=201)
async def create_link(
    body: CreateLinkRequest,
    ctx: AuthContext = Depends(current_user),
) -> dict:
    """Initiate a link. The OAuth exchange that *completes* it happens later (step 4).

    Idempotent on (user_id, institution_id): re-initiating an existing link
    returns the existing record instead of creating a duplicate.
    """
    inst = get_institution(body.institution_slug)
    if inst is None:
        raise BadRequest(f"unknown institution: {body.institution_slug}")

    pool = get_pool()
    inst_id = await pool.fetchval(
        "SELECT id FROM institutions WHERE slug = $1", inst.slug
    )
    row = await pool.fetchrow(
        """
        INSERT INTO links (user_id, institution_id, status)
        VALUES ($1, $2, 'pending')
        ON CONFLICT (user_id, institution_id) DO UPDATE SET status = links.status
        RETURNING id, status
        """,
        ctx.user_id,
        inst_id,
    )
    return {
        "link_id": row["id"],
        "status": row["status"],
        "authorize_url": inst.oauth_authorize_url,
    }
