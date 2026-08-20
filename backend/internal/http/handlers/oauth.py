import secrets

from fastapi import APIRouter, Query

from ...connectors.mockbank import MockBankConnector
from ...db.pool import get_pool
from ...security.crypto import encrypt
from ..errors import BadRequest

router = APIRouter()

# In-memory state store for the MVP. Production uses signed/short-lived state.
_PENDING_STATE: dict[str, int] = {}


@router.get("/oauth/start")
async def oauth_start(link_id: int) -> dict:
    """Mint a CSRF state token bound to the link the user is connecting."""
    state = secrets.token_urlsafe(24)
    _PENDING_STATE[state] = link_id
    return {"state": state}


@router.get("/oauth/callback")
async def oauth_callback(
    code: str = Query(...),
    state: str = Query(...),
) -> dict:
    """Validate state, exchange the code, and store encrypted tokens on the link."""
    link_id = _PENDING_STATE.pop(state, None)
    if link_id is None:
        raise BadRequest("invalid or expired state")  # CSRF / replay guard

    connector = MockBankConnector()
    tokens = await connector.exchange_code(code)

    pool = get_pool()
    await pool.execute(
        """
        UPDATE links
        SET access_token = $1,
            refresh_token = $2,
            token_expires_at = now() + ($3 || ' seconds')::interval,
            status = 'connected'
        WHERE id = $4
        """,
        encrypt(tokens.access_token),
        encrypt(tokens.refresh_token) if tokens.refresh_token else None,
        str(tokens.expires_in),
        link_id,
    )
    return {"link_id": link_id, "status": "connected"}
