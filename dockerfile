FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    lilypond \
    ghostscript \
    fluidsynth \
    fluid-soundfont-gm \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Render define $PORT; usamos la forma shell para expandirlo
CMD streamlit run index.py --server.address=0.0.0.0 --server.port=${PORT:-8501} --server.headless=true
