from fastapi import APIRouter

from .handlers import (
    accounts,
    health,
    institutions,
    links,
    oauth,
    sync,
    transactions,
)

api_router = APIRouter()
api_router.include_router(health.router, tags=["system"])
api_router.include_router(institutions.router, tags=["linking"])
api_router.include_router(links.router, tags=["linking"])
api_router.include_router(oauth.router, tags=["linking"])
api_router.include_router(sync.router, tags=["ingestion"])
api_router.include_router(accounts.router, tags=["data"])
api_router.include_router(transactions.router, tags=["data"])
