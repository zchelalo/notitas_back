from fastapi import APIRouter, status, File, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
from starlette.status import HTTP_200_OK
from middlewares.auth_handler import CheckRoles
from routes.v1.transcripcion.schema import Text as TextSchema

import tempfile
import speech_recognition as sr
import subprocess
import os
from gtts import gTTS

router = APIRouter()

############################################################################
# TEST
############################################################################
@router.post(
  path='/audio_trascription', 
  tags=['transcripcion'], 
  status_code=status.HTTP_200_OK,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def transcribir_audio(file: UploadFile = File(...)) -> JSONResponse:
  # Crear un archivo temporal para almacenar el audio en formato WebM
  with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_audio:
    temp_audio.write(await file.read())
    temp_audio_path = temp_audio.name

  # Ruta de salida para el archivo WAV convertido
  output_wav_path = temp_audio_path.replace('.webm', '.wav')

  # Ejecutar ffmpeg para convertir el archivo WebM a WAV
  subprocess.run(['ffmpeg', '-i', temp_audio_path, '-vn', '-acodec', 'pcm_s16le', '-ar', '44100', '-ac', '2', output_wav_path])
  
  try:
    # Inicializa el reconocedor
    recognizer = sr.Recognizer()

    # Lee el archivo de audio WAV
    with sr.AudioFile(output_wav_path) as source:
        audio = recognizer.record(source)

    # Reconoce el audio
    texto = recognizer.recognize_google(audio, language="es-ES")

    # Eliminar los archivos temporales
    os.remove(temp_audio_path)
    os.remove(output_wav_path)

    return {"transcripcion": texto}
  except sr.UnknownValueError:
    return {"error": "No se pudo entender el audio"}
  except sr.RequestError as e:
    return {"error": f"Error al solicitar el reconocimiento de voz; {e}"}
  except Exception as e:
    return {"error": f"Error al procesar el archivo de audio; {e}"}

@router.post(
  path='/text_to_speech', 
  tags=['transcripcion'], 
  status_code=status.HTTP_200_OK,
  dependencies=[Depends(CheckRoles("admin", "cliente"))]
)
async def transcribir_audio(
  text: TextSchema
) -> JSONResponse:
  temp_audio_path = None
  try:
    # Crear un archivo temporal para almacenar el audio generado
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_audio:
      tts = gTTS(text=text.texto, lang='es')
      tts.save(temp_audio.name)
      temp_audio_path = temp_audio.name

    # Retornar el archivo de audio como una respuesta de streaming
    return StreamingResponse(open(temp_audio_path, "rb"), media_type="audio/mpeg", headers={"Content-Disposition": "attachment; filename=audio.mp3"})
  
  except Exception as e:
    return {"error": f"Error al procesar el texto; {e}"}
  
  finally:
    # Eliminar el archivo temporal si se ha creado
    if temp_audio_path and os.path.exists(temp_audio_path):
      os.remove(temp_audio_path)