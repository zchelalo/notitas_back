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