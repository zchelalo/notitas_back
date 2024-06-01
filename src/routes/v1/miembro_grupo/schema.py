from pydantic import BaseModel, conint
from typing import Optional

class MiembroGrupo(BaseModel):
  id: Optional[conint(strict=True, gt=0)] = None
  usuario_id: conint(strict=True, gt=0)
  grupo_id: conint(strict=True, gt=0)
  rol_grupo_id: conint(strict=True, gt=0)

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "usuario_id": 1,
        "grupo_id": 1,
        "rol_grupo_id": 1
      }
    }

class MiembroGrupoCreate(BaseModel):
  usuario_id: conint(strict=True, gt=0)
  grupo_id: conint(strict=True, gt=0)
  rol_grupo_id: conint(strict=True, gt=0)

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "usuario_id": 1,
        "grupo_id": 1,
        "rol_grupo_id": 1
      }
    }

class MiembroGrupoUpdate(BaseModel):
  rol_grupo_id: conint(strict=True, gt=0)

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "rol_grupo_id": 1
      }
    }

class MiembroGrupoResponse(BaseModel):
  id: int
  rol_grupo_id: int
  rol_grupo_clave: str
  rol_grupo_descripcion: str
  usuario_id: int
  usuario_nombre: str
  usuario_profile_pic: Optional[str] = None
  grupo_id: int
  grupo_nombre: str
  grupo_descripcion: Optional[str] = None
  grupo_profile_pic: Optional[str] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "id": 1,
        "rol_grupo_id": 1,
        "rol_grupo_clave": "admin",
        "rol_grupo_descripcion": "Administrador del grupo",
        "usuario_id": 1,
        "usuario_nombre": "Juan",
        "usuario_profile_pic": "http://localhost/notitas_back/public/images/pfp/default.jpg",
        "grupo_id": 1,
        "grupo_nombre": "Grupo 1",
        "grupo_profile_pic": "http://localhost/notitas_back/public/images/banner/default.jpg"
      }
    }

class InvitationData(BaseModel):
  grupo_id: int
  correo: str
  rol_grupo_id: int

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "grupo_id": 1,
        "correo": "eduardosaavedra687@gmail.com",
        "rol_grupo_id": 1
      }
    }

class TokenAceptarInv(BaseModel):
  token: str

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "token": "eyJ0eXA.dgsfg8gsd.3gx_bf78a"
      }
    }