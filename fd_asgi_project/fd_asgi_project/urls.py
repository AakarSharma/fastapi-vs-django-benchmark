from __future__ import annotations

from fast_django.routers import APIRouter
from .routes import router as routes_router

router = APIRouter()
router.include_router(routes_router)


@router.get("/health")
def healthz() -> dict[str, str]:
    return {"status": "ok"}
