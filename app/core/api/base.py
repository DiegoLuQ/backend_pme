from fastapi import APIRouter
from .v1.base import router as router_v1

router = APIRouter()

router.include_router(router_v1, prefix='/v1')