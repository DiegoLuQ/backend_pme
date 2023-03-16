from fastapi import APIRouter
from .route_accion import router as router_accion
from .route_colegio import router as router_colegio
from .router_actividad import router as router_actividad
from .route_pme import router as router_pme
router = APIRouter()

router.include_router(router_colegio, prefix='/colegio', tags=["Colegios"])
router.include_router(router_pme, prefix='/pme', tags=["PME"])
router.include_router(router_accion, prefix='/accion', tags=["Acciones"])
router.include_router(router_actividad, prefix='/subaccion', tags=["Actividades"])
