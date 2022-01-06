from fastapi import APIRouter

from app.api.api_v1.endpoints import (
    domains,
    login,
    users,
    utils,
    events,
    analytics,
    billing,
)

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(domains.router, prefix="/domains", tags=["domains"])
api_router.include_router(events.router, tags=["events"])
api_router.include_router(analytics.router, prefix="/a", tags=["analytics"])
api_router.include_router(billing.router, prefix="/billing", tags=["billing"])
