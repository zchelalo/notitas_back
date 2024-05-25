from config.database import Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship

class MiembroGrupo(Base):
  __tablename__ = "miembros_grupo"

  id = Column(Integer, primary_key=True, autoincrement=True)
  usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
  grupo_id = Column(Integer, ForeignKey('grupos.id'), nullable=False)
  rol_grupo_id = Column(Integer, ForeignKey('roles_grupo.id'), nullable=False)
  disabled = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  usuario = relationship('Usuario', back_populates='miembros_grupo')
  grupo = relationship('Grupo', back_populates='miembros_grupo')
  rol_grupo = relationship('RolGrupo', back_populates='miembro_grupo')