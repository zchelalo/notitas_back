from sqlalchemy import text, update

from models import (
  UsuarioModel,
  GrupoModel,
  MiembroGrupoModel,
  RolGrupoModel,
  NotitaModel,
  NotitaUsuarioModel,
  NotitaGrupoModel
)
from routes.v1.notitas.schema import Notita as NotitaSchema

class NotitaService():
  def __init__(self, db) -> None:
    self.db = db

  def get_notitas_usuario(self, usuario_id: int):
    with self.db as session:
      params = {}

      sql = """
        SELECT
          "notitas_usuario"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_usuario"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_usuario"."notita_id"
        WHERE "notitas_usuario"."disabled" = FALSE
      """

      sql += " AND \"notitas_usuario\".\"usuario_id\" = :usuario_id"
      params["usuario_id"] = usuario_id

      query = session.execute(text(sql), params)
      notitas = query.fetchall()

      return notitas

  def get_notita_usuario(self, usuario_id: int, notita_id: int):
    with self.db as session:
      params = {}

      sql = """
        SELECT
          "notitas_usuario"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_usuario"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_usuario"."notita_id"
        WHERE "notitas_usuario"."disabled" = FALSE
      """

      sql += " AND \"notitas_usuario\".\"id\" = :notita_id"
      sql += " AND \"notitas_usuario\".\"usuario_id\" = :usuario_id"

      params["notita_id"] = notita_id
      params["usuario_id"] = usuario_id

      query = session.execute(text(sql), params)
      notita = query.fetchone()

      return notita

  def create_notita_usuario(self, usuario_id: int, notita: NotitaSchema):
    with self.db as session:
      new_notita = NotitaModel(**notita.model_dump())
      session.add(new_notita)
      session.flush()

      notita_usuario = NotitaUsuarioModel(
        usuario_id=usuario_id,
        notita_id=new_notita.id
      )

      session.add(notita_usuario)
      session.commit()
      session.refresh(new_notita)
      session.refresh(notita_usuario)

      new_notita.id = notita_usuario.id
      return new_notita

  def update_notita_usuario(self, usuario_id: int, notita_id: int, notita_update: NotitaSchema):
    with self.db as session:
      params = {}

      sql = """
        SELECT
          "notitas_usuario"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_usuario"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_usuario"."notita_id"
        WHERE "notitas_usuario"."disabled" = FALSE
      """

      sql += " AND \"notitas_usuario\".\"id\" = :notita_id"
      sql += " AND \"notitas_usuario\".\"usuario_id\" = :usuario_id"

      params["notita_id"] = notita_id
      params["usuario_id"] = usuario_id

      query = session.execute(text(sql), params)
      notita = query.fetchone()

      if not notita:
        raise ValueError("No se encontró la notita del usuario")

      # notita = dict(zip(query.keys(), notita))

      # # Actualizar los campos proporcionados en la solicitud
      # for key, value in notita_update.dict(exclude_unset=True).items():
      #   notita[key] = value

      # print(notita)

      # # Ejecutar la consulta de actualización en la base de datos
      # sql_update = text("""
      #   UPDATE "notitas"
      #   SET
      #     "titulo" = :titulo,
      #     "nota" = :nota,
      #     "color" = :color,
      #     "privada" = :privada
      #   WHERE "id" = :id
      # """)

      # session.execute(sql_update, notita)
      # session.commit()
      # return notita

      notita_update = notita_update.dict(exclude_unset=True)
      update_stmt = update(NotitaModel).filter(NotitaModel.id == notita_id).values(**notita_update)
      session.execute(update_stmt)
      session.commit()

      notita = session.query(NotitaModel).filter(NotitaModel.id == notita_id).first()
      return notita

  def delete_notita_usuario(self, usuario_id: int, notita_id: int):
    with self.db as session:
      params = {}

      sql = """
        SELECT
          "notitas_usuario"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_usuario"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_usuario"."notita_id"
        WHERE "notitas_usuario"."disabled" = FALSE
      """

      sql += " AND \"notitas_usuario\".\"id\" = :notita_id"
      sql += " AND \"notitas_usuario\".\"usuario_id\" = :usuario_id"

      params["notita_id"] = notita_id
      params["usuario_id"] = usuario_id

      query = session.execute(text(sql), params)
      notita = query.fetchone()

      if not notita:
        raise ValueError("No se encontró la notita del usuario")

      update_stmt = update(NotitaUsuarioModel).filter(NotitaUsuarioModel.id == notita_id).values(disabled=True)
      session.execute(update_stmt)
      session.commit()

      return True

  def get_notitas_grupo(self, usuario_id: int, grupo_id: int):
    with self.db as session:
      existe_usuario_en_grupo = session.query(MiembroGrupoModel).filter(MiembroGrupoModel.usuario_id == usuario_id, MiembroGrupoModel.grupo_id == grupo_id, MiembroGrupoModel.disabled == False).first()

      if not existe_usuario_en_grupo:
        return None

      params = {}

      sql = """
        SELECT
          "notitas_grupo"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_grupo"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_grupo"."notita_id"
        WHERE "notitas_grupo"."disabled" = FALSE
      """

      sql += " AND \"notitas_grupo\".\"grupo_id\" = :grupo_id"
      params["grupo_id"] = grupo_id

      query = session.execute(text(sql), params)
      notitas = query.fetchall()

      return notitas

  def get_notita_grupo(self, usuario_id: int, grupo_id: int, notita_id: int):
    with self.db as session:
      existe_usuario_en_grupo = session.query(MiembroGrupoModel).filter(MiembroGrupoModel.usuario_id == usuario_id, MiembroGrupoModel.grupo_id == grupo_id, MiembroGrupoModel.disabled == False).first()

      if not existe_usuario_en_grupo:
        return None

      params = {}

      sql = """
        SELECT
          "notitas_grupo"."id",
          "notitas"."titulo",
          "notitas"."nota",
          "notitas"."color",
          "notitas"."privada",
          "notitas"."updated_at"
        FROM "notitas_grupo"
        INNER JOIN "notitas"
        ON "notitas"."id" = "notitas_grupo"."notita_id"
        WHERE "notitas_grupo"."disabled" = FALSE
      """

      sql += " AND \"notitas_grupo\".\"grupo_id\" = :grupo_id"
      sql += " AND \"notitas_grupo\".\"notita_id\" = :notita_id"
      params["grupo_id"] = grupo_id
      params["notita_id"] = notita_id

      query = session.execute(text(sql), params)
      notita = query.fetchone()

      return notita

  def create_notita_grupo(self, usuario_id: int, grupo_id: int, notita: NotitaSchema):
    with self.db as session:
      sql = text("""
        SELECT "roles_grupo"."clave"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."usuario_id" = :usuario_id AND "grupos"."id" = :grupo_id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "grupo_id": grupo_id})
      rol_grupo_clave = query.fetchone()

      if not rol_grupo_clave:
        raise ValueError("No se encontró el rol del grupo para el usuario")

      rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))

      roles_permitidos = ["propietario", "administrador", "editor"]
      if rol_grupo_clave["clave"] not in roles_permitidos:
        raise ValueError("No tiene permisos para crear notitas en este grupo")

      new_notita = NotitaModel(**notita.model_dump())
      session.add(new_notita)
      session.flush()

      notita_grupo = NotitaGrupoModel(
        grupo_id=grupo_id,
        notita_id=new_notita.id
      )

      session.add(notita_grupo)
      session.commit()
      session.refresh(new_notita)
      session.refresh(notita_grupo)

      new_notita.id = notita_grupo.id
      return new_notita