from fastapi import APIRouter, status, File, UploadFile, Depends
from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK
from middlewares.auth_handler import CheckRoles

import tempfile
import speech_recognition as sr

router = APIRouter()

############################################################################
# TEST
############################################################################
@router.post(
    path='/transcribir_audio', 
    tags=['test'], 
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(CheckRoles("admin"))]
  )
async def transcribir_audio(file: UploadFile = File(...)) -> JSONResponse:
  with tempfile.NamedTemporaryFile(delete=False) as temp_audio:
    temp_audio.write(await file.read())
    temp_audio_path = temp_audio.name

  # Inicializa el reconocedor
  recognizer = sr.Recognizer()

  # Lee el archivo de audio
  with sr.AudioFile(temp_audio_path) as source:
    audio = recognizer.record(source)

  try:
    # Reconoce el audio
    texto = recognizer.recognize_google(audio, language="es-ES")
    return {"transcripcion": texto}
  except sr.UnknownValueError:
    return {"error": "No se pudo entender el audio"}
  except sr.RequestError as e:
    return {"error": f"Error al solicitar el reconocimiento de voz; {e}"}