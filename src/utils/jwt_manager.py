from jwt import decode, algorithms
from jwt.exceptions import ExpiredSignatureError
import requests
from dotenv import load_dotenv
import os

load_dotenv()
JWKS_ACCESS_URI = os.getenv("JWKS_ACCESS_URI")

def get_jwks():
  try:
    response = requests.get(JWKS_ACCESS_URI)
    response.raise_for_status()  # Lanza una excepción si la solicitud no tiene éxito
    jwks = response.json()
    return jwks
  except requests.RequestException as e:
    raise e

def validate_token(token: str) -> dict:
  try:
    jwks = get_jwks()
    for key in jwks['keys']:
      public_key = algorithms.RSAAlgorithm.from_jwk(key)
      try:
        data: dict = decode(token, key=public_key, algorithms=["RS256"])
        return data
      except ExpiredSignatureError:
        raise ExpiredSignatureError("Token JWT ha expirado")
      except Exception as e:
        pass
    return {"error": "No se pudo verificar la firma del token"}
  except requests.RequestException as e:
    return {"error": "Error al obtener claves JWKS: " + str(e)}
  except ExpiredSignatureError as e:
    return {"error": str(e)}
  except Exception as e:
    return {"error": "Error desconocido: " + str(e)}