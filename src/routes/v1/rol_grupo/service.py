from models import (
  RolGrupoModel
)

class RolGrupoService():
  def __init__(self, db) -> None:
    self.db = db

  def get_roles_grupo(self):
    with self.db as session:
      roles_grupo = session.query(RolGrupoModel).all()
      return roles_grupo

  def get_rol_grupo(self, id: int):
    with self.db as session:
      rol_grupo = session.query(RolGrupoModel).where(RolGrupoModel.id == id).one_or_none()
      return rol_grupo