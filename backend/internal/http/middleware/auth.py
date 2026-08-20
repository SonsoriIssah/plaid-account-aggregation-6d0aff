"""MVP auth: an X-User-Id header maps to a user record. Production swaps this for OAuth/JWT."""
from __future__ import annotations

from dataclasses import dataclass

from fastapi import Header

from ..errors import Unauthorized


@dataclass
class AuthContext:
    user_id: int


async def current_user(x_user_id: str | None = Header(default=None)) -> AuthContext:
    """FastAPI dependency: resolves the caller's identity from a header.

    For the MVP a trusted header is enough to scope every query. In production
    this dependency would verify a signed JWT or call an auth service instead —
    the *shape* (a dependency that yields an AuthContext) stays identical.
    """
    if not x_user_id or not x_user_id.isdigit():
        raise Unauthorized("missing X-User-Id header")
    return AuthContext(user_id=int(x_user_id))
