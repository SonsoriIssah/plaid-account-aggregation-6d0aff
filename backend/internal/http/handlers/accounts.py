from fastapi import APIRouter, Depends

from ...db.pool import get_pool
from ...services.accounts_service import AccountsService
from ..middleware.auth import AuthContext, current_user

router = APIRouter()


@router.get("/accounts")
async def get_accounts(ctx: AuthContext = Depends(current_user)) -> dict:
    """All of the caller's accounts, served via the cache-aside service."""
    service = AccountsService(get_pool())
    accounts = await service.list_accounts(ctx.user_id)
    return {"accounts": accounts}
