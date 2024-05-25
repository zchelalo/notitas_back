from fastapi import APIRouter

from routes.v1.test.router import router as testRouter
from routes.v1.grupo.router import router as grupoRouter
from routes.v1.miembro_grupo.router import router as miembroGrupoRouter

router = APIRouter()

router.include_router(testRouter, tags=["test"])
router.include_router(grupoRouter, prefix="/grupos", tags=["grupos"])
router.include_router(miembroGrupoRouter, prefix="/miembros_grupo", tags=["miembros_grupo"])