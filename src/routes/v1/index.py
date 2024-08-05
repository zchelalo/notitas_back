from fastapi import APIRouter

from routes.v1.transcripcion.router import router as transcripcionRouter
from routes.v1.grupo.router import router as grupoRouter
from routes.v1.miembro_grupo.router import router as miembroGrupoRouter
from routes.v1.notitas.router import router as notitasRouter
from routes.v1.rol_grupo.router import router as rolGrupoRouter

router = APIRouter()

router.include_router(transcripcionRouter, prefix="/transcripcion", tags=["transcripcion"])
router.include_router(grupoRouter, prefix="/grupos", tags=["grupos"])
router.include_router(miembroGrupoRouter, prefix="/miembros_grupo", tags=["miembros_grupo"])
router.include_router(notitasRouter, prefix="/notitas", tags=["notitas"])
router.include_router(rolGrupoRouter, prefix="/roles_grupo", tags=["roles_grupo"])