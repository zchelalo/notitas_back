from config.database import Base
from sqlalchemy import Column, Integer, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class NotitaUsuario(Base):
  __tablename__ = "notitas_usuario"

  id = Column(Integer, primary_key=True, autoincrement=True)
  notita_id = Column(Integer, ForeignKey('notitas.id'), nullable=False)
  usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
  disabled = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  notita = relationship('Notita', back_populates='notitas_usuario')
  usuario = relationship('Usuario', back_populates='notitas_usuario')