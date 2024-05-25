from fastapi import HTTPException, Request
from fastapi.security import HTTPBearer
from starlette.status import HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN
from utils.jwt_manager import validate_token

class CheckRoles(HTTPBearer):
  def __init__(self, *roles: str):
    super().__init__()
    self.roles = roles

  async def __call__(self, request: Request):
    auth = await super().__call__(request)
    token_data = validate_token(auth.credentials)
    if "rol" not in token_data:
      raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="El token no contiene rol")
    user_roles = token_data["rol"]
    for rol in self.roles:
      if rol == user_roles:
        request.state.data_usuario = token_data
        return auth
    raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="El usuario no tiene permisos suficientes")

# class CheckAuthentication(HTTPBearer):
#   async def __call__(self, request: Request):
#     try:
#       auth = await super().__call__(request)
#       token_data = validate_token(auth.credentials)
#       if token_data.get("sub") is None:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="El token es invalido")

#       request.state.data_usuario = token_data
#       return auth
#     except HTTPException as e:
#       if e.status_code == HTTP_401_UNAUTHORIZED:
#         raise HTTPException(status_code=HTTP_401_UNAUTHORIZED, detail="Acceso no autorizado. Token JWT no válido o ausente")
#       else:
#         raise e