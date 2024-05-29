from config.database import Base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class NotitaGrupo(Base):
  __tablename__ = "notitas_grupo"

  id = Column(Integer, primary_key=True, autoincrement=True)
  notita_id = Column(Integer, ForeignKey('notitas.id'), nullable=False)
  grupo_id = Column(Integer, ForeignKey('grupos.id'), nullable=False)
  disabled = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  notita = relationship('Notita', back_populates='notitas_grupo')
  grupo = relationship('Grupo', back_populates='notitas_grupo')