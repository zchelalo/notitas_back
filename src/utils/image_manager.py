import os
from uuid import uuid4

def save_image(image_data, filename: str, folder: str, base_url: str) -> str:
  # Define la ruta de destino
  destination_folder = os.path.join("src", "public", "images", folder)
  os.makedirs(destination_folder, exist_ok=True)  # Crea la carpeta si no existe
  image_path = os.path.join(destination_folder, filename)
  with open(image_path, "wb") as f:
    f.write(image_data)
  return os.path.join(base_url, "notitas_back", "public", "images", folder, filename)  # Retorna la ruta de la imagen guardada con el protocolo HTTP y el host

def generate_unique_filename(original_filename: str) -> str:
  unique_id = uuid4().hex
  _, extension = original_filename.rsplit(".", 1)
  return f"{unique_id}.{extension}"