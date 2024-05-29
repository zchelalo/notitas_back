from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from starlette.requests import Request

from config.database import Session, engine, Base
from middlewares.auth_handler import CheckRoles

from routes.v1.notitas.schema import (
  Notita as NotitaSchema,
  NotitaUsuarioCreate as NotitaUsuarioCreateSchema,
  NotitaUsuarioUpdate as NotitaUsuarioUpdateSchema
)
from routes.v1.notitas.service import NotitaService

router = APIRouter()

Base.metadata.create_all(bind=engine)

@router.get(
  path='/usuarios', 
  tags=['notitas'], 
  status_code=status.HTTP_200_OK,
  response_model=list[NotitaSchema],
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_notitas_usuario(request: Request) -> list[NotitaSchema]:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")
  
  db = Session()
  result = NotitaService(db).get_notitas_usuario(usuario_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'error': 'No se encontraron notitas'})
  return result

@router.get(
  path='/usuarios/{notita_id}', 
  tags=['notitas'], 
  status_code=status.HTTP_200_OK,
  response_model=NotitaSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_notitas_usuario(request: Request, notita_id: int) -> NotitaSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")
  
  db = Session()
  result = NotitaService(db).get_notita_usuario(usuario_id, notita_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'error': 'No se encontró la notita'})
  return result

@router.post(
  path='/usuarios',
  tags=['notitas'], 
  status_code=status.HTTP_200_OK,
  response_model=NotitaSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def create_notita_usuario(
  request: Request,
  notita: NotitaUsuarioCreateSchema
) -> NotitaSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  db = Session()
  new_notita = NotitaService(db).create_notita_usuario(usuario_id, notita)
  return new_notita

@router.put(
  path='/usuarios/{notita_id}',
  tags=['notitas'], 
  status_code=status.HTTP_200_OK,
  response_model=NotitaSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def update_notita_usuario(
  request: Request,
  notita_id: int,
  notita_update: NotitaUsuarioUpdateSchema
) -> NotitaSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  db = Session()
  updated_notita = NotitaService(db).update_notita_usuario(usuario_id, notita_id, notita_update)
  return updated_notita

@router.delete(
  path='/usuarios/{notita_id}',
  tags=['notitas'], 
  status_code=status.HTTP_200_OK,
  response_model=NotitaSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def update_notita_usuario(
  request: Request,
  notita_id: int
) -> NotitaSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  db = Session()
  result = NotitaService(db).delete_notita_usuario(usuario_id, notita_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se pudo eliminar la notita'})
  return JSONResponse(status_code=HTTP_200_OK, content={'message': 'Notita eliminada correctamente'})