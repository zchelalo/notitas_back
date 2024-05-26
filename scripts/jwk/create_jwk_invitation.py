import os
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import hashlib

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

# Obtener los componentes de la clave pública
public_key = private_key.public_key()
public_numbers = public_key.public_numbers()

# Construir el objeto JWK
jwk_obj = {
  "keys": [
    {
      "kty": "RSA",
      "kid": hashlib.sha256(pem_data).hexdigest(),
      "n": public_numbers.n,
      "e": public_numbers.e
    }
  ]
}

# Convertir el objeto JWK a JSON y mostrarlo
print(json.dumps(jwk_obj, indent=2))