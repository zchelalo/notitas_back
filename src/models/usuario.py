from config.database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

class Usuario(Base):
  __tablename__ = "usuarios"

  id = Column(Integer, primary_key=True, autoincrement=True)
  nombre = Column(String(255), nullable=False)
  profile_pic = Column(String(255), nullable=True)
  correo = Column(String(255), nullable=False, unique=True)
  password = Column(String(255), nullable=False)
  tipo_usuario_id = Column(Integer, ForeignKey('tipos_usuario.id'), nullable=False)
  disabled = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  tipo_usuario = relationship('TipoUsuario', back_populates='usuarios')
  miembros_grupo = relationship('MiembroGrupo', back_populates='usuario')