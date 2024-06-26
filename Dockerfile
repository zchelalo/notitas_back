FROM python:3.12.3-slim

# Configura variables de entorno
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PYTHONUNBUFFERED=1

# Actualiza e instala los paquetes necesarios, incluido ffmpeg
RUN apt-get update \
    && apt-get install -y ffmpeg \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Instala las dependencias de tu proyecto FastAPI
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copia los archivos de tu proyecto FastAPI
COPY . .

# Exponer puertos para FastAPI
EXPOSE 8000

# Comando para iniciar tanto FastAPI
CMD ["bash", "-c", "python src/main.py"]