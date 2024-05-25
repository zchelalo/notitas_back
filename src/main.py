from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from docs import tags_metadata
from middlewares.error_handler import ErrorHandler

from routes.index import router

import os
import uvicorn

if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=int(os.environ.get("PORT", 8000)), reload=True)

app = FastAPI(
	title= 'REST API para el backend de Notitas',
	description= 'API para el manejo del backend de Notitas, desarrollada con FastAPI y PostgreSQL',
	version= '0.0.1',
	openapi_tags=tags_metadata,
  openapi_url="/public/docs/openapi.json",
  docs_url="/public/docs/swagger",
  redoc_url="/public/docs/redoc"
)

app.add_middleware(ErrorHandler)

# Configura el middleware CORS para permitir solicitudes desde cualquier origen
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],  # Esto permitirá solicitudes desde cualquier origen, cambia a una lista de orígenes permitidos si es necesario.
	allow_credentials=True,
	allow_methods=["*"],  # Puedes especificar los métodos HTTP permitidos
	allow_headers=["*"],  # Puedes especificar los encabezados permitidos
)

app.mount("/public", StaticFiles(directory="src/public"), name="public")

app.include_router(router, prefix="/api")