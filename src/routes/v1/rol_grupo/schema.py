from pydantic import BaseModel, Field
from typing import Optional

class RolGrupo(BaseModel):
  id: Optional[int] = None
  clave: str = Field(min_length=1, max_length=255)
  descripcion: str

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "clave": "propietario",
        "descripcion": "Tiene acceso total al grupo"
      }
    }