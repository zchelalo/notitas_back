from sqlalchemy import text
import jwt
import time
import os
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import requests

from models import (
  UsuarioModel,
  GrupoModel,
  MiembroGrupoModel,
  RolGrupoModel
)
from routes.v1.miembro_grupo.schema import MiembroGrupo as MiembroGrupoSchema, InvitationData as InvitationDataSchema, TokenAceptarInv as TokenAceptarInvSchema

class MiembroGrupoService():
  def __init__(self, db) -> None:
    self.db = db

  def get_miembros_grupo(self, grupo_id: int, usuario_id: int):
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
      
      # if rol_grupo_clave:
      #   rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))  # Convertir a un diccionario
      return miembros_grupo

  def get_miembro_grupo(self, id: int):
    with self.db as session:
      # filtros = [
      #   MiembroGrupoModel.disabled == False
      # ]

      # filtros.append(MiembroGrupoModel.id == id)

      # result = session.query(MiembroGrupoModel).filter(*filtros).one_or_none()

      sql = text("""
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
        WHERE "miembros_grupo"."disabled" = FALSE AND "miembros_grupo"."id" = :miembro_grupo_id
      """)

      query = session.execute(sql, {"miembro_grupo_id": id})
      miembro_grupo = query.fetchone()

      if not miembro_grupo:
        raise ValueError("No se encontró el miembro del grupo")

      miembro_grupo = dict(zip(query.keys(), miembro_grupo))

      return miembro_grupo

  def invitar_miembro_grupo(self, inv_data: InvitationDataSchema, usuario_id: int):
    with self.db as session:
      grupo = session.query(GrupoModel).filter(GrupoModel.id == inv_data.grupo_id, GrupoModel.disabled == False).one_or_none()
      if not grupo:
        raise ValueError("No se encontró el grupo")

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

      rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))

      roles_permitidos = ["propietario", "administrador"]

      if rol_grupo_clave.get("clave") not in roles_permitidos:
        raise ValueError("El usuario no tiene permisos para invitar personas a este grupo")

      usuario = session.query(UsuarioModel).filter(UsuarioModel.correo == inv_data.correo, UsuarioModel.disabled == False).one_or_none()
      if not usuario:
        raise ValueError("No se encontró al usuario")
      
      rol_grupo = session.query(RolGrupoModel).filter(RolGrupoModel.id == inv_data.rol_grupo_id).one_or_none()
      if not rol_grupo:
        raise ValueError("No se encontró el rol del grupo")

      existe_usuario_en_grupo = session.query(MiembroGrupoModel).filter(MiembroGrupoModel.usuario_id == usuario.id, MiembroGrupoModel.grupo_id == grupo.id).one_or_none()
      if existe_usuario_en_grupo and not existe_usuario_en_grupo.disabled:
        raise ValueError("El usuario ya es miembro del grupo")

      # if existe_usuario_en_grupo and existe_usuario_en_grupo.disabled:
      #   return { 'a': 'a' }

      # MANDAR CORREO DE INVITACIÓN
      # Leer la clave privada PEM
      ruta_certs = os.path.join(os.getcwd(), 'certs')
      with open(os.path.join(ruta_certs, 'private_invitation.pem'), 'rb') as pem_file:
        pem_data = pem_file.read()

      # Cargar la clave privada
      private_key = serialization.load_pem_private_key(
        pem_data,
        password=None,
        backend=default_backend()
      )

      # Definir el tiempo actual y el tiempo de expiración (10 minutos)
      current_time = int(time.time())
      expiration_time = current_time + 600  # 10 minutos en segundos

      # Definir los datos del JWT (claims)
      jwt_payload = {
        'sub': usuario.id,
        'grupo_id': grupo.id,
        'rol_grupo_id': rol_grupo.id,
        'exp': expiration_time
      }

      # Crear el JWT firmado
      jwt_token = jwt.encode(jwt_payload, private_key, algorithm='RS256')

      link = f'http://localhost:5173/invitacion?token={jwt_token}'

      info = {
        'from': 'Notitas',
        'to': usuario.correo,
        'subject': f'Invitación para unirse a {grupo.nombre}',
        'html': f'<b>Acepte la invitación ingresando al siguiente link</b><br /><a href="{link}">Aceptar</a>'
      }

      url = 'http://notitas_email:3000/api/v1/correo'

      response = requests.post(url, json=info)
      response.raise_for_status()

      # print(jwt_token)

      return response.json()

  def aceptar_invitacion_miembro_grupo(self, token_data: TokenAceptarInvSchema):
    with self.db as session:
      # Leer la clave pública PEM
      ruta_certs = os.path.join(os.getcwd(), 'certs')
      with open(os.path.join(ruta_certs, 'public_invitation.pem'), 'rb') as pem_file:
        pem_data = pem_file.read()

      # Cargar la clave pública
      public_key = serialization.load_pem_public_key(
        pem_data,
        backend=default_backend()
      )

      payload = jwt.decode(token_data.token, public_key, algorithms=["RS256"])

      usuario = session.query(UsuarioModel).filter(UsuarioModel.id == payload['sub'], UsuarioModel.disabled == False).one_or_none()
      if not usuario:
        raise ValueError("No se encontró al usuario")

      grupo = session.query(GrupoModel).filter(GrupoModel.id == payload['grupo_id'], GrupoModel.disabled == False).one_or_none()
      if not grupo:
        raise ValueError("No se encontró el grupo")

      rol_grupo = session.query(RolGrupoModel).filter(RolGrupoModel.id == payload['rol_grupo_id']).one_or_none()
      if not rol_grupo:
        raise ValueError("No se encontró el rol del grupo")

      miembro_grupo = session.query(MiembroGrupoModel).filter(MiembroGrupoModel.usuario_id == usuario.id, MiembroGrupoModel.grupo_id == grupo.id).one_or_none()
      if miembro_grupo and not miembro_grupo.disabled:
        raise ValueError("El usuario ya es miembro del grupo")

      if miembro_grupo and miembro_grupo.disabled:
        miembro_grupo.disabled = False
        session.commit()
        session.refresh(miembro_grupo)
        return miembro_grupo

      new_miembro_grupo_schema = MiembroGrupoSchema(usuario_id=usuario.id, grupo_id=grupo.id, rol_grupo_id=rol_grupo.id)
      new_miembro_grupo = MiembroGrupoModel(**new_miembro_grupo_schema.model_dump())
      session.add(new_miembro_grupo)
      session.commit()
      session.refresh(new_miembro_grupo)

      return new_miembro_grupo

  def update_miembro_grupo(self, id: int, miembro_grupo_update: MiembroGrupoSchema, usuario_id: int):
    with self.db as session:
      sql_miembro_grupo = text("""
        SELECT
          "miembros_grupo"."id",
          "miembros_grupo"."grupo_id",
          "miembros_grupo"."usuario_id",
          "miembros_grupo"."rol_grupo_id",
          "roles_grupo"."clave" as "rol_grupo_clave"
        FROM "miembros_grupo"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."id" = :miembro_grupo_id
        AND "miembros_grupo"."disabled" = FALSE
      """)

      query_miembro_grupo = session.execute(sql_miembro_grupo, {"miembro_grupo_id": id})
      miembro_grupo = query_miembro_grupo.fetchone()

      if not miembro_grupo:
        raise ValueError("No se encontró al miembro del grupo")

      miembro_grupo = dict(zip(query_miembro_grupo.keys(), miembro_grupo))

      sql = text("""
        SELECT "roles_grupo"."clave"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."usuario_id" = :usuario_id AND "grupos"."id" = :grupo_id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "grupo_id": miembro_grupo.get("grupo_id")})
      rol_grupo_clave = query.fetchone()

      if not rol_grupo_clave:
        raise ValueError("No se encontró el rol del grupo para el usuario")

      rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))

      roles_permitidos = ["propietario", "administrador"]

      if rol_grupo_clave.get("clave") not in roles_permitidos:
        raise ValueError("El usuario no tiene permisos para modificar el rol de los miembros en este grupo")

      if miembro_grupo.get("rol_grupo_clave") == "propietario":
        raise ValueError("No se puede modificar el rol del propietario")

      if miembro_grupo.get("rol_grupo_clave") == "administrador" and rol_grupo_clave.get("clave") == "administrador":
        raise ValueError("No se puede modificar el rol del administrador")

      rol = session.query(RolGrupoModel).filter(RolGrupoModel.id == miembro_grupo_update.rol_grupo_id).one_or_none()
      if not rol:
        raise ValueError("No se encontró el rol del grupo")

      roles_permitidos_modificar = []

      if rol_grupo_clave.get("clave") == "administrador":
        roles_permitidos_modificar = ["invitado", "editor"]
      elif rol_grupo_clave.get("clave") == "propietario":
        roles_permitidos_modificar = ["invitado", "editor", "administrador"]

      if rol.clave not in roles_permitidos_modificar:
        raise ValueError("No se puede modificar el rol del miembro")

      # Actualizar los campos proporcionados en la solicitud
      for key, value in miembro_grupo_update.dict(exclude_unset=True).items():
        miembro_grupo[key] = value

      # Ejecutar la consulta de actualización en la base de datos
      sql_update = text("""
        UPDATE "miembros_grupo"
        SET
          "rol_grupo_id" = :rol_grupo_id
        WHERE "id" = :miembro_grupo_id
      """)

      session.execute(sql_update, {
        "rol_grupo_id": miembro_grupo["rol_grupo_id"],
        "miembro_grupo_id": id
      })

      session.commit()
      return miembro_grupo

  def delete_miembro_grupo(self, id: int, usuario_id: int):
    with self.db as session:
      sql_miembro_grupo = text("""
        SELECT
          "miembros_grupo"."id",
          "miembros_grupo"."grupo_id",
          "miembros_grupo"."usuario_id",
          "miembros_grupo"."rol_grupo_id",
          "roles_grupo"."clave" as "rol_grupo_clave"
        FROM "miembros_grupo"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."id" = :miembro_grupo_id
        AND "miembros_grupo"."disabled" = FALSE
      """)

      query_miembro_grupo = session.execute(sql_miembro_grupo, {"miembro_grupo_id": id})
      miembro_grupo = query_miembro_grupo.fetchone()

      if not miembro_grupo:
        raise ValueError("No se encontró al miembro del grupo")

      miembro_grupo = dict(zip(query_miembro_grupo.keys(), miembro_grupo))

      sql = text("""
        SELECT "roles_grupo"."clave"
        FROM "grupos"
        INNER JOIN "miembros_grupo"
        ON "miembros_grupo"."grupo_id" = "grupos"."id"
        INNER JOIN "roles_grupo"
        ON "miembros_grupo"."rol_grupo_id" = "roles_grupo"."id"
        WHERE "miembros_grupo"."usuario_id" = :usuario_id AND "grupos"."id" = :grupo_id
      """)

      query = session.execute(sql, {"usuario_id": usuario_id, "grupo_id": miembro_grupo.get("grupo_id")})
      rol_grupo_clave = query.fetchone()

      if not rol_grupo_clave:
        raise ValueError("No se encontró el rol del grupo para el usuario")

      rol_grupo_clave = dict(zip(query.keys(), rol_grupo_clave))

      roles_permitidos = ["propietario", "administrador"]

      if rol_grupo_clave.get("clave") not in roles_permitidos:
        raise ValueError("El usuario no tiene permisos para eliminar miembros en este grupo")

      if miembro_grupo.get("rol_grupo_clave") == "propietario":
        raise ValueError("No se puede eliminar al propietario")

      if miembro_grupo.get("rol_grupo_clave") == "administrador" and rol_grupo_clave.get("clave") == "administrador":
        raise ValueError("No se puede eliminar a un administrador")

      sql_delete = text("""
        UPDATE "miembros_grupo"
        SET
          "disabled" = TRUE
        WHERE "id" = :miembro_grupo_id
      """)

      session.execute(sql_delete, {
        "miembro_grupo_id": id
      })

      session.commit()
      return True