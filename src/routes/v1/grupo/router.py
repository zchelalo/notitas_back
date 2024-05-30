from fastapi import APIRouter, status, File, UploadFile, Depends, Form, HTTPException, Response
from fastapi.responses import JSONResponse
from starlette.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from typing import Optional
from starlette.requests import Request
from pydantic import constr

from config.database import Session, engine, Base
from middlewares.auth_handler import CheckRoles
from utils.image_manager import save_image, generate_unique_filename

from routes.v1.grupo.schema import Grupo as GrupoSchema
from routes.v1.grupo.service import GrupoService

router = APIRouter()

Base.metadata.create_all(bind=engine)

@router.get(
  path='', 
  tags=['grupos'], 
  status_code=status.HTTP_200_OK,
  response_model=list[GrupoSchema],
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_grupos(request: Request) -> list[GrupoSchema]:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  db = Session()
  result = GrupoService(db).get_grupos(usuario_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontraron grupos'})
  return result

@router.get(
  path='/{id}', 
  tags=['grupos'], 
  status_code=status.HTTP_200_OK,
  response_model=GrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def get_grupo(request: Request, id: int) -> GrupoSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  db = Session()
  result = GrupoService(db).get_grupo(id, usuario_id)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontró el grupo'})
  return result

@router.post(
  path='', 
  tags=['grupos'], 
  status_code=status.HTTP_200_OK,
  response_model=GrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def create_grupo(
  request: Request,
  nombre: str = Form(..., min_length=1, max_length=255),
  descripcion: Optional[constr(min_length=1)] = Form(None),
  color: Optional[constr(min_length=1, max_length=50)] = Form(None),
  profile_pic: Optional[UploadFile] = File(None),
  banner: Optional[UploadFile] = File(None)
) -> GrupoSchema:
  profile_pic_path, banner_path = None, None

  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  if profile_pic:
    profile_pic_contents = await profile_pic.read()
    filename = generate_unique_filename(profile_pic.filename)
    profile_pic_path = save_image(profile_pic_contents, filename, "pfp", str(request.base_url))

  if banner:
    banner_contents = await banner.read()
    filename = generate_unique_filename(banner.filename)
    banner_path = save_image(banner_contents, filename, "banner", str(request.base_url))

  grupo = GrupoSchema(nombre=nombre, descripcion=descripcion, color=color, profile_pic=profile_pic_path, banner=banner_path)

  db = Session()
  new_grupo = GrupoService(db).create_grupo(usuario_id, grupo)
  return new_grupo

@router.put(
  path='/{id}', 
  tags=['grupos'], 
  status_code=status.HTTP_200_OK,
  response_model=GrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def update_grupo(
  request: Request,
  id: int,
  nombre: Optional[constr(min_length=1, max_length=255)] = Form(None),
  descripcion: Optional[constr(min_length=1)] = Form(None),
  color: Optional[constr(min_length=1, max_length=50)] = Form(None),
  profile_pic: Optional[UploadFile] = File(None),
  banner: Optional[UploadFile] = File(None),
) -> GrupoSchema:
  db = Session()
  grupo = GrupoService(db).get_grupo(id)
  if not grupo:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontró el grupo'})

  grupo_schema = GrupoSchema.from_orm(grupo)

  profile_pic_path, banner_path = None, None

  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")

  if profile_pic:
    profile_pic_contents = await profile_pic.read()
    filename = generate_unique_filename(profile_pic.filename)
    profile_pic_path = save_image(profile_pic_contents, filename, "pfp", str(request.base_url))

  if banner:
    banner_contents = await banner.read()
    filename = generate_unique_filename(banner.filename)
    banner_path = save_image(banner_contents, filename, "banner", str(request.base_url))

  grupo_schema.nombre = nombre if nombre else grupo_schema.nombre
  grupo_schema.descripcion = descripcion if descripcion else grupo_schema.descripcion
  grupo_schema.color = color if color else grupo_schema.color
  grupo_schema.profile_pic = profile_pic_path if profile_pic_path else grupo_schema.profile_pic
  grupo_schema.banner = banner_path if banner_path else grupo_schema.banner

  updated_grupo = GrupoService(db).update_grupo(usuario_id, id, grupo_schema)
  return updated_grupo

@router.delete(
  path='/{id}', 
  tags=['grupos'], 
  status_code=status.HTTP_200_OK,
  response_model=GrupoSchema,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def delete_grupo(request: Request, id: int) -> GrupoSchema:
  data_usuario = request.state.data_usuario
  usuario_id = data_usuario.get("sub")
  
  db = Session()
  grupo = GrupoService(db).get_grupo(id)
  if not grupo:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se encontró el grupo'})
  
  result = GrupoService(db).delete_grupo(usuario_id, grupo)
  if not result:
    raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail={'message': 'No se pudo eliminar el grupo'})

  return JSONResponse(status_code=HTTP_200_OK, content={'message': 'Grupo eliminado correctamente'})