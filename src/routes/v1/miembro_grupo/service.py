from sqlalchemy import text

from models import (
  MiembroGrupoModel
)
from routes.v1.miembro_grupo.schema import MiembroGrupo as MiembroGrupoSchema

class MiembroGrupoService():
  def __init__(self, db) -> None:
    self.db = db

  def get_miembros_grupo(self, grupo_id, usuario_id):
    with self.db as session:
      # filtros = [
      #   MiembroGrupoModel.disabled == False
      # ]

      # if grupo_id:
      #   filtros.append(MiembroGrupoModel.grupo_id == grupo_id)

      # if usuario_id:
      #   filtros.append(MiembroGrupoModel.usuario_id == usuario_id)

      # result = session.query(MiembroGrupoModel).filter(*filtros).all()

      params = {}

      sql = """
        SELECT
          "miembros_grupo"."id",
          "miembros_grupo"."usuario_id",
          "miembros_grupo"."grupo_id",
          "miembros_grupo"."rol_grupo_id",
          "roles_grupo"."clave" AS "rol_grupo_clave",
          "roles_grupo"."descripcion" AS "rol_grupo_descripcion",
          "usuarios"."nombre" AS "usuario_nombre",
          "usuarios"."profile_pic" AS "usuario_profile_pic",
          "grupos"."nombre" AS "grupo_nombre",
          "grupos"."profile_pic" AS "grupo_profile_pic"
        FROM "miembros_grupo"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        INNER JOIN "grupos"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        INNER JOIN "usuarios"
        ON "miembros_grupo"."usuario_id" = "usuarios"."id"
        WHERE "miembros_grupo"."disabled" = FALSE
      """

      if grupo_id:
        sql += " AND \"miembros_grupo\".\"grupo_id\" = :grupo_id"
        params["grupo_id"] = grupo_id

      if usuario_id:
        sql += " AND \"miembros_grupo\".\"usuario_id\" = :usuario_id"
        params["usuario_id"] = usuario_id

      query = session.execute(text(sql), params)
      miembros_grupo = query.fetchall()

      if not miembros_grupo:
        raise ValueError("No se encontrarón miembros del grupo")
      
      # if rol_grupo_clave:
      #   rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))  # Convertir a un diccionario
      return miembros_grupo

  def get_miembro_grupo(self, id):
    with self.db as session:
      filtros = [
        MiembroGrupoModel.disabled == False
      ]

      filtros.append(MiembroGrupoModel.id == id)

      result = session.query(MiembroGrupoModel).filter(*filtros).one_or_none()
      return result

  def create_miembro_grupo(self, miembro_grupo: MiembroGrupoSchema):
    with self.db as session:
      miembro_grupo = MiembroGrupoModel(**miembro_grupo.dict())
      session.add(miembro_grupo)
      session.commit()
      session.refresh(miembro_grupo)
      return miembro_grupo