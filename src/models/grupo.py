from config.database import Base
from sqlalchemy import Column, Integer, Text, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship

class Grupo(Base):
  __tablename__ = "grupos"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(255), nullable=False)
  descripcion = Column(Text, nullable=True)
  profile_pic = Column(String(255), nullable=True)
  banner = Column(String(255), nullable=True)
  color = Column(String(50), nullable=True)
  disabled = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  miembros_grupo = relationship('MiembroGrupo', cascade="all, delete", back_populates='grupo')