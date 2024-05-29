from config.database import Base
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func
from sqlalchemy.orm import relationship

class Notita(Base):
  __tablename__ = "notitas"

  id = Column(Integer, primary_key=True, autoincrement=True)
  titulo = Column(String(255), nullable=False)
  nota = Column(Text, nullable=True)
  color = Column(String(255), nullable=True)
  privada = Column(Boolean, nullable=False, default=False)
  created_at = Column(DateTime, default=func.now())
  updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

  notitas_usuario = relationship('NotitaUsuario', back_populates='notita')
  notitas_grupo = relationship('NotitaGrupo', back_populates='notita')