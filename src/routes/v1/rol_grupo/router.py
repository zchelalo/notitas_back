from fastapi import APIRouter, status, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK

from config.database import Session, engine, Base
from middlewares.auth_handler import CheckRoles

from routes.v1.rol_grupo.schema import RolGrupo as RolGrupoSchema
from routes.v1.rol_grupo.service import RolGrupoService

router = APIRouter()

Base.metadata.create_all(bind=engine)

@router.get(
  path='', 
  tags=['roles_grupo'], 
  status_code=status.HTTP_200_OK,
  response_model=list[RolGrupoSchema],
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_roles_grupo() -> list[RolGrupoSchema]:
  db = Session()
  result = RolGrupoService(db).get_roles_grupo()
  if not result:
    return []
  return result

@router.get(
  path='/{id}',
  tags=['roles_grupo'], 
  status_code=status.HTTP_200_OK,
  response_model=RolGrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_rol_grupo(
  id: int
) -> RolGrupoSchema:
  db = Session()
  result = RolGrupoService(db).get_rol_grupo(id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontró el rol del grupo'})
  return result