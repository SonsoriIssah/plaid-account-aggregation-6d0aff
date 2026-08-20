from fastapi import APIRouter, Depends, Query

from ...db.pool import get_pool
from ..errors import NotFound
from ..serializers import transaction_dto
from ..middleware.auth import AuthContext, current_user

router = APIRouter()


@router.get("/accounts/{account_id}/transactions")
async def get_transactions(
    account_id: int,
    ctx: AuthContext = Depends(current_user),
    limit: int = Query(default=50, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
) -> dict:
    """Paginated transaction history for one account, scoped to the caller."""
    pool = get_pool()

    # Authorize: the account must belong to a link owned by the caller.
    owner = await pool.fetchval(
        """
        SELECT l.user_id
        FROM accounts a JOIN links l ON l.id = a.link_id
        WHERE a.id = $1
        """,
        account_id,
    )
    if owner != ctx.user_id:
        raise NotFound("account not found")  # 404, not 403 — don't reveal existence

    total = await pool.fetchval(
        "SELECT count(*) FROM transactions WHERE account_id = $1", account_id
    )
    rows = await pool.fetch(
        """
        SELECT id, account_id, amount_minor, currency, description, posted_at
        FROM transactions
        WHERE account_id = $1
        ORDER BY posted_at DESC
        LIMIT $2 OFFSET $3
        """,
        account_id, limit, offset,
    )
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "transactions": [transaction_dto(dict(r)) for r in rows],
    }
