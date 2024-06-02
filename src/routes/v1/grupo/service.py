from sqlalchemy import text

from models import (
  GrupoModel,
  RolGrupoModel,
  MiembroGrupoModel
)
from routes.v1.grupo.schema import Grupo as GrupoSchema
from routes.v1.miembro_grupo.schema import MiembroGrupo as MiembroGrupoSchema

class GrupoService():
  def __init__(self, db) -> None:
    self.db = db

  def get_grupos(self, usuario_id: int):
    with self.db as session:
      sql = text("""
        SELECT
          "grupos"."id",
          "grupos"."nombre",
          "grupos"."descripcion",
          "grupos"."profile_pic",
          "grupos"."banner",
          "grupos"."color"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        WHERE "grupos"."disabled" = FALSE
        AND "miembros_grupo"."disabled" = FALSE
        AND "miembros_grupo"."usuario_id" = :usuario_id
        ORDER BY "grupos"."id" DESC
      """)

      query = session.execute(sql, {"usuario_id": usuario_id})
      grupos = query.fetchall()

      return grupos

  def get_grupo(self, id: int, usuario_id: int):
    with self.db as session:
      sql = text("""
        SELECT
          "grupos"."id",
          "grupos"."nombre",
          "grupos"."descripcion",
          "grupos"."profile_pic",
          "grupos"."banner",
          "grupos"."color"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        WHERE "grupos"."disabled" = FALSE
        AND "miembros_grupo"."disabled" = FALSE
        AND "miembros_grupo"."usuario_id" = :usuario_id
        AND "grupos"."id" = :id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "id": id})
      grupo = query.fetchone()
      
      return grupo

  def create_grupo(self, usuario_id: int, grupo: GrupoSchema):
    with self.db as session:
      new_grupo = GrupoModel(**grupo.model_dump())
      session.add(new_grupo)
      session.flush()

      # Obtener el ID del grupo recién insertado
      grupo_id = new_grupo.id

      # Obtener el ID del rol de grupo "administrador"
      rol_propietario = session.query(RolGrupoModel).filter(RolGrupoModel.clave == "propietario").one_or_none()

      if not rol_propietario:
        return None

      # Insertar al usuario en el grupo con el rol de administrador
      new_miembro_grupo_schema = MiembroGrupoSchema(usuario_id=usuario_id, grupo_id=grupo_id, rol_grupo_id=rol_propietario.id)
      new_miembro_grupo = MiembroGrupoModel(**new_miembro_grupo_schema.model_dump())
      session.add(new_miembro_grupo)
      session.commit()
      session.refresh(new_grupo)
      session.refresh(new_miembro_grupo)
      
      return new_grupo

  def update_grupo(self, usuario_id: int, id: int, grupo_update: GrupoSchema):
    with self.db as session:
      grupo = session.query(GrupoModel).filter(GrupoModel.id == id).one_or_none()
      if not grupo:
        return None

      sql = text("""
        SELECT "roles_grupo"."clave"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."usuario_id" = :usuario_id AND "grupos"."id" = :grupo_id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "grupo_id": grupo.id})
      rol_grupo_clave = query.fetchone()

      if not rol_grupo_clave:
        raise ValueError("No se encontró el rol del grupo para el usuario")

      rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))  # Convertir a un diccionario

      roles_permitidos = ["propietario", "administrador"]

      if rol_grupo_clave.get("clave") not in roles_permitidos:
        raise ValueError("El usuario no tiene permisos para modificar este grupo")

      for field, value in grupo_update.model_dump(exclude_unset=True).items():
        setattr(grupo, field, value)

      session.commit()
      session.refresh(grupo)
      return grupo

  def delete_grupo(self, usuario_id: int, grupo: GrupoModel):
    with self.db as session:
      sql = text("""
        SELECT "roles_grupo"."clave"
        FROM "miembros_grupo"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."usuario_id" = :usuario_id AND "miembros_grupo"."grupo_id" = :grupo_id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "grupo_id": grupo.id})
      rol_grupo_clave = query.fetchone()

      if not rol_grupo_clave:
        raise ValueError("No se encontró el rol del grupo para el usuario")

      if rol_grupo_clave:
        rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))  # Convertir a un diccionario

      if rol_grupo_clave.get("clave") != "propietario":
        raise ValueError("El usuario no tiene permisos de propietario en este grupo")

      grupo.disabled = True
      session.add(grupo)

      miembros_grupo = session.query(MiembroGrupoModel).filter(MiembroGrupoModel.grupo_id == grupo.id).all()
      for miembro_grupo in miembros_grupo:
        miembro_grupo.disabled = True
        session.add(miembro_grupo)

      session.commit()
      return True