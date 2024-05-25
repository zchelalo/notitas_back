from config.database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, func
from sqlalchemy.orm import relationship

class RolGrupo(Base):
  __tablename__ = "roles_grupo"

  id = Column(Integer, primary_key=True, autoincrement=True)
  clave = Column(String(255), nullable=False)
  descripcion = Column(Text, nullable=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  miembro_grupo = relationship('MiembroGrupo', back_populates='rol_grupo')