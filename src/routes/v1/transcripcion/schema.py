from pydantic import BaseModel

class Text(BaseModel):
  texto: str

  class Config:
    from_attributes = True
    json_schema_extra = {
      "example": {
        "texto": "Texto a convertir a audio"
      }
    }