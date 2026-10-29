# Usamos una imagen oficial de Python como base
FROM python:3.10-slim

# Evitamos que Python genere archivos .pyc y activamos logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalamos LilyPond, TiMidity, Soundfonts y FFmpeg, y configuramos la ruta del soundfont
RUN apt-get update && apt-get install -y --no-install-recommends \
    lilypond \
    ghostscript \
    fluidsynth \
    fluid-soundfont-gm \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copiamos e instalamos las dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos todo el código de tu proyecto al contenedor
COPY . .

# Exponemos el puerto que utiliza Streamlit
EXPOSE 8501

# Comando para ejecutar la aplicación web en la nube
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
