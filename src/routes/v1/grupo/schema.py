from pydantic import BaseModel, Field, constr
from typing import Optional
    
class Grupo(BaseModel):
  id: Optional[int] = None
  nombre: str = Field(min_length=1, max_length=255)
  descripcion: Optional[constr(min_length=1)] = None
  color: Optional[constr(min_length=1, max_length=50)] = None
  profile_pic: Optional[constr(min_length=1, max_length=255)] = None
  banner: Optional[constr(min_length=1, max_length=255)] = None

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "nombre": "Grupo de amigos",
        "descripcion": "Descripcion del grupo",
        "color": "#FFFFFF",
        "profile_pic": "http://localhost/notitas_back/public/images/pfp/default.jpg",
        "banner": "http://localhost/notitas_back/public/images/banner/default.jpg"
      }
    }