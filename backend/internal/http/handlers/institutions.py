from fastapi import APIRouter

from ...connectors.registry import list_institutions

router = APIRouter()


@router.get("/institutions")
async def get_institutions() -> dict[str, list[dict]]:
    """List the institutions a user can link. Returns [] (not null) when empty."""
    items = [
        {"slug": inst.slug, "name": inst.name}
        for inst in list_institutions()
    ]
    return {"institutions": items}
