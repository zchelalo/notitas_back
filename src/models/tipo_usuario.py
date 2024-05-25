from config.database import Base
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

class TipoUsuario(Base):
  __tablename__ = "tipos_usuario"

  id = Column(Integer, primary_key=True, autoincrement=True)
  clave = Column(String(255), nullable=False, unique=True)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  usuarios = relationship('Usuario', back_populates='tipo_usuario')