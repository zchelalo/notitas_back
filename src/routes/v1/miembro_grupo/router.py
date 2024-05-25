from fastapi import APIRouter, status, Depends, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT

from config.database import Session, engine, Base
from middlewares.auth_handler import CheckRoles

from routes.v1.miembro_grupo.schema import (
  MiembroGrupo as MiembroGrupoSchema,
  MiembroGrupoResponse as MiembroGrupoResponseSchema,
  MiembroGrupoCreate as MiembroGrupoCreateSchema
)
from routes.v1.miembro_grupo.service import MiembroGrupoService

router = APIRouter()

Base.metadata.create_all(bind=engine)

@router.get(
  path='', 
  tags=['miembros_grupo'], 
  status_code=status.HTTP_200_OK,
  response_model=list[MiembroGrupoResponseSchema],
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_miembros_grupo(
  grupo_id: int = None,
  usuario_id: int = None
) -> list[MiembroGrupoResponseSchema]:
  db = Session()
  result = MiembroGrupoService(db).get_miembros_grupo(grupo_id, usuario_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontraron miembros del grupo'})
  return result

@router.get(
  path='/{id}', 
  tags=['miembros_grupo'], 
  status_code=status.HTTP_200_OK,
  response_model=MiembroGrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_miembro_grupo(id: int) -> MiembroGrupoSchema:
  db = Session()
  result = MiembroGrupoService(db).get_miembro_grupo(id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontró al miembro del grupo'})
  return result

@router.post(
  path='', 
  tags=['miembros_grupo'], 
  status_code=status.HTTP_201_CREATED,
  response_model=MiembroGrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def create_miembro_grupo(miembro_grupo: MiembroGrupoCreateSchema) -> MiembroGrupoSchema:
  db = Session()
  result = MiembroGrupoService(db).create_miembro_grupo(miembro_grupo)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se pudo crear el miembro del grupo'})
  return result