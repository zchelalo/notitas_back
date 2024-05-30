from pydantic import BaseModel, conint, constr
from typing import Optional

class Notita(BaseModel):
  id: Optional[conint(strict=True, gt=0)] = None
  titulo: constr(min_length=0, max_length=255)
  nota: Optional[str] = None
  color: Optional[constr(min_length=0, max_length=50)] = None
  privada: Optional[bool] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "titulo": "Nota 1",
        "nota": "Esta es una nota",
        "color": "#FF0000",
        "privada": False
      }
    }

class NotitaCreate(BaseModel):
  titulo: constr(min_length=0, max_length=255)
  nota: Optional[str] = None
  color: Optional[constr(min_length=0, max_length=50)] = None
  privada: Optional[bool] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "titulo": "Nota 1",
        "nota": "Esta es una nota",
        "color": "#FF0000",
        "privada": False
      }
    }

class NotitaUpdate(BaseModel):
  titulo: Optional[constr(min_length=0, max_length=255)] = None
  nota: Optional[str] = None
  color: Optional[constr(min_length=0, max_length=50)] = None
  privada: Optional[bool] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "titulo": "Nota 1",
        "nota": "Esta es una nota",
        "color": "#FF0000",
        "privada": False
      }
    }