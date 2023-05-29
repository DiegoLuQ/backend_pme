from fastapi import APIRouter
from .route_accion import router as router_accion
from .route_colegio import router as router_colegio
from .router_actividad import router as router_actividad
from .route_pme import router as router_pme
from .route_presupuesto_colegio import router as router_presupuesto_colegio
from .route_presupuesto import router as router_presupuesto
from .route_recurso import router as router_recurso
from .route_user import router as router_user
from .route_login import router as router_login
router = APIRouter()

router.include_router(router_user, prefix='/user', tags=["Usuarios"])
router.include_router(router_login, prefix='/login', tags=["Login"])
router.include_router(router_colegio, prefix='/colegio', tags=["Colegios"])
router.include_router(router_pme, prefix='/pme', tags=["PME"])
router.include_router(router_accion, prefix='/accion', tags=["Acciones"])
router.include_router(router_actividad, prefix='/actividades', tags=["Actividades"])
router.include_router(router_recurso, prefix='/recursos', tags=["Recursos de Actividades"])
router.include_router(router_presupuesto, prefix='/presupuesto', tags=["Presupuesto"])
router.include_router(router_presupuesto_colegio, prefix='/lista_presupuesto', tags=["Lista Presupuesto"])

