from __future__ import annotations

from fast_django.routers import APIRouter
from .views import router as benchmark_router

router = APIRouter()

router.include_router(benchmark_router)
