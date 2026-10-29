import hashlib
import os
import shutil
import subprocess
import sys
import streamlit as st

# Agregar la ruta actual para que importe sin problema tus archivos
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

st.set_page_config(page_title="Compilador Bazilio - ANTLR", page_icon="🎵")

st.title("Compilador Bazilio (ANTLR) en la Nube")
st.write(
    "Escribe tu código en Bazilio y genera tus partituras y audios desde"
    " cualquier dispositivo."
)

# Texto predeterminado actualizado según tu código funcional
codigo_usuario = st.text_area(
    "Código Bazilio:", "Main\n|:\n  (:){E4 F3}\n:|\n", height=150
)

if st.button("Compilar y Generar", type="primary"):
  if not codigo_usuario.strip():
    st.warning("Por favor ingresa código.")
  else:
    try:
      # Asegurar que la librería de ANTLR esté instalada en la nube antes de importar
      try:
        import antlr4
      except ImportError:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "antlr4-python3-runtime",
        ])
        import antlr4

      # Importaciones de ANTLR de forma segura dentro del evento
      from BazilioLexer import BazilioLexer
      from BazilioParser import BazilioParser
      from antlr4 import *
      from bazilio import BazilioVisitor

      os.makedirs("Practica", exist_ok=True)

      # 1. Procesar con ANTLR
      input_stream = InputStream(codigo_usuario)
      lexer = BazilioLexer(input_stream)
      stream = CommonTokenStream(lexer)
      parser = BazilioParser(stream)
      tree = parser.programa()

      # 2. Ejecutar tu Visitor/Listener o lógica que genera el .ly / audio
      base = os.path.join(
          "Practica",
          f"partitura_{hashlib.md5(codigo_usuario.encode()).hexdigest()[:6]}",
      )

      ruta_bzl = "temp_cloud.bzl"
      with open(ruta_bzl, "w", encoding="utf-8") as f:
        f.write(codigo_usuario)

      res = subprocess.run(
          ["python3", "bazilio.py", ruta_bzl, "Main"],
          capture_output=True,
          text=True,
      )

      if res.returncode != 0:
        st.error(f"Error de sintaxis ANTLR / Ejecución:\n{res.stderr}")
      else:
        st.success("¡Compilación y generación exitosa con ANTLR!")

        # 3. Mostrar mensaje de búsqueda y cargar el reproductor dinámicamente
        st.info("Buscando archivos de audio generados en la carpeta Practica...")

        audio_encontrado = None

        # Revisar rutas comunes donde tu script de Python podría guardar el audio
        posibles_rutas = ["audio.mp3", "audio.wav"]
        for p in posibles_rutas:
          if os.path.exists(p):
            audio_encontrado = p
            break

        # Si no está en la raíz, buscar dentro de la carpeta 'Practica'
        if not audio_encontrado and os.path.exists("Practica"):
          for archivo in os.listdir("Practica"):
            if archivo.endswith((".mp3", ".wav")):
              audio_encontrado = os.path.join("Practica", archivo)
              break

        # Mostrar el reproductor si se localiza el archivo
        if audio_encontrado:
          formato = "audio/wav" if audio_encontrado.endswith(".wav") else "audio/mp3"
          st.audio(audio_encontrado, format=formato)
        else:
          st.warning(
              "Compilación exitosa, pero no se encontró automáticamente el"
              " archivo de audio. Asegúrate de que tu script `bazilio.py` guarde"
              " el archivo `.mp3` o `.wav` en la raíz o dentro de la carpeta"
              " 'Practica'."
          )

    except Exception as e:
      st.error(f"Error: {e}")
